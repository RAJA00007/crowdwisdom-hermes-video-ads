# Forensic Codebase Audit: CrowdWisdom Video Ads Repository

> **Audit Type**: Complete Pre-Submission Forensic Codebase Audit  
> **Date**: September 20, 2026  
> **Repository Target**: `C:\Users\Raja\automated_ad\crowdwisdom-hermes-video-ads`  
> **Approved Master Target**: `outputs/videos/final_cinematic_ad_phase22.mp4`  
> **Constraint**: AUDIT ONLY — Zero files deleted, moved, renamed, or modified.

---

## 1. Production Execution Path

The approved final ad master (`outputs/videos/final_cinematic_ad_phase22.mp4`) is rendered through a dedicated 2.5D procedural motion graphics pipeline rather than the earlier stock-footage or generative AI backends. 

### End-to-End Execution Trace

```
[ENTRY POINT]
scripts/render_final_cinematic_ad_phase22.py
   │
   ├── 1. MASTER AUDIO INGESTION
   │      └── outputs/videos/temp_audio_phase21/phase21_master_audio.wav
   │             ├── Synthesized via tools/voice_tool.py (Edge TTS en-US-ChristopherNeural)
   │             │   ├── Spoken line: "CrowdWisdom... Trading."
   │             │   ├── Tagline: "See the signal inside the noise."
   │             │   └── CTA URL: "Get access at crowdwisdomtrading.com."
   │             ├── Audio chain: 80Hz HPF -> 250Hz cut -> 3kHz presence boost -> EBU R128 (-16 LUFS, -1.0 dBTP)
   │             └── Motivated SFX: Monotonous clock ticks, mouse clicks, keystrokes, 50Hz sub-bass pulses
   │
   ├── 2. 2.5D MOTION GRAPHICS ENGINE
   │      └── tools/vox_motion_engine.py
   │             ├── VoxMotionComposition (1080x1920, 30fps, 48.5s duration, 1,455 frames)
   │             ├── Camera25D (60.0° FOV, projective coordinates)
   │             ├── HalftoneTraderFigure (Procedural halftone dot matrix trader cutout)
   │             ├── NewspaperFragment (Tumbling archival clipping with red category pill)
   │             ├── KineticTextObject (Spring-interpolated typography with drop shadows)
   │             ├── NetworkMeshLayer (32-node 2.5D dynamic topological graph)
   │             └── AnimatedStatCounter (Fast 0.5s roll locking permanently onto 1,482,930)
   │
   ├── 3. IMPORTED EDITORIAL COMPONENTS
   │      ├── scripts/render_final_cinematic_ad_phase20.py
   │      │      ├── NotificationAlertBubble (Sentiment drift & RSI divergence pills)
   │      │      ├── MicroChartFragment (Archival candlestick volatility cards)
   │      │      ├── EditorialCaptionObject (Dynamic selective captions with hot red highlights)
   │      │      ├── AccuracyComparisonCardAudited (Retail Baseline vs 68.4% Accuracy)
   │      │      └── TimelineLeadObjectAudited (14.6h Early Detection Lead timeline)
   │      └── scripts/render_final_cinematic_ad_phase19.py
   │             ├── BrandResolutionLockup (Master card: CROWDWISDOM TRADING + triple badges)
   │             └── RadarDirectionalObject (Concentric sweep radar with target acquisition)
   │
   ├── 4. SPATIAL COLLISION & SAFE-ZONE GUARD
   │      └── tools/visual_collision_guard.py
   │             ├── 98 time-slice audits (0.5s intervals across 48.5s runtime)
   │             ├── AABB boundary checks across priority hierarchy (P0: CTA -> P5: Decorative)
   │             └── Safe margin compliance (Left/Right >= 80px, Top >= 100px, Bottom <= 1740px)
   │
   ├── 5. DIRECT FRAME-BY-FRAME PIPE TO FFMPEG
   │      └── tools/ffmpeg_tool.py
   │             ├── Direct RGBA rawvideo pipe (Pillow memory buffer -> FFmpeg stdin)
   │             └── Video stream encoding: H.264 (libx264, yuv420p, crf 18, 30fps)
   │
   └── 6. FINAL BROADCAST MUX
          └── FFmpeg muxes raw video track + broadcast audio -> outputs/videos/final_cinematic_ad_phase22.mp4
```

