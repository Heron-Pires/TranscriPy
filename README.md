# TranscriPy

**TranscriPy** is a lightweight, local, and privacy-focused desktop audio transcription tool built with Python, [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), and [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

It runs completely offline on your computer (CPU or NVIDIA GPU with CUDA acceleration), detects speech in multiple languages automatically, and saves transcripts directly into clean text files.

---

## Features

- **100% Private & Local**: Your audio files and transcripts never leave your machine.
- **Hardware Acceleration (GPU/CUDA)**: Optional toggle for NVIDIA GPU acceleration (INT8 / FP16 / FP32) with automatic CPU fallback.
- **Model Selection**: Switch between Whisper model sizes (`tiny`, `base`, `small`, `medium`) directly from the UI.
- **Optional Timestamps**: Toggle timestamp markers (`[00:01:23]`) or output clean text paragraphs.
- **Optional Live Text Preview**: Toggle a real-time text view to watch transcripts stream segment by segment, with **Copy Text** and **Open Folder** shortcuts.
- **Cancellation Control**: Stop transcription at any point and automatically preserve the partial transcript.
- **Automatic Language Detection**: Transcribes audio in English, Portuguese, Spanish, French, German, and 90+ other languages automatically.
- **Fast & Efficient**: Powered by `faster-whisper` with INT8 quantization, providing up to 4x speedup over standard Whisper on CPU and 10x+ on CUDA.
- **Modern Dark UI**: Sleek, distraction-free desktop interface built with CustomTkinter.
- **Real-time Progress Bar**: Displays actual transcription progress percentage and step-by-step status.
- **Wide Format Support**: Accepts `.mp3`, `.wav`, `.m4a`, `.mp4`, `.aac`, `.flac`, `.mkv`, `.ogg`, and `.wma`.
- **Automatic Export**: Transcriptions are automatically saved as `[filename]_transcription.txt` in the same folder as the input audio.

---

## Prerequisites

1. **Python 3.8 to 3.12+** ([python.org](https://www.python.org/downloads/)). When installing on Windows, check **"Add Python to PATH"**.
2. **FFmpeg** (required for decoding audio):
   - **Windows**: Run `winget install Gyan.FFmpeg` in terminal, or install via chocolatey (`choco install ffmpeg`).
   - **Linux (Ubuntu/Debian)**: `sudo apt install ffmpeg`

---

## Quick Start (Easiest Method - No Virtual Environment Needed)

You do **not** need a virtual environment. You can install the dependencies globally and run the app with one click.

### Windows

1. Open PowerShell or Command Prompt in the project folder and run:
   ```powershell
   pip install -r requirements.txt
   ```
2. **To launch the app**:
   - Simply double-click **`run.bat`** (or double-click `transcripy.py`).
   *(The `run.bat` script can also auto-install missing packages on first launch).*

### Linux

1. Install system requirements and dependencies:
   ```bash
   sudo apt install -y python3 python3-pip python3-tk ffmpeg
   pip3 install -r requirements.txt
   ```
2. **To launch the app**:
   - Run:
     ```bash
     python3 transcripy.py
     ```
   - Or use the included script:
     ```bash
     chmod +x run.sh
     ./run.sh
     ```

---

## How to Use

1. **Configure Options (Optional)**:
   - Check **GPU Acceleration (CUDA)** to use your NVIDIA graphics card.
   - Choose your **Whisper Model** size (`small` recommended for a great balance of speed and accuracy).
   - Check **Include Timestamps** if you want `[mm:ss]` markers for each spoken sentence.
   - Check **Show Text Preview** if you want to inspect text live as it is transcribed.
2. Click **"Select Audio (MP3, WAV, M4A...)"**.
3. Select your audio or video file.
4. Wait for transcription to complete (first run downloads the Whisper model once).
5. The transcript is automatically saved alongside the original audio file as `[filename]_transcription.txt`. You can also click **"Copy Text"** or **"Open Folder"** directly from the app.

---

## Advanced Installation (Using Virtual Environment)

<details>
<summary><b>Click to expand instructions for Python Virtual Environment (venv)</b></summary>

A virtual environment isolates project dependencies from your system's global Python:

### Windows (venv)
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python transcripy.py
```

### Linux (venv)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 transcripy.py
```
</details>

---

## Uninstallation

### Windows

1. **Delete Cached Models** (frees ~500 MB):
   ```powershell
   Remove-Item -Recurse -Force "$env:USERPROFILE\.cache\huggingface\hub\models--Systran--faster-whisper-small"
   ```
2. **Delete Project Folder**:
   Simply delete the `transcripy` folder.
3. *(Optional)* Uninstall packages:
   ```powershell
   pip uninstall -y customtkinter faster-whisper
   ```

### Linux

1. **Delete Cached Models**:
   ```bash
   rm -rf ~/.cache/huggingface/hub/models--Systran--faster-whisper-small
   ```
2. **Delete Project Folder**:
   ```bash
   rm -rf /path/to/transcripy
   ```
3. *(Optional)* Uninstall packages:
   ```bash
   pip3 uninstall -y customtkinter faster-whisper
   ```

---

## Troubleshooting & FAQ

<details>
<summary><b>1. "FileNotFoundError" or error related to FFmpeg</b></summary>

Ensure FFmpeg is installed and added to your PATH:
```bash
ffmpeg -version
```
- On **Windows**: Run `winget install Gyan.FFmpeg` and restart terminal.
- On **Linux**: Run `sudo apt install ffmpeg`.
</details>

<details>
<summary><b>2. "ModuleNotFoundError: No module named '_tkinter'" on Linux</b></summary>

Install the Tkinter package:
- Ubuntu/Debian: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch: `sudo pacman -S tk`
</details>

<details>
<summary><b>3. Why is the first transcription slower?</b></summary>

On the first run, the selected Whisper model is downloaded automatically from Hugging Face. After this initial download, all transcriptions run locally and offline.
</details>

<details>
<summary><b>4. How does CUDA acceleration work?</b></summary>

When enabled, TranscriPy detects your NVIDIA GPU and runs using `ctranslate2` CUDA kernels. If CUDA runtime libraries are not present, it will automatically fallback to CPU without interrupting the workflow.
</details>

---

## License

This project is open-source and free to use. Licensed under the [MIT License](https://opensource.org/licenses/MIT).
