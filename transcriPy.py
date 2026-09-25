import os
import threading
from tkinter import filedialog

import customtkinter as ctk
from faster_whisper import WhisperModel

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TranscriPy - Whisper")
        self.geometry("550x350")
        self.resizable(True, True)

        # Variable to store the loaded model in memory
        self.model = None

        self.title_label = ctk.CTkLabel(
            self, text="Local Audio Transcriber", font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=20)

        self.btn_select = ctk.CTkButton(
            self,
            text="Select Audio (MP3, WAV, M4A...)",
            command=self.start_transcription,
        )
        self.btn_select.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self, text="Waiting for file...", font=("Arial", 12)
        )
        self.status_label.pack(pady=15)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=10)
        self.progress.set(0)

    def update_progress_ui(self, percentage, text):
        self.progress.set(percentage)
        self.status_label.configure(text=text)

    def start_transcription(self):
        audio_path = filedialog.askopenfilename(
            title="Select an audio file",
            filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.mp4 *.aac *.flac")],
        )

        if not audio_path:
            return

        self.btn_select.configure(state="disabled")
        self.progress.set(0)
        self.update_progress_ui(0, "Starting processing...")

        threading.Thread(
            target=self.process_audio, args=(audio_path,), daemon=True
        ).start()

    def process_audio(self, audio_path):
        try:
            # Load the model only on the first transcription
            if self.model is None:
                self.after(
                    0,
                    self.update_progress_ui,
                    0,
                    "Loading Whisper model into memory...",
                )
                self.model = WhisperModel("small", device="cpu", compute_type="int8")

            self.after(0, self.update_progress_ui, 0, "Transcribing audio...")

            # Transcribe with automatic language detection
            segments, info = self.model.transcribe(audio_path, vad_filter=True)
            total_duration = info.duration
            full_text = []

            for segment in segments:
                full_text.append(segment.text)

                if total_duration > 0:
                    # Cap progress at 1.0 to avoid visual glitches
                    progress = min(1.0, segment.end / total_duration)
                    progress_text = f"Transcribing: {int(progress * 100)}%"
                    self.after(
                        0,
                        self.update_progress_ui,
                        progress,
                        progress_text,
                    )

            result_text = "\n".join(full_text)

            output_path = os.path.splitext(audio_path)[0] + "_transcription.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result_text)

            self.after(
                0,
                self.update_progress_ui,
                1.0,
                f"Done! Saved to:\n{output_path}",
            )

        except Exception as e:
            self.after(
                0, self.update_progress_ui, 0, f"Error processing audio: {str(e)}"
            )

        finally:
            self.after(0, lambda: self.btn_select.configure(state="normal"))


if __name__ == "__main__":
    app = TranscriberApp()
    app.mainloop()