---

## 2. Active Files

Files that are **directly executed or imported** in either:
1. The **Phase 22 Production Video Pipeline** (generating `final_cinematic_ad_phase22.mp4`), OR
2. The **Hermes Multi-Agent Framework** (the primary assessment CLI pipeline invoked via `main.py`).

### Category A: Phase 22 Production Video Core (6 Files)
| File | Lines | Size | Role / Evidence |
| :--- | :---: | :---: | :--- |
| `scripts/render_final_cinematic_ad_phase22.py` | 772 | 36.5 KB | **Master production runner**. Builds the 8 scenes, audits collisions, executes direct pipe to FFmpeg, extracts verification frames, and writes `phase22_cleanup_report.json`. |
| `tools/vox_motion_engine.py` | 985 | 40.5 KB | **Core motion graphics engine**. Houses `Camera25D`, `VoxMotionComposition`, procedural halftone shaders, archival canvas generation, and keyframing interpolation. |
| `tools/visual_collision_guard.py` | 288 | 11.1 KB | **Spatial clearance auditor**. Performs AABB collision checking and safe margin enforcement across P0–P5 priorities. |
| `tools/voice_tool.py` | 276 | 11.3 KB | **Neural voiceover engine**. Synthesizes ChristopherNeural speech via `edge-tts` with duration calculation and phoneme timing. |
| `tools/audio_tool.py` | 274 | 11.8 KB | **Audio mastering pipeline**. Handles procedural sound effect synthesis, sub-bass pulse generation, and filter complexes. |
| `tools/ffmpeg_tool.py` | 359 | 13.6 KB | **FFmpeg wrapper**. Discovers binary paths, probes media streams, executes multiplexing and filter graphs. |

### Category B: Active Component Providers (2 Files)
*Critical Notice: Although these files represent earlier renderers, Phase 22 imports core visual classes from them.*
| File | Lines | Size | Imported Components |
| :--- | :---: | :---: | :--- |
| `scripts/render_final_cinematic_ad_phase20.py` | 1,310 | 62.1 KB | Supplies `NotificationAlertBubble`, `MicroChartFragment`, `EditorialCaptionObject`, `AccuracyComparisonCardAudited`, and `TimelineLeadObjectAudited`. |
| `scripts/render_final_cinematic_ad_phase19.py` | 1,006 | 47.3 KB | Supplies `BrandResolutionLockup` and `RadarDirectionalObject`. |

