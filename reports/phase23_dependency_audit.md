# Phase 23: Production Dependency Audit Report

> **Target**: Comprehensive mapping of runtime dependencies vs `requirements.txt`  
> **Python Environment Target**: Python 3.10+  
> **Date**: September 20, 2026

---

## 1. Executive Summary

A static and runtime dependency audit was conducted across the 33 active Python files in the repository. The audit revealed that while all 9 previously declared dependencies were legitimate, four critical packages required by the Phase 22 video renderer (`pillow`, `numpy`, `edge-tts`, `imageio-ffmpeg`) were missing from `requirements.txt`. 

`requirements.txt` has now been updated to include all essential production libraries.

---

## 2. Dependency Comparison Matrix

| Package | Status in `requirements.txt` | Active Importing Files | Functional Role | Category |
| :--- | :---: | :--- | :--- | :--- |
| **`python-dotenv`** | Declared | `config/settings.py`, `tools/llm_tool.py`, `main.py` | Environment variable management from `.env` | Active (Core) |
| **`pydantic`** | Declared | `config/settings.py`, `agents/*.py` | Schema validation, data contracts, and LLM structured outputs | Active (Core) |
| **`pydantic-settings`** | Declared | `config/settings.py` | Type-safe environment variable parsing | Active (Core) |
| **`openai`** | Declared | `tools/llm_tool.py` | Official SDK used to communicate with NousResearch Hermes on OpenRouter | Active (Agents) |
| **`requests`** | Declared | `tools/apify_tool.py`, `tools/ffmpeg_tool.py` | Direct HTTP requests for status probes and webhook calls | Active (Agents) |
| **`tavily-python`** | Declared | `tools/tavily_tool.py` | Web research for retail trading pain-points and market discussions | Active (Agents) |
| **`exa-py`** | Declared | `tools/exa_tool.py` | Neural semantic search for community sentiment | Active (Agents) |
| **`apify-client`** | Declared | `tools/apify_tool.py` | Meta Ad Library scraping client | Active (Agents) |
| **`rich`** | Declared | `main.py`, `agents/*.py` | Terminal dashboard, tables, status cards, and diagnostic output | Active (CLI) |
| **`pillow` (`PIL`)** | **ADDED** | `tools/vox_motion_engine.py`, `scripts/render_*.py`, `tools/visual_collision_guard.py` | **CRITICAL**: RGBA canvas creation, font rasterization, halftone dot matrix, image manipulation | Active (Video) |
| **`numpy`** | **ADDED** | `tools/vox_motion_engine.py` | **CRITICAL**: Coordinate arrays, projection transforms, procedural math | Active (Video) |
| **`edge-tts`** | **ADDED** | `tools/voice_tool.py` | **CRITICAL**: Microsoft Neural TTS (`en-US-ChristopherNeural`) broadcast voiceover | Active (Audio) |
| **`imageio-ffmpeg`** | **ADDED** | `tools/ffmpeg_tool.py` | Fallback discovery of FFmpeg binary on systems without system-wide FFmpeg PATH | Active (Video) |
| **`pyttsx3`** | **ADDED** | `tools/voice_tool.py` | Fully offline text-to-speech fallback if internet or neural API is unavailable | Active (Fallback) |

---

## 3. Dynamic & Subprocess Runtime Dependencies

The production pipeline also interacts with external binaries:

1. **`ffmpeg`** (System Binary):
   - Discovered automatically by `tools/ffmpeg_tool.py` via `shutil.which("ffmpeg")`, local paths, or `imageio-ffmpeg`.
   - Used for raw memory video encoding (`libx264`), audio stream extraction, audio filtering (`highpass`, `equalizer`, `loudnorm`), and multiplexing.
2. **`ffprobe`** (System Binary):
   - Used in `tools/ffmpeg_tool.py` to verify stream duration, codecs, sample rate, and pixel format.

---

## 4. Unused / Orphaned Dependencies Check

- **Declared Packages Unused by Codebase**: **0**.
  - Every single package in `requirements.txt` corresponds to active code imported by either the Hermes Multi-Agent CLI or the Phase 22 video renderer.
- **Packages Safely Omitted**:
  - `fal-client`: Used in early generative AI experiments (Phase 13); omitted because Phase 14–22 strictly committed to zero-cost local rendering.
  - `opencv-python`: Early video experiments; replaced by direct Pillow memory pipe to FFmpeg for significantly lower memory overhead and 100% color accuracy.
