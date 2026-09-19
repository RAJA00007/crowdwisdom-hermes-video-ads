# Troubleshooting Guide — CrowdWisdom Hermes AI Video Advertising System

This guide addresses symptoms, root causes, and solutions for common issues encountered during environment setup, agent execution, and video rendering.

---

## Issue Matrix

### 1. `FFmpeg not found or executable missing`
- **Symptom:**
  ```
  FileNotFoundError: [WinError 2] The system cannot find the file specified: 'ffmpeg'
  ```
  or rendering fails with `FFmpegTool: FFmpeg executable not located on PATH`.
- **Root Cause:** FFmpeg is not installed, or its `bin` directory is not added to the system `PATH` environment variable.
- **Solution:**
  1. **Windows:** Install via winget:
     ```powershell
     winget install Gyan.FFmpeg
     ```
     Or manually download from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/), extract to `C:\ffmpeg`, and add `C:\ffmpeg\bin` to your system `PATH`. Restart your terminal.
  2. **Linux:** Run `sudo apt update && sudo apt install ffmpeg`.
  3. **macOS:** Run `brew install ffmpeg`.
  4. Test availability by typing `ffmpeg -version`.

---

### 2. `Python Version Incompatibility`
- **Symptom:**
  ```
  SyntaxError or ModuleNotFoundError in standard library typing
  ```
- **Root Cause:** Running an unsupported Python version (e.g., Python < 3.10).
- **Solution:**
  Verify Python version:
  ```bash
  python --version
  ```
  Ensure Python 3.10.x or 3.11.x is active in your virtual environment. Recreate the environment if necessary:
  ```bash
  py -3.10 -m venv .venv
  .\.venv\Scripts\activate
  pip install -r requirements.txt
  ```

---

### 3. `Missing API Key / Hermes LLM Pending Config`
- **Symptom:**
  `python main.py --test-hermes` displays `[PENDING CONFIG] Hermes LLM Not Connected`.
- **Root Cause:** `.env` file does not exist, or `OPENROUTER_API_KEY` is empty.
- **Solution:**
  1. Ensure you have copied `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
  2. Add your active OpenRouter key:
     ```env
     OPENROUTER_API_KEY=sk-or-v1-...
     ```
  3. Run `python main.py --status` to confirm status changes to `[OK] Configured`.
  4. *Note:* If you only wish to render the video, you do not need an OpenRouter key. Run `python scripts/render_final_cinematic_ad_phase22.py` directly.

---

### 4. `Edge-TTS Connection / Rate Limit Fallback`
- **Symptom:**
  Voice generation displays a warning or falls back to standard pyttsx3 speech.
- **Root Cause:** Network connectivity interruption or firewall blocking Microsoft Edge-TTS websocket servers.
- **Solution:**
  The `VoiceTool` (`tools/voice_tool.py`) automatically implements a graceful fallback hierarchy:
  1. Primary: High-fidelity Microsoft Neural TTS via `edge-tts` (`en-US-ChristopherNeural` / `en-US-GuyNeural`).
  2. Secondary: Offline OS-level SAPI5/espeak speech synthesizer via `pyttsx3`.
  If you are running in an offline or air-gapped environment, the system automatically switches to local synthesis without throwing fatal exceptions.

---

### 5. `Windows Path Backslash Escaping Issues`
- **Symptom:**
  ```
  OSError: [Errno 22] Invalid argument: 'C:\\Users\\...\\raw_footage\x08eat_05.webm'
  ```
- **Root Cause:** Unescaped backslashes in hardcoded Windows paths (e.g., `\b` being interpreted as an ASCII backspace character).
- **Solution:**
  Always use `pathlib.Path` or forward slashes in configuration files and scripts:
  ```python
  from pathlib import Path
  video_dir = Path("outputs") / "videos"
  ```
  All production scripts in this repository have been audited and updated to machine-independent `Path` constructs.

---

### 6. `VisualCollisionGuard Bounding-Box Margin Warning`
- **Symptom:**
  Console outputs `[COLLISION GUARD] Warning: Label and chart bounding boxes overlap by 14px`.
- **Root Cause:** Custom text string or subtitle was added with a font size exceeding the safe area bounding box.
- **Solution:**
  The collision engine (`tools/visual_collision_guard.py`) uses axis-aligned bounding boxes (AABB) with safety margins. If customizing scenes, adjust element `y` offsets or reduce font size to keep at least 20px padding between adjacent kinetic text cards. In the approved Phase 22 master script, all collision checks are 100% compliant.

---

### 7. `Pillow / PIL Deprecation Warning`
- **Symptom:**
  ```
  DeprecationWarning: Image.Image.getdata is deprecated and will be removed in Pillow 14. Use get_flattened_data instead.
  ```
- **Root Cause:** Pillow version 10+ deprecating older alpha extraction methods.
- **Solution:**
  This is a non-fatal warning from Pillow internal methods. Rendering continues and completes without disruption.