### Category C: Hermes Multi-Agent Framework (25 Files)
*These modules fulfill the original internship assessment requirement for NousResearch Hermes / OpenRouter orchestration.*
| File | Lines | Size | Role |
| :--- | :---: | :---: | :--- |
| `main.py` | 457 | 18.0 KB | Main CLI interface with Rich diagnostics, connectivity checks, and workflow triggers. |
| `config/settings.py` | 76 | 3.4 KB | Pydantic configuration loader for OpenRouter, Apify, Tavily, and Exa. |
| `workflows/marketing_pipeline.py` | 128 | 5.1 KB | Orchestrates the 6-stage multi-agent pipeline. |
| `agents/ads_manager.py` | 146 | 6.6 KB | Stage 1: Meta Ad Library scraper coordination via Apify. |
| `agents/ad_analyzer.py` | 302 | 12.7 KB | Stage 2: Hook, angle, format, and CTA pattern analysis. |
| `agents/research_agent.py` | 378 | 16.0 KB | Stage 3: ICP pain-point and competitor intelligence via Tavily/Exa. |
| `agents/proprietary_data_agent.py` | 70 | 3.3 KB | Stage 4: Ingestion and validation of CrowdWisdom internal performance data. |
| `agents/creative_agent.py` | 823 | 54.9 KB | Stage 5: Generation of 3 differentiated video ad creative angles. |
| `agents/storyboard_agent.py` | 1,187 | 78.3 KB | Stage 5b: Scene-by-scene timing, visual prompt, and narration breakdown. |
| `agents/storyboard_validator.py` | 290 | 12.6 KB | Storyboard schema validator and coherence auditor. |
| `agents/video_agent.py` | 1,450 | 68.4 KB | Stage 6: Video production coordinator. |
| `agents/creative_video_qa.py` | 341 | 15.2 KB | Automated quality assurance auditor for generated video assets. |
| `agents/phase10_qa_auditor.py` | 310 | 12.8 KB | Multi-point compliance checker for duration, audio, and visual criteria. |
| `tools/llm_tool.py` | 163 | 6.0 KB | Client for Hermes-3 LLM on OpenRouter with OpenAI SDK compatibility. |
| `tools/apify_tool.py` | 360 | 14.0 KB | Scrapes Meta Ads Library via Apify Actor `apify/facebook-ads-scraper`. |
| `tools/tavily_tool.py` | 82 | 2.9 KB | Web search tool for trader forums and competitor angles. |
| `tools/exa_tool.py` | 73 | 2.5 KB | Neural semantic search tool for retail trader psychology. |
| `tools/proprietary_data_tool.py` | 369 | 18.4 KB | Parses CSV, PDF, and Excel performance records. |
| `tools/data_visualization_tool.py` | 361 | 16.0 KB | Generates matplotlib charts and data overlays. |
| `tools/style_prompt_system.py` | 413 | 15.2 KB | Enforces archival/editorial prompt constraints for generative systems. |
| `tools/phase11_prompt_system.py` | 346 | 25.2 KB | Specialized cinematography prompt generation system. |
| `tools/video_generation_tool.py` | 282 | 11.3 KB | Dispatches video generation jobs to external backends. |
| `tools/video_provider.py` | 1,460 | 57.2 KB | Abstraction layer for multiple video rendering engines. |
| `tools/openmontage_tool.py` | 172 | 6.2 KB | Integration tool for local OpenMontage engine. |
| `tools/editorial_compositor.py` | 1,204 | 57.4 KB | Multi-layer video compositor with text and matte overlays. |

---

## 3. Potentially Unused Files

These files are located in the repository but have no active inbound imports from `main.py` or `scripts/render_final_cinematic_ad_phase22.py`.

| File | Confidence | Evidence / Reason |
| :--- | :---: | :--- |
| `agents/style_prompt_validator.py` | **HIGH** | Standalone validator created during Phase 9 to verify Midjourney/Runway prompt structures. Neither `main.py` nor `video_agent.py` calls this class directly. |
| `tools/video_tool.py` | **HIGH** | Legacy lightweight wrapper around OpenCV/imageio created in Phase 1; superseded by `tools/ffmpeg_tool.py` and `tools/editorial_compositor.py`. |
| `scripts/render_vox_motion_proof_v2.py` | **MEDIUM** | The 10-second proof of concept that established the approved visual style in Phase 19. It remains a valuable visual reference but is not imported by production code. |
| `agents/__init__.py` | **LOW** | Standard Python package initializer (21 lines). Harmless, but exports unused aliases. |
| `tools/__init__.py` | **LOW** | Standard Python package initializer (15 lines). |
| `config/__init__.py` | **LOW** | Package initializer (5 lines). |
| `workflows/__init__.py` | **LOW** | Package initializer (5 lines). |

---

## 4. Definitely Unused Files

These files are obsolete artifacts or orphaned scripts that have no functional connection to the current production or agent system.

