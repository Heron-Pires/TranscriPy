import os
import platform
import subprocess
import threading
from tkinter import filedialog

import customtkinter as ctk
from faster_whisper import WhisperModel

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def format_timestamp(seconds: float) -> str:
    """Format seconds into [HH:MM:SS] or [MM:SS] format."""
    total_seconds = max(0, int(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def open_in_file_manager(path: str):
    """Open the file's parent folder in the system file manager."""
    folder = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(folder):
        return
    current_os = platform.system()
    if current_os == "Windows":
        os.startfile(folder)
    elif current_os == "Darwin":
        subprocess.Popen(["open", folder])
    else:
        subprocess.Popen(["xdg-open", folder])


def check_cuda_support() -> bool:
    """Check if CUDA is available through ctranslate2."""
    try:
        import ctranslate2

        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


def get_supported_compute_type(device: str) -> str:
    """Get the optimal compute type supported by the hardware device."""
    try:
        import ctranslate2

        supported = ctranslate2.get_supported_compute_types(device)
        if device == "cuda":
            for ct in ["float16", "int8_float16", "int8", "float32"]:
                if ct in supported:
                    return ct
        else:
            for ct in ["int8", "int8_float32", "float32"]:
                if ct in supported:
                    return ct
    except Exception:
        pass
    return "int8" if device == "cpu" else "default"


class TranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TranscriPy - Whisper")
        self.geometry("600x430")
        self.minsize(540, 400)
        self.resizable(True, True)

        # Model and processing state
        self.model = None
        self.loaded_model_name = None
        self.loaded_device = None
        self.cancel_event = threading.Event()
        self.last_transcript = ""
        self.last_output_path = ""

        self.cuda_available = check_cuda_support()

        self._create_widgets()

    def _create_widgets(self):
        # 1. Header
        self.title_label = ctk.CTkLabel(
            self, text="TranscriPy", font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=(16, 2))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Local & Private Audio Transcriber",
            font=("Arial", 12),
            text_color="gray",
        )
        self.subtitle_label.pack(pady=(0, 10))

        # 2. Options card (GPU, Timestamps, Preview, Model)
        self.options_frame = ctk.CTkFrame(
            self, fg_color=("gray85", "gray17"), corner_radius=8
        )
        self.options_frame.pack(fill="x", padx=25, pady=(0, 12))

        # Row 0: GPU toggle + Model selector
        self.cuda_var = ctk.BooleanVar(value=False)
        if self.cuda_available:
            self.cuda_check = ctk.CTkCheckBox(
                self.options_frame,
                text="GPU Acceleration (CUDA)",
                variable=self.cuda_var,
                font=("Arial", 12),
            )
        else:
            self.cuda_check = ctk.CTkCheckBox(
                self.options_frame,
                text="GPU (CUDA not detected)",
                variable=self.cuda_var,
                state="disabled",
                font=("Arial", 12),
            )
        self.cuda_check.grid(row=0, column=0, padx=15, pady=(10, 6), sticky="w")

        model_subframe = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        model_subframe.grid(row=0, column=1, padx=15, pady=(10, 6), sticky="e")

        ctk.CTkLabel(model_subframe, text="Model:", font=("Arial", 12)).pack(
            side="left", padx=(0, 6)
        )
        self.model_var = ctk.StringVar(value="small")
        self.model_menu = ctk.CTkOptionMenu(
            model_subframe,
            values=["tiny", "base", "small", "medium"],
            variable=self.model_var,
            width=100,
            height=28,
        )
        self.model_menu.pack(side="left")

        # Row 1: Timestamps toggle + Text Preview toggle
        self.timestamps_var = ctk.BooleanVar(value=False)
        self.timestamps_check = ctk.CTkCheckBox(
            self.options_frame,
            text="Include Timestamps ([00:00])",
            variable=self.timestamps_var,
            font=("Arial", 12),
        )
        self.timestamps_check.grid(row=1, column=0, padx=15, pady=(6, 10), sticky="w")

        self.preview_var = ctk.BooleanVar(value=False)
        self.preview_check = ctk.CTkCheckBox(
            self.options_frame,
            text="Show Text Preview",
            variable=self.preview_var,
            command=self.toggle_preview,
            font=("Arial", 12),
        )
        self.preview_check.grid(row=1, column=1, padx=15, pady=(6, 10), sticky="w")

        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)

        # 3. Action buttons (Select audio + Cancel)
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(pady=(2, 6))

        self.btn_select = ctk.CTkButton(
            self.actions_frame,
            text="Select Audio (MP3, WAV, M4A...)",
            command=self.start_transcription,
            font=("Arial", 13, "bold"),
            height=36,
            width=290,
        )
        self.btn_select.pack(side="left", padx=5)

        self.btn_cancel = ctk.CTkButton(
            self.actions_frame,
            text="Cancel",
            fg_color="#c0392b",
            hover_color="#962d22",
            command=self.cancel_transcription,
            width=85,
            height=36,
            state="disabled",
        )
        self.btn_cancel.pack(side="left", padx=5)

        # 4. Status and progress bar
        self.status_label = ctk.CTkLabel(
            self, text="Waiting for file...", font=("Arial", 12), wraplength=540
        )
        self.status_label.pack(pady=(8, 4))

        self.progress = ctk.CTkProgressBar(self, width=500)
        self.progress.pack(pady=4)
        self.progress.set(0)

        # 5. Result action buttons (Copy text & Open folder)
        self.results_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.results_frame.pack(pady=(8, 6))

        self.btn_copy = ctk.CTkButton(
            self.results_frame,
            text="Copy Text",
            command=self.copy_to_clipboard,
            width=125,
            state="disabled",
        )
        self.btn_copy.pack(side="left", padx=6)

        self.btn_open_folder = ctk.CTkButton(
            self.results_frame,
            text="Open Folder",
            command=self.open_output_folder,
            width=125,
            state="disabled",
        )
        self.btn_open_folder.pack(side="left", padx=6)

        # 6. Text Preview Frame (dynamically toggled)
        self.preview_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.textbox = ctk.CTkTextbox(
            self.preview_frame, wrap="word", font=("Consolas", 12)
        )
        self.textbox.pack(fill="both", expand=True)

    def toggle_preview(self):
        """Toggle text preview widget and dynamically adjust window height."""
        if self.preview_var.get():
            self.preview_frame.pack(fill="both", expand=True, padx=25, pady=(5, 15))
            self.geometry("600x670")
            # If a transcript was already generated, populate the textbox
            if self.last_transcript and not self.textbox.get("1.0", "end").strip():
                self.textbox.delete("1.0", "end")
                self.textbox.insert("end", self.last_transcript)
        else:
            self.preview_frame.pack_forget()
            self.geometry("600x430")

    def update_progress_ui(self, percentage, text):
        self.progress.set(percentage)
        self.status_label.configure(text=text)

    def append_preview_text(self, text_line):
        self.textbox.insert("end", text_line + "\n")
        self.textbox.see("end")

    def enable_result_buttons(self):
        self.btn_copy.configure(state="normal")
        self.btn_open_folder.configure(state="normal")

    def copy_to_clipboard(self):
        if not self.last_transcript:
            return
        self.clipboard_clear()
        self.clipboard_append(self.last_transcript)
        self.update()
        original_text = self.btn_copy.cget("text")
        self.btn_copy.configure(text="Copied!")
        self.after(1500, lambda: self.btn_copy.configure(text=original_text))

    def open_output_folder(self):
        if self.last_output_path:
            open_in_file_manager(self.last_output_path)

    def cancel_transcription(self):
        self.cancel_event.set()
        self.btn_cancel.configure(state="disabled")
        self.status_label.configure(text="Cancelling transcription...")

    def start_transcription(self):
        audio_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[
                (
                    "Audio/Video Files",
                    "*.mp3 *.wav *.m4a *.mp4 *.aac *.flac *.mkv *.ogg *.wma",
                ),
                ("All Files", "*.*"),
            ],
        )

        if not audio_path:
            return

        self.cancel_event.clear()
        self.last_transcript = ""
        self.last_output_path = ""

        self.btn_select.configure(state="disabled")
        self.btn_cancel.configure(state="normal")
        self.btn_copy.configure(state="disabled")
        self.btn_open_folder.configure(state="disabled")

        self.progress.set(0)
        self.update_progress_ui(0, "Starting processing...")

        if self.preview_var.get():
            self.textbox.delete("1.0", "end")

        threading.Thread(
            target=self.process_audio, args=(audio_path,), daemon=True
        ).start()

    def process_audio(self, audio_path):
        try:
            target_model = self.model_var.get()
            use_cuda = self.cuda_var.get() and self.cuda_available
            target_device = "cuda" if use_cuda else "cpu"
            compute_type = get_supported_compute_type(target_device)

            # Load or re-load model if model size or target device changed
            if (
                self.model is None
                or self.loaded_model_name != target_model
                or self.loaded_device != target_device
            ):
                self.after(
                    0,
                    self.update_progress_ui,
                    0,
                    f"Loading Whisper '{target_model}' model ({target_device.upper()})...",
                )
                try:
                    self.model = WhisperModel(
                        target_model, device=target_device, compute_type=compute_type
                    )
                    self.loaded_model_name = target_model
                    self.loaded_device = target_device
                except Exception as model_err:
                    if target_device == "cuda":
                        self.after(
                            0,
                            self.update_progress_ui,
                            0,
                            "CUDA initialization failed. Falling back to CPU...",
                        )
                        target_device = "cpu"
                        compute_type = get_supported_compute_type("cpu")
                        self.model = WhisperModel(
                            target_model,
                            device="cpu",
                            compute_type=compute_type,
                        )
                        self.loaded_model_name = target_model
                        self.loaded_device = "cpu"
                    else:
                        raise model_err

            self.after(0, self.update_progress_ui, 0, "Transcribing audio...")

            segments, info = self.model.transcribe(audio_path, vad_filter=True)
            total_duration = info.duration or 0
            full_text = []
            include_timestamps = self.timestamps_var.get()

            for segment in segments:
                if self.cancel_event.is_set():
                    break

                text_clean = segment.text.strip()
                if not text_clean:
                    continue

                if include_timestamps:
                    line = f"[{format_timestamp(segment.start)}] {text_clean}"
                else:
                    line = text_clean

                full_text.append(line)

                if self.preview_var.get():
                    self.after(0, self.append_preview_text, line)

                if total_duration > 0:
                    progress = min(1.0, segment.end / total_duration)
                    progress_text = f"Transcribing: {int(progress * 100)}%"
                    self.after(
                        0,
                        self.update_progress_ui,
                        progress,
                        progress_text,
                    )

            # Handle cancellation
            if self.cancel_event.is_set():
                result_text = "\n".join(full_text)
                self.last_transcript = result_text
                if result_text:
                    output_path = (
                        os.path.splitext(audio_path)[0]
                        + "_partial_transcription.txt"
                    )
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(result_text)
                    self.last_output_path = output_path
                    self.after(
                        0,
                        self.update_progress_ui,
                        self.progress.get(),
                        f"Cancelled! Partial transcript saved to:\n{output_path}",
                    )
                    self.after(0, self.enable_result_buttons)
                else:
                    self.after(
                        0, self.update_progress_ui, 0, "Transcription cancelled."
                    )
                return

            result_text = "\n".join(full_text)
            self.last_transcript = result_text

            output_path = os.path.splitext(audio_path)[0] + "_transcription.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result_text)

            self.last_output_path = output_path

            self.after(
                0,
                self.update_progress_ui,
                1.0,
                f"Done! Saved to:\n{output_path}",
            )
            self.after(0, self.enable_result_buttons)

        except Exception as e:
            self.after(
                0,
                self.update_progress_ui,
                0,
                f"Error processing audio: {str(e)}",
            )

        finally:
            self.after(0, lambda: self.btn_select.configure(state="normal"))
            self.after(0, lambda: self.btn_cancel.configure(state="disabled"))


if __name__ == "__main__":
    app = TranscriberApp()
    app.mainloop()
