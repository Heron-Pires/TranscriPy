# TranscriPy 🎙️

**TranscriPy** is a lightweight, local, and privacy-focused desktop audio transcription tool built with Python, [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), and [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

It runs completely offline on your computer (CPU-optimized with INT8 quantization), detects speech in multiple languages automatically, and saves transcripts directly into clean text files.

---

## ✨ Features

- **🔒 100% Private & Local**: Your audio files and transcripts never leave your machine.
- **🌐 Automatic Language Detection**: Transcribes audio in English, Portuguese, Spanish, French, German, and 90+ other languages automatically.
- **⚡ Fast & Efficient**: Powered by `faster-whisper` (`small` model with `int8` quantization), providing up to 4x speedup over standard Whisper on CPU.
- **🎨 Modern Dark UI**: Sleek, distraction-free desktop interface built with CustomTkinter.
- **📊 Real-time Progress Bar**: Displays actual transcription progress percentage and step-by-step status.
- **📁 Wide Format Support**: Accepts `.mp3`, `.wav`, `.m4a`, `.mp4`, `.aac`, and `.flac`.
- **💾 Automatic Export**: Transcriptions are automatically saved as `[filename]_transcription.txt` in the same folder as the input audio.

---

## 📋 System Requirements

- **Python**: Version `3.8` to `3.12` (Python `3.10` or `3.11` recommended)
- **FFmpeg**: Required for audio decoding across formats.
- **Memory (RAM)**: Minimum 4 GB RAM (8 GB+ recommended).
- **Disk Space**: ~500 MB for the Whisper `small` model weights (downloaded automatically on first use).
- **Internet Access**: Required **only on the first run** to download the model from Hugging Face. After that, it runs completely offline.

---

## 🚀 Installation

### 🪟 Windows

#### 1. Install Python
1. Download Python from [python.org](https://www.python.org/downloads/).
2. During installation, make sure to check **"Add Python to PATH"**.

#### 2. Install FFmpeg
Choose **one** of the methods below:
- **Via Winget (Fastest)**:
  Open PowerShell or Command Prompt and run:
  ```powershell
  winget install Gyan.FFmpeg
  ```
- **Via Chocolatey**:
  ```powershell
  choco install ffmpeg
  ```
- **Manual**:
  Download the release build from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/), extract it, and add the `bin` folder to your Windows system `PATH`.

#### 3. Clone or Download this Project
Open PowerShell or Command Prompt:
```powershell
git clone https://github.com/<username>/transcripy.git
cd transcripy
```
*(Or download the ZIP, extract it, and navigate to the `transcripy` folder)*

#### 4. (Recommended) Set up a Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

#### 5. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 🐧 Linux (Ubuntu, Debian, Fedora, Arch)

#### 1. Install System Dependencies (Python, pip, venv, Tkinter, and FFmpeg)

- **Ubuntu / Debian / Mint**:
  ```bash
  sudo apt update
  sudo apt install -y python3 python3-pip python3-venv python3-tk ffmpeg git
  ```

- **Fedora / RHEL**:
  ```bash
  sudo dnf install -y python3 python3-pip python3-tkinter ffmpeg git
  ```

- **Arch Linux / Manjaro**:
  ```bash
  sudo pacman -S python python-pip tk ffmpeg git
  ```

#### 2. Clone or Navigate to the Project Directory
```bash
git clone https://github.com/<username>/transcripy.git
cd transcripy
```

#### 3. (Recommended) Set up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 💻 How to Run

1. Make sure your virtual environment is activated:
   - **Windows**: `venv\Scripts\activate`
   - **Linux**: `source venv/bin/activate`

2. Launch the application:
   - **Windows**:
     ```powershell
     python transcriPy.py
     ```
   - **Linux**:
     ```bash
     python3 transcriPy.py
     ```

3. **Usage Steps**:
   - Click **"Select Audio (MP3, WAV, M4A...)"**.
   - Choose your audio or video file in the file picker.
   - Wait while the audio is processed. The progress bar will indicate status and percentage.
   - Once completed, the full transcript will be saved to the same directory as the source audio file (named `[audio_file]_transcription.txt`).

---

## 🗑️ Uninstallation

If you wish to remove TranscriPy and its associated files from your system:

### 🪟 Windows

1. **Delete the Virtual Environment & Dependencies**:
   Open PowerShell in the `transcripy` directory:
   ```powershell
   deactivate  # if currently activated
   Remove-Item -Recurse -Force venv
   ```

2. **Delete Cached Whisper Models**:
   Whisper models downloaded by Hugging Face are stored in your user cache. To free up disk space (~500 MB):
   ```powershell
   Remove-Item -Recurse -Force "$env:USERPROFILE\.cache\huggingface\hub\models--Systran--faster-whisper-small"
   ```

3. **Delete Project Files**:
   Navigate out of the folder and remove the `transcripy` directory:
   ```powershell
   cd ..
   Remove-Item -Recurse -Force transcripy
   ```

4. **(Optional) Uninstall FFmpeg**:
   If installed via winget:
   ```powershell
   winget uninstall Gyan.FFmpeg
   ```

---

### 🐧 Linux

1. **Delete the Virtual Environment & Dependencies**:
   ```bash
   deactivate  # if currently activated
   rm -rf venv
   ```

2. **Delete Cached Whisper Models**:
   ```bash
   rm -rf ~/.cache/huggingface/hub/models--Systran--faster-whisper-small
   ```

3. **Delete Project Files**:
   Navigate out of the folder and remove the `transcripy` directory:
   ```bash
   cd ..
   rm -rf transcripy
   ```

4. **(Optional) Remove FFmpeg**:
   - **Ubuntu/Debian**:
     ```bash
     sudo apt remove --purge ffmpeg
     ```
   - **Fedora**:
     ```bash
     sudo dnf remove ffmpeg
     ```
   - **Arch**:
     ```bash
     sudo pacman -R ffmpeg
     ```

---

## ❓ Troubleshooting & FAQ

<details>
<summary><b>1. "FileNotFoundError" or error related to FFmpeg</b></summary>

Make sure FFmpeg is installed and accessible from your terminal:
```bash
ffmpeg -version
```
If this command fails:
- On **Windows**: Ensure the path containing `ffmpeg.exe` is added to your Environment Variables (`PATH`), and restart your terminal.
- On **Linux**: Install it with your package manager (`sudo apt install ffmpeg`).
</details>

<details>
<summary><b>2. "ModuleNotFoundError: No module named '_tkinter'" on Linux</b></summary>

Linux distributions often package Tkinter separately from Python. Install it via:
- Ubuntu/Debian: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch: `sudo pacman -S tk`
</details>

<details>
<summary><b>3. Why is the first transcription slower?</b></summary>

On the very first run, TranscriPy automatically downloads the Whisper `small` model (~460 MB) from Hugging Face. Subsequent runs will use the cached local model and start transcribing immediately without needing an internet connection.
</details>

<details>
<summary><b>4. Can I change the Whisper model size?</b></summary>

Yes! In `transcriPy.py`, look for:
```python
self.model = WhisperModel("small", device="cpu", compute_type="int8")
```
You can change `"small"` to `"tiny"`, `"base"`, `"medium"`, or `"large-v3"` depending on your hardware and accuracy needs.
</details>

---

## 📄 License

This project is open-source and free to use. Licensed under the [MIT License](https://opensource.org/licenses/MIT).