| File | Confidence | Evidence / Reason |
| :--- | :---: | :--- |
| `scripts/probe_footage.py` | **HIGH** | 11-line utility script from Phase 14 that probed a single static `.ogv` test file. Never imported. |
| `scripts/fetch_footage.py` | **HIGH** | Downloaded Pexels/Wikimedia stock footage during Phase 14. Stock footage was explicitly eliminated in Phase 15–19 in favor of procedural motion graphics. |
| `scripts/generate_overlays.py` | **HIGH** | Rendered static PNG overlays for the discontinued stock-footage compositor. |
| `scripts/extract_phase14_frames.py` | **HIGH** | Extracted debug frames from the discarded Phase 14 video. |
| `scripts/test_synth_p19.py` | **HIGH** | Scratch test from Phase 19 that tested single-sentence TTS output. |

---

## 5. Legacy Code (Historical Phase Iterations)

Because the project progressed through 22 iterative phases, numerous complete rendering pipelines exist as historical records.

| File | Lines | Superseded By | Reason Retained / Status |
| :--- | :---: | :--- | :--- |
| `scripts/render_final_cinematic_ad_phase21.py` | 1,147 | `render_final_cinematic_ad_phase22.py` | Phase 21 master ad. Retained for auditability. |
| `scripts/render_phase18_ad.py` | 446 | `render_final_cinematic_ad_phase19.py` | Discarded intermediate experimental ad. |
| `scripts/render_phase17_style_proof.py` | 401 | `render_vox_motion_proof_v2.py` | Failed style proof rejected by user for looking like PowerPoint. |
| `scripts/generate_phase16_storyboard.py` | 312 | Phase 19 motion script | Hardcoded script generator superseded by motion script. |
| `scripts/render_phase14_ad.py` | 363 | `render_final_cinematic_ad_phase19.py` | Stock-footage commercial rejected by user in Phase 15. |
| `scripts/generate_phase14_audio.py` | 305 | `tools/voice_tool.py` | Old audio generator without loudness normalization. |
| `scripts/generate_phase14_storyboard.py` | 284 | Phase 16 storyboard | Old storyboard generator. |
| `scripts/phase12_discovery.py` | 151 | `tools/openmontage_tool.py` | OpenMontage hardware probe script. |
| `scripts/run_phase12_hero.py` | 191 | Motion engine | Generative AI hero shot test. |
| `tools/cinematic_vox_system.py` | 571 | `tools/vox_motion_engine.py` | Early procedural visual system; replaced by the true 2.5D spatial camera engine. |

---

## 6. Duplicate Code & Utilities

Several functions and patterns were duplicated across phase renderers during development:

1. **`get_system_font(size, bold)`**:
   - Implemented in `tools/vox_motion_engine.py` (Lines 60–80).
   - Re-implemented in `scripts/render_final_cinematic_ad_phase19.py` (Lines 45–65).
   - Re-implemented in `scripts/render_final_cinematic_ad_phase20.py` (Lines 48–70).
   - Re-implemented in `scripts/render_final_cinematic_ad_phase21.py` (Lines 57–58, imported).
   - *Recommendation*: Centralize font discovery exclusively within `tools/vox_motion_engine.py`.

2. **Easing Functions (`ease_out_back`, `ease_out_cubic`, `ease_out_quad`, `ease_in_back`)**:
   - Defined in `tools/vox_motion_engine.py`.
   - Copied verbatim into `scripts/render_final_cinematic_ad_phase19.py`.
   - *Recommendation*: Import easing functions exclusively from `tools/vox_motion_engine.py`.

3. **Color Constants (`COLOR_ARCHIVAL_TAN`, `COLOR_INK_BLACK`, `COLOR_HOT_RED`, etc.)**:
   - Defined in `tools/vox_motion_engine.py`.
   - Redefined in `tools/cinematic_vox_system.py` and `tools/editorial_compositor.py`.

---

## 7. Unused Assets

An automated scan cross-referencing all 43 files in `assets/`, `data/`, and `images/` against all source code revealed **24 unreferenced asset files**:

