# Quickstart Guide — CrowdWisdom Hermes AI Video Advertising System

Get up and running with the CrowdWisdom Hermes Video Advertising System in under 5 minutes.

---

## 1. Clone Repository

```bash
git clone <REPOSITORY_URL>
cd crowdwisdom-hermes-video-ads
```

---

## 2. Create and Activate Virtual Environment

### Windows (PowerShell / Command Prompt):
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies & FFmpeg

```bash
pip install -r requirements.txt
```

Ensure **FFmpeg** is installed and accessible on your system `PATH`:
- **Windows:** Download from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) or install via `winget install Gyan.FFmpeg` / `choco install ffmpeg`.
- **Linux:** `sudo apt-get install ffmpeg`
- **macOS:** `brew install ffmpeg`

Verify FFmpeg availability:
```bash
ffmpeg -version
```

---

## 4. Configure Environment (Optional for Local Demo)

Copy the configuration template:
```bash
cp .env.example .env
```

If you plan to run live multi-agent research stages, add your API keys to `.env`:
```env
OPENROUTER_API_KEY=your_openrouter_key
APIFY_API_TOKEN=your_apify_token
TAVILY_API_KEY=your_tavily_key
EXA_API_KEY=your_exa_key
```

> **Note:** Rendering the approved cinematic broadcast video ad is **100% local** and does **not** require any paid API keys!

---

## 5. Run Diagnostic Checks

Verify that your environment, dependencies, and agents are properly initialized:
```bash
# Verify environment readiness
python main.py --status

# View the Hermes multi-agent roster and Kanban pipeline
python main.py --pipeline

# Run core engine verification tests
python tests/test_vox_motion_engine.py
```

---

## 6. Render the Approved Final Ad (Instant Reproducibility)

To render the official 48.5-second Phase 22 cinematic broadcast master advertisement:

```bash
python scripts/render_final_cinematic_ad_phase22.py
```

---

## 7. Locate Output Deliverables

Upon completion, your finished video ad and quality audit report will be located at:
- **Master Video File:** `outputs/videos/final_cinematic_ad_phase22.mp4` (1080x1920 vertical, 30 fps, H.264/AAC)
- **Production Report:** `outputs/videos/phase22_cleanup_report.json`
- **Keyframe Previews:** `outputs/videos/p22_frame_*.png`

For full architectural details and multi-agent workflows, refer to [`docs/ARCHITECTURE.md`](ARCHITECTURE.md) and [`README.md`](../README.md).