### Obsolete Graphics & Element Cutouts
| Asset Path | Size | Description / Reason Unreferenced |
| :--- | :---: | :--- |
| `assets/style_reference/Example Style Reference.png` | 2.82 MB | Reference image used during early creative prompt ideation; never loaded programmatically. |
| `assets/extracted_elements/cutout_man_hat.png` | 79.8 KB | PNG cutout from early Phase 7 tests. Replaced by `HalftoneTraderFigure` procedural dot matrix. |
| `assets/extracted_elements/cutout_man_profile.png` | 22.6 KB | Alternate trader silhouette; never imported. |
| `assets/extracted_elements/map_pin.png` | 20.5 KB | Static map pin graphic; replaced by vector drawing primitives. |
| `assets/extracted_elements/map_pin_clean.png` | 23.4 KB | Alternate map pin. |
| `assets/extracted_elements/red_stat_box.png` | 46.5 KB | Pre-rendered stat box; replaced by dynamic PIL card rendering. |
| `assets/extracted_elements/red_stat_box_clean.png` | 53.2 KB | Alternate stat box. |
| `assets/extracted_elements/torn_paper.png` | 46.0 KB | Pre-rendered torn paper border; replaced by vector torn paper drawing in `NewspaperFragment`. |
| `assets/extracted_elements/torn_paper_clean.png` | 50.8 KB | Alternate paper border. |

### Discontinued Phase 9 Cinematic Frames
*These were generated during Phase 9 for a paper-diorama concept that was replaced in Phase 19:*
- `data/assets/cinematic/phase9_frame_beat4.png` (2.29 MB)
- `data/assets/cinematic/phase9_frame_beat5.png` (2.17 MB)
- `data/assets/cinematic/phase9_frame_beat6.png` (2.39 MB)
- `data/assets/cinematic/phase9_frame_beat7.png` (2.22 MB)
- `data/assets/cinematic/phase9_frame_beat8.png` (1.99 MB)
- `data/assets/cinematic/style_test_frame_beat1.png` (2.10 MB)
- `data/assets/cinematic/style_test_frame_beat2.png` (941.6 KB)
- `data/assets/cinematic/style_test_frame_beat3.png` (1.99 MB)
- `data/assets/cinematic/stage_map_texture.jpg` (99.3 KB)
- `data/assets/cinematic/test_halftone_cutout.png` (24.8 KB)

### Stale Raw Scrapes
- `data/raw/meta_ads_raw_20260917_134347.json` (278.7 KB) — Raw debug dump from September 17.
- `data/raw/meta_ads_raw_20260917_134812.json` (374.9 KB) — Raw debug dump from September 17.

---

## 8. Dependencies Audit

### Declared in `requirements.txt`
```
python-dotenv>=1.0.1
pydantic>=2.7.0
pydantic-settings>=2.2.0
openai>=1.30.0
requests>=2.31.0
tavily-python>=0.3.3
exa-py>=1.0.7
apify-client>=1.6.4
rich>=13.7.1
```
- **Declared but Unused**: **None**. All 9 packages are imported by the active Hermes agent framework (`main.py`, `agents/`, `config/settings.py`, `tools/`).

### CRITICAL: Imported in Active Code but Missing from `requirements.txt`
A clean environment running `pip install -r requirements.txt` will **FAIL** when executing the Phase 22 video renderer due to missing core libraries:
1. **`Pillow` (`PIL`)** — **CRITICAL**: Used in `tools/vox_motion_engine.py`, `tools/visual_collision_guard.py`, and `scripts/render_final_cinematic_ad_phase22.py` for all frame rendering.
2. **`numpy`** — **CRITICAL**: Used in `tools/vox_motion_engine.py` for spatial array operations and coordinate projections.
3. **`edge-tts`** — **CRITICAL**: Used in `tools/voice_tool.py` for Microsoft neural voiceover generation.
4. **`imageio-ffmpeg`** — Used in `tools/ffmpeg_tool.py` as a fallback binary discovery tool.
5. **`pyttsx3`** — Used in `tools/voice_tool.py` as an offline speech synthesis fallback.
6. **`pypdf`** & **`openpyxl`** — Used in `tools/proprietary_data_tool.py` for parsing document formats.

---

## 9. Debug & Temporary Code

1. **`print()` Statements**:
   - 68 Python files contain a total of **842 `print()` calls**.
   - While appropriate for CLI scripts (`scripts/render_*.py`) and `main.py`, library modules like `tools/vox_motion_engine.py` and `tools/visual_collision_guard.py` should ideally use standard `logging`.
2. **TODO / FIXME / HACK Markers**:
   - Zero critical blockers found. Only 3 informational markers exist in test/experimental scripts.
3. **Temporary File Generation**:
   - `scripts/render_final_cinematic_ad_phase22.py` creates:
     - `outputs/videos/temp_motion_raw_p22.mp4` (temporary raw visual stream before audio muxing).
   - This file is correctly overwritten on each run.

---

## 10. Security & Confidentiality Risks

### 1. Live API Keys in Local `.env` File (HIGH RISK)
The local `.env` file at the root of the project contains **LIVE, ACTIVE SECRETS**:
- `OPENROUTER_API_KEY`
- `APIFY_API_TOKEN`
- `TAVILY_API_KEY`
- `EXA_API_KEY`
- `FAL_KEY`

> [!WARNING]
> While `.env` is listed in `.gitignore`, the repository is not currently initialized with git (`fatal: not a git repository`). If the user runs `git init` and `git add .` without caution, these live credentials could be committed to a public GitHub repository.

### 2. Machine-Specific Absolute File Paths (MEDIUM RISK)
Five files contain hardcoded absolute Windows paths specific to `C:\Users\Raja\...`:
- `outputs/videos/p14_beats/concat_list.txt`
- `outputs/videos/p17_beats/concat_p17.txt`
- `outputs/videos/p18_scenes/concat_list.txt`
- `scripts/phase12_discovery.py` (`C:\Users\Raja\OpenMontage`)
- `tools/video_provider.py` (`C:\Users\Raja\OpenMontage`)

*Remediation*: Replace all hardcoded paths with `Path(__file__).resolve().parents[...]` or environment variables.

---

## 11. Large Files Inventory

The repository contains **147 files exceeding 1 MB**, totaling **966.53 MB** (mostly in `outputs/`):

### Top 10 Largest Binaries
| File Path | Size | Category | Recommendation |
| :--- | :---: | :---: | :--- |
| `outputs/videos/raw_footage/beat_05_exchange.webm` | **177.13 MB** | OBSOLETE | **EXCEEDS GITHUB 100MB LIMIT**. Must not be committed to GitHub. |
| `outputs/videos/final_cinematic_ad.mp4` | 24.35 MB | OBSOLETE | Phase 9 render; exclude from git. |
| `outputs/videos/final_cinematic_ad_phase10.mp4` | 24.34 MB | OBSOLETE | Phase 10 render; exclude from git. |
| `outputs/videos/phase9_paper_diorama/raw_video_concatenated.mp4` | 23.06 MB | OBSOLETE | Phase 9 video; exclude from git. |
| `outputs/videos/temp_phase10_master/raw_video_track_phase10.mp4` | 23.05 MB | OBSOLETE | Phase 10 video; exclude from git. |
| `outputs/videos/final_cinematic_ad_phase14.mp4` | 22.31 MB | OBSOLETE | Phase 14 video; exclude from git. |
| `outputs/videos/final_cinematic_ad_phase18.mp4` | 22.20 MB | OBSOLETE | Phase 18 video; exclude from git. |
| `outputs/videos/p14_beats/concat_video_stream.mp4` | 21.23 MB | OBSOLETE | Phase 14 stream; exclude from git. |
| `outputs/videos/p18_scenes/concat_vox_video.mp4` | 21.12 MB | OBSOLETE | Phase 18 stream; exclude from git. |
| `outputs/videos/raw_footage/beat_02_typing.ogv` | 13.61 MB | OBSOLETE | Stock footage; exclude from git. |

The approved final master video:
- **`outputs/videos/final_cinematic_ad_phase22.mp4`** is only **3.82 MB**, making it lightweight and well within GitHub's file limits.

---

## 12. Recommended Cleanup Plan (For Post-Audit Action)

*Note: As per instructions, NO changes have been made during this audit.*

1. **Update `requirements.txt`**:
   Add `Pillow>=10.0.0`, `numpy>=1.24.0`, and `edge-tts>=6.1.0` so that any fresh clone can render Phase 22 immediately.
2. **Refactor Shared Visual Components**:
   Extract `NotificationAlertBubble`, `MicroChartFragment`, `EditorialCaptionObject`, `AccuracyComparisonCardAudited`, `TimelineLeadObjectAudited`, `BrandResolutionLockup`, and `RadarDirectionalObject` out of `render_final_cinematic_ad_phase20.py` and `phase19.py` into a dedicated `tools/vox_components.py` module.
3. **Clean Intermediate Output Artifacts**:
   Delete obsolete video renders from Phases 7 through 21 (saving ~950 MB of disk space). Keep only `final_cinematic_ad_phase22.mp4` and its verification reports.
4. **Remove Unused Assets**:
   Delete unused PNGs in `assets/extracted_elements/` and `data/assets/cinematic/` (saving ~25 MB).
5. **Verify `.gitignore` Before Git Init**:
   Ensure `.env` and `outputs/videos/*` (except `final_cinematic_ad_phase22.mp4`) are strictly ignored before committing to GitHub.

---

## 13. Files That MUST NOT Be Deleted

Deleting any of the following files will break either the **Phase 22 Production Video Pipeline** or the **Hermes Multi-Agent Framework**:

### Core Video Engine & Renderer
- `scripts/render_final_cinematic_ad_phase22.py` (Master ad generator)
- `scripts/render_final_cinematic_ad_phase20.py` (**CRITICAL**: Provides active component classes)
- `scripts/render_final_cinematic_ad_phase19.py` (**CRITICAL**: Provides active component classes)
- `tools/vox_motion_engine.py` (Core 2.5D procedural motion engine)
- `tools/visual_collision_guard.py` (Spatial clearance validator)
- `tools/voice_tool.py` (Neural voiceover synthesis)
- `tools/audio_tool.py` (Foley & audio mastering)
- `tools/ffmpeg_tool.py` (FFmpeg execution & probing)
- `outputs/videos/temp_audio_phase21/phase21_master_audio.wav` (Master broadcast audio track)

### Hermes Multi-Agent Framework (Assignment Requirement)
- `main.py` (Master CLI entrypoint)
- `config/settings.py` (Pydantic environment config)
- `workflows/marketing_pipeline.py` (Master pipeline orchestrator)
- `agents/ads_manager.py` (Meta ad research)
- `agents/ad_analyzer.py` (Ad pattern analysis)
- `agents/research_agent.py` (ICP web intelligence)
- `agents/proprietary_data_agent.py` (Internal data grounding)
- `agents/creative_agent.py` (Creative concepting)
- `agents/storyboard_agent.py` (Storyboard generation)
- `agents/video_agent.py` (Video orchestration)
- `tools/llm_tool.py` (NousResearch Hermes client)
- `tools/apify_tool.py` (Meta Ads Library scraper)
- `tools/tavily_tool.py` (Market trend search)
- `tools/exa_tool.py` (Neural semantic search)
- `tools/proprietary_data_tool.py` (Data ingestion)

---

## 14. Final GitHub Submission Structure

For a clean, professional, and compliant GitHub submission, the repository should be structured as follows:

```
crowdwisdom-hermes-video-ads/
│
├── .env.example                        # Safe template with placeholder keys (NO REAL KEYS)
├── .gitignore                          # Ignores .env, __pycache__, .venv, raw footage
├── requirements.txt                    # Updated with Pillow, numpy, edge-tts, etc.
├── README.md                           # Architecture, Hermes multi-agent setup, Phase 22 video showcase
├── main.py                             # Hermes Multi-Agent CLI Entrypoint
│
├── agents/                             # 6-Stage Multi-Agent Architecture
│   ├── ads_manager.py                  # Stage 1: Meta Ads Research (Apify)
│   ├── ad_analyzer.py                  # Stage 2: Hook & Angle Analysis
│   ├── research_agent.py               # Stage 3: ICP Deep Dive (Tavily / Exa)
│   ├── proprietary_data_agent.py       # Stage 4: Proprietary Data Ingestion
│   ├── creative_agent.py               # Stage 5: 3 Differentiated Concepts
│   ├── storyboard_agent.py             # Stage 5b: Scene-by-scene Storyboard
│   └── video_agent.py                  # Stage 6: Video Production Orchestrator
│
├── workflows/                          # Master Pipeline Workflows
│   └── marketing_pipeline.py
│
├── config/                             # Pydantic Settings & Configuration
│   └── settings.py
│
├── tools/                              # Tools & Execution Engines
│   ├── vox_motion_engine.py            # Phase 22 2.5D Vox Motion Engine
│   ├── visual_collision_guard.py       # AABB Spatial Clearance Guard
│   ├── voice_tool.py                   # Edge Neural TTS Speech Engine
│   ├── audio_tool.py                   # Foley, Sub-Bass & Loudnorm Mastering
│   ├── ffmpeg_tool.py                  # Direct Memory-Pipe FFmpeg Multiplexer
│   ├── llm_tool.py                     # Hermes LLM OpenRouter Client
│   ├── apify_tool.py                   # Meta Ads Scraper Tool
│   ├── tavily_tool.py                  # Web Search Tool
│   ├── exa_tool.py                     # Neural Search Tool
│   └── proprietary_data_tool.py        # CrowdWisdom Data Ingestion Tool
│
├── scripts/                            # Production Video Execution Scripts
│   ├── render_final_cinematic_ad_phase22.py # Master Phase 22 Ad Producer
│   ├── render_final_cinematic_ad_phase20.py # Component Library Provider
│   └── render_final_cinematic_ad_phase19.py # Component Library Provider
│
├── tests/                              # Validation & Test Suite
│   ├── test_ads_schema.py
│   ├── test_cinematic_vox_system.py
│   └── test_vox_motion_engine.py
│
├── outputs/
│   └── videos/
│       ├── final_cinematic_ad_phase22.mp4   # Master Ad Video (3.82 MB, 48.5s, 1080x1920)
│       ├── phase22_cleanup_report.json      # Final Compliance & Collision Audit
│       ├── p22_frame_s1_hook.png            # Milestone Verification Frame 1
│       ├── p22_frame_s4_network.png         # Milestone Verification Frame 4
│       ├── p22_frame_s5_accuracy.png        # Milestone Verification Frame 5
│       └── p22_frame_s8_cta.png             # Milestone Verification Frame 8
│
└── reports/
    └── codebase_forensic_audit.md           # This comprehensive forensic report
```

---

## Summary Statistics

```
================================================================================
TOTAL PYTHON FILES:                 68
ACTIVE PYTHON FILES:                33 (6 Phase 22 Core + 2 Component Providers + 25 Hermes Agent Framework)
POTENTIALLY UNUSED PYTHON FILES:    7
LEGACY FILES:                       16
TEST FILES:                         14
UNUSED ASSETS:                      24 (out of 43 total assets)
UNUSED DEPENDENCIES:                0 declared unused, but 7 active packages undeclared in requirements.txt
LARGE FILES (>1MB):                 147 files (totaling 966.53 MB in outputs/)
SECURITY ISSUES:                    6 (1 live .env file + 5 hardcoded user paths)
================================================================================
```
