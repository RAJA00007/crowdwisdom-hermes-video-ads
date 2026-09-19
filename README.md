# CrowdWisdom Hermes — AI Video Advertising System

An intelligent, multi-agent AI video advertising platform engineered for **CrowdWisdomTrading**. The system combines the **Hermes-3 multi-agent framework** for market research, competitor ad dissection, and ICP psychological grounding with a **procedural 2.5D Vox-inspired cinematic motion engine** to generate broadcast-quality vertical video advertisements (1080x1920, 9:16) grounded in verified financial consensus data.

---

## Overview

### What the Project Does
The CrowdWisdom Hermes system automates the complete lifecycle of quantitative financial advertising:
1. **Competitive Ad Intelligence:** Automatically scrapes and dissects active Meta Ad Library campaigns in the trading, fintech, and algorithmic intelligence spaces.
2. **ICP & Behavioral Grounding:** Uses web and neural community search to extract retail trader pain points, emotional triggers, and prevailing market narratives.
3. **Proprietary Data Ingestion:** Grounds all marketing claims in verified CrowdWisdomTrading platform metrics (1.48M+ predictions, 68.4% directional accuracy, 48-hour institutional signal lead time).
4. **Cinematic Storyboarding:** Automatically writes screenplay-grade voiceover scripts and structured multi-scene storyboards.
5. **Procedural Motion Graphics Rendering:** Renders 1080x1920 broadcast video ads using a local 2.5D visual journalism motion engine with kinetic typography, halftone cutouts, and dynamic data visualization—without relying on costly or unreliable external generative video APIs.

### The Problem It Solves
Retail traders face immense sensory and informational overload—navigating thousands of noisy social alerts, conflicting analyst commentary, and lagging financial headlines. Typical financial advertising relies on generic stock footage or repetitive PowerPoint-style slide decks that fail to capture attention. This system solves both problems: it speaks directly to the trader's acute psychological pain point ("drowning in noise") and delivers the solution through sophisticated, authoritative visual journalism.

### What Makes the System Different
- **Hermes Multi-Agent Orchestration:** Specialized agents execute distinct roles (scraping, creative analysis, web search, data verification, cinematography) structured around a clear Kanban pipeline.
- **Procedural 2.5D Motion Engine:** Rather than relying on AI video generation APIs that hallucinate text and anatomy, the system generates procedural motion graphics using pure Python, Pillow, NumPy, and FFmpeg.
- **Zero Hallucinated Metrics:** Every statistic presented in the video is strictly validated against CrowdWisdom ground-truth data.
- **Local Reproducibility:** The entire final broadcast rendering pipeline executes locally with zero paid API dependencies required for demo reproduction.

---

## Key Features

- **Meta Ad Research Agent:** Scrapes active competitive ad campaigns from the Meta Ad Library using Apify.
- **Creative Hook & Angle Dissection:** Dissects 0–3 second opening hooks, emotional triggers, and persuasion mechanisms using Nous Research Hermes-3.
- **Cited Market Research:** Verifies market narratives and trader sentiment using Tavily citations and Exa neural semantic discovery.
- **Proprietary Data Anchoring:** Enforces factual grounding against CrowdWisdom's proprietary platform statistics.
- **Screenplay-Grade Storyboards:** Generates multi-concept storyboards with precise 35mm cinematographic direction and strict word-rate pacing.
- **Procedural Vox-Inspired Motion Engine:** 2.5D camera with parallax, halftone trader figure animations, newspaper fragments, and animated stat counters.
- **Visual Collision Guard:** Bounding-box overlap detection ensuring text cards, labels, and charts never collide or breach margin boundaries.
- **Automated Neural Voice Synthesis:** Generates high-fidelity narration via `edge-tts` with seamless fallback to offline OS speech engines (`pyttsx3`).
- **Dynamic Audio Mixing:** Automated background music ducking (-14 dB under narration), timed sound effects, and clean audio endpoint holding.
- **Broadcast FFmpeg Assembly:** Compiles crisp 1080x1920 H.264/AAC MP4 vertical video deliverables at 30 fps.

---

## System Architecture

```
                                  User / CLI
                                      │
                                      ▼
                        Hermes Multi-Agent Pipeline
                     (workflows/marketing_pipeline.py)
                                      │
        ┌───────────────────┬─────────┴─────────┬───────────────────┐
        ▼                   ▼                   ▼                   ▼
Ads Manager Agent    Research Agent      Proprietary Data    Creative Director
(Apify Meta Ads)     (Tavily / Exa)      (CrowdWisdom Data)  (3-Concept Design)
        │                   │                   │                   │
        └───────────────────┴─────────┬─────────┴───────────────────┘
                                      ▼
                              Storyboard Agent
                         (8-12 Scene Shot Sheets)
                                      │
                                      ▼
                             Storyboard Validator
                        (Pacing & Constraint Checks)
                                      │
                                      ▼
                              Video Producer
                                      │
                                      ▼
                        Procedural Vox Motion Engine
                        (tools/vox_motion_engine.py)
                                      │
               ┌──────────────────────┼──────────────────────┐
               ▼                      ▼                      ▼
         2.5D Primitives        Camera & Depth        Collision Guard
        - Halftone Figures     - 2.5D Parallax        - AABB Bounding Box
        - Newspaper Clips      - Dynamic Zoom         - Margin Checks
        - Stat Counters        - Easing Curves        - Typography Safe
               │                      │                      │
               └──────────────────────┼──────────────────────┘
                                      │
                                      ▼
                                Voice & Audio
                           (VoiceTool & AudioTool)
                          - Neural TTS / Fallback
                          - Auto-Ducking Music Bed
                                      │
                                      ▼
                               FFmpeg Pipeline
                           (tools/ffmpeg_tool.py)
                         1080x1920 • 30 fps • H.264
                                      │
                                      ▼
                 outputs/videos/final_cinematic_ad_phase22.mp4
```

---

## Agent Workflow

Each agent in the pipeline operates as an independent specialist with strict input/output boundaries:

| Agent Name | Role | Inputs | Processing Logic | Outputs | Primary Dependencies |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`AdsManagerAgent`** | Competitive Ad Intelligence | ICP search queries & targeting keywords | Executes Apify actor `apify/facebook-ads-scraper` over the last 30 days of active Meta ads | `data/processed/ads.json` | `tools/apify_tool.py` |
| **`AdAnalyzerAgent`** | Creative Angle Dissector | Normalized Meta ads JSON | Prompts Hermes-3 to isolate opening hooks (0–3s), acute pain points, marketing angles, and market gaps | `data/processed/ad_analysis.json` | `tools/llm_tool.py` (Hermes-3) |
| **`ResearchAgent`** | Market & ICP Psychologist | Extracted trader pain points | Queries Tavily for cited financial press and Exa for semantic retail trading discussions | `data/research/current_icp_research.json` | `tools/tavily_tool.py`, `tools/exa_tool.py` |
| **`ProprietaryDataAgent`** | Ground-Truth Specialist | Raw CSV/JSON metrics & company docs | Ingests platform metrics, tagging verified facts vs inferred statistical claims | Structured metrics dictionary | `data/seed_data/`, `data/company_info.txt` |
| **`CreativeDirectorAgent`** | Concept Strategist | Ad analysis, research trends, company data | Synthesizes 3 distinct 30–60s cinematic ad concepts with visual hooks and narrative arcs | `outputs/scripts/ad_concepts_phase5.json` | `tools/llm_tool.py` |
| **`StoryboardAgent`** | Cinematographer | Approved ad concepts | Generates detailed shot-by-shot storyboards with 35mm camera directions, durations, and voiceover text | Validated storyboard JSON | `agents/storyboard_validator.py` |
| **`VideoAgent`** | Video Production Engineer | Validated storyboard & scene descriptions | Coordinates asset pipelines and renders the final video composition | `outputs/videos/*.mp4` | `tools/ffmpeg_tool.py`, `tools/vox_motion_engine.py` |

---

## Video Generation Pipeline

The approved broadcast master is produced by the Phase 22 procedural pipeline ([`scripts/render_final_cinematic_ad_phase22.py`](scripts/render_final_cinematic_ad_phase22.py)):

```
Narration Script ──► Visual Argument ──► 2.5D Transformation ──► Camera Movement ──► Next Scene
```

### Visual Grammar (Not a Slideshow)
The video does not present static cards or slide transitions. Every beat obeys a strict narrative-to-visual causal chain:
1. **Narration:** The voiceover states a concrete premise.
2. **Visual Argument:** A visual entity immediately materializes to support the premise (e.g., trader figure, headline fragment, institutional chart).
3. **Object Transformation:** The object evolves dynamically (e.g., counters accelerate, charts diverge, radar sweeps activate).
4. **Camera Movement:** The 2.5D camera pans, re-focuses, or zooms with mathematical easing to guide the viewer's eye.
5. **Collision Guard:** Text cards and charts maintain strict margin spacing to prevent overlapping elements.

### Phase 22 Master Scene Architecture (48.5 Seconds)

1. **Scene 1: The Sensory Hook (0.0s – 6.0s)**
   - *Narration:* "At 2:17 in the morning, a trader isn't fighting the market. They're drowning in it."
   - *Visuals:* Halftone trader silhouette at desk, ambient room glow, incoming news and candlestick charts.
2. **Scene 2: The Feed Illusion (6.0s – 14.0s)**
   - *Narration:* "Ten tabs open. Conflicting analysts. 1,400 noisy social alerts every hour. You think you're gathering information. You're actually absorbing noise."
   - *Visuals:* Cascading social alert notifications, media clutter, red noise pulses.
3. **Scene 3: The Institutional Shift (14.0s – 22.0s)**
   - *Narration:* "Institutions don't trade headlines. They trade consensus shifts. While retail traders chase yesterday's news, algorithmic consensus has already priced it in."
   - *Visuals:* Financial newspaper fragments, order book matrices, transition from chaos to structured institutional geometry.
4. **Scene 4: The CrowdWisdom Signal (22.0s – 31.0s)**
   - *Narration:* "CrowdWisdom doesn't give you more noise. We filter 1.48 million market data points to isolate verified sentiment and directional consensus."
   - *Visuals:* Clean radar sweep, stat counter rapidly accelerating and locking firmly onto **1,482,930** verified data points.
5. **Scene 5: The Visual Proof (31.0s – 39.5s)**
   - *Narration:* "A 68.4% historical accuracy rate. 48 hours before major trend breakouts. Clear, directional conviction before the market moves."
   - *Visuals:* Verified 68.4% accuracy card, 48-hour institutional lead-time timeline, dual-series breakout chart.
6. **Scene 6: Resolution & Call to Action (39.5s – 48.5s)**
   - *Narration:* "Stop fighting the feed. Start trading the consensus. CrowdWisdom Trading. Visit crowdwisdomtrading.com."
   - *Visuals:* Editorial brand lockup, official domain callout, 1.09s visual breathing room at completion.

---

## Visual Design System

The visual language marries **CrowdWisdom's financial art direction** with **Vox-inspired visual journalism grammar**:

- **Archival Paper Canvas:** Textured warm paper base (`#EFE8DB`) with a subtle 50px geometric grid and an 18% multiplicative vignette.
- **Halftone Cutouts:** Procedurally converted monochromatic halftone trader figures and imagery.
- **Newspaper & Document Clippings:** High-contrast archival fragments with bold editorial headlines and weathered paper borders.
- **Curated Editorial Palette:**
  - Archival Tan (`#EFE8DB`) — Canvas background
  - Ink Black (`#1A1817`) — Primary typography and structural framing
  - Hot Editorial Red (`#E63946`) — Accent alerts and bearish market noise
  - Mustard Gold (`#E0A93B`) — Proprietary data highlights and radar accents
  - Grid Neutral (`#D8D0C0`) — Technical coordinate lines
- **2.5D Parallax & Depth:** True mathematical projection simulating camera distance (`Z`), lens focal length (`f=1000`), and focal depth.
- **Kinetic Editorial Typography:** Rapid overshoot reveals (`ease_out_back`) and dynamic subtitle word synchronization.

---

## Project Structure

```
crowdwisdom-hermes-video-ads/
│
├── agents/                       # Specialized Hermes Multi-Agent Implementations
│   ├── ads_manager.py            # Meta Ad Library Apify scraper & orchestrator
│   ├── ad_analyzer.py            # Competitor hook & marketing angle dissector
│   ├── research_agent.py         # Tavily cited search & Exa forum researcher
│   ├── proprietary_data_agent.py # CrowdWisdom ground-truth metrics specialist
│   ├── creative_agent.py         # 3-concept ideation & screenplay architect
│   ├── storyboard_agent.py       # Lead cinematographer & scene timing calculator
│   ├── storyboard_validator.py   # Strict duration & word-rate validator
│   └── video_agent.py            # Video production compilation orchestrator
│
├── workflows/                    # Multi-Agent Workflow State Machines
│   └── marketing_pipeline.py     # End-to-end Kanban execution coordinator
│
├── tools/                        # Production Media, Scraping & LLM Tooling
│   ├── vox_motion_engine.py      # Core 2.5D procedural motion graphics engine
│   ├── visual_collision_guard.py # AABB bounding-box collision detection guard
│   ├── voice_tool.py             # Neural TTS (edge-tts) with offline fallback
│   ├── audio_tool.py             # Audio mixing, normalization & ducking engine
│   ├── ffmpeg_tool.py            # FFmpeg encoding & stream muxing wrapper
│   ├── llm_tool.py               # Hermes-3 / OpenRouter structured client
│   ├── apify_tool.py             # Apify Meta Ad Library scraper interface
│   ├── tavily_tool.py            # Tavily market intelligence client
│   ├── exa_tool.py               # Exa neural semantic discovery client
│   └── video_provider.py         # Video generation abstractions
│
├── scripts/                      # Production Rendering & Discovery Scripts
│   ├── render_final_cinematic_ad_phase22.py # Official Phase 22 master render script
│   ├── render_final_cinematic_ad_phase21.py # Phase 21 render implementation
│   ├── render_final_cinematic_ad_phase20.py # Phase 20 render implementation
│   ├── render_final_cinematic_ad_phase19.py # Phase 19 render implementation
│   └── run_phase12_hero.py       # Hero asset generation utility
│
├── tests/                        # Verification & Quality Gate Test Suite
│   ├── test_vox_motion_engine.py # Comprehensive unit tests for motion primitives
│   ├── test_ads_schema.py        # Validation test for scraped ads schema
│   └── run_storyboard_validation.py # Storyboard constraint validator
│
├── data/                         # Input Datasets, Schemas & Static Assets
│   ├── seed_data/                # Verified CrowdWisdom platform statistics
│   ├── schemas/                  # JSON validation schemas for pipeline outputs
│   ├── assets/                   # Typography, logos, and audio background stems
│   ├── company_info.txt          # Brand positioning & product value propositions
│   └── target_audience.txt       # Retail trader persona & ICP pain points
│
├── config/                       # Application Settings & Configuration
│   └── settings.py               # Pydantic environment configuration loader
│
├── docs/                         # Detailed Architectural & Setup Guides
│   ├── QUICKSTART.md             # 5-minute fast setup guide
│   ├── ARCHITECTURE.md           # In-depth architectural documentation
│   ├── API_CONFIGURATION.md      # Environment variable specifications
│   └── TROUBLESHOOTING.md        # Common issues and solutions
│
├── reports/                      # Verification Audits & Phase Quality Reports
│   ├── phase22_verification.json # Phase 22 video technical audit
│   ├── phase23_final_validation.md # Phase 23 reproducibility & test report
│   └── phase24_github_preflight.md # Phase 24 pre-flight security scan
│
├── outputs/videos/               # Rendered Video Deliverables
│   ├── final_cinematic_ad_phase22.mp4 # Approved 48.5s Broadcast Master Ad
│   ├── phase22_cleanup_report.json    # Verified compliance and collision report
│   └── p22_frame_*.png                # Exported reference keyframes
│
├── main.py                       # Unified CLI Diagnostic & Pipeline Router
├── requirements.txt              # Pinned Python dependencies
├── .env.example                  # Secret-free environment variable template
├── .gitignore                    # Strict secret, bytecode & large binary exclusions
└── README.md                     # Primary repository guide
```

---

## Requirements

- **Operating System:** Windows 10/11, Ubuntu 20.04+ (Linux), or macOS 12+
- **Python:** Version 3.10.x or 3.11.x
- **FFmpeg:** Modern FFmpeg build (version 4.4+) installed and accessible on your system `PATH`
- **System Memory (RAM):** 8 GB minimum (16 GB recommended)
- **GPU:** Optional. Rendering runs locally on CPU via Pillow, NumPy, and FFmpeg software encoding.

---

## Installation

### 1. Clone the Repository
```bash
git clone <REPOSITORY_URL>
cd crowdwisdom-hermes-video-ads
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify FFmpeg
```bash
ffmpeg -version
```
*(If FFmpeg is not found, follow instructions in [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)).*

---

## Environment Configuration

Copy the template to create your `.env` file:
```bash
cp .env.example .env
```

Open `.env` in any editor:
```env
# --- Hermes / OpenRouter LLM Configuration ---
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
HERMES_MODEL=nousresearch/hermes-3-llama-3.1-70b
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096

# --- Meta Ad Research (Apify) ---
APIFY_API_TOKEN=
APIFY_META_ADS_ACTOR_ID=apify/facebook-ads-scraper

# --- Market Research APIs (Tavily & Exa) ---
TAVILY_API_KEY=
EXA_API_KEY=
```

> **IMPORTANT:**  
> Copy `.env.example` to `.env` and provide your own credentials.  
> Never commit `.env` into version control.

---

## API / Cost Requirements

| Service | Purpose | Required for Full Pipeline | Required for Local Video Demo | Paid Account Required? |
| :--- | :--- | :---: | :---: | :---: |
| **OpenRouter (Hermes-3)** | Multi-agent reasoning, ad analysis, scripting | **YES** | **NO** | Yes (Pay-as-you-go token usage) |
| **Apify** | Meta Ad Library scraping | **YES** | **NO** | Free tier available ($5/mo free credit) |
| **Tavily** | Cited financial market search | **YES** | **NO** | Free tier available (1,000 free searches/mo) |
| **Exa** | Neural forum discovery | Optional | **NO** | Free tier available ($10 free credit) |
| **Edge-TTS / Local TTS** | Neural narration audio generation | Local | **YES** | **100% Free** (No API key needed) |
| **Pillow / NumPy / FFmpeg** | 2.5D motion rendering & encoding | Local | **YES** | **100% Free / Open-Source** |

> **Key Takeaway:** The approved master video rendering pipeline is **100% local**. You do **not** need any external paid API credits to render and verify the broadcast master ad. External APIs are only invoked when re-running upstream live research stages.

---

## Running the Project

The CLI entrypoint [`main.py`](main.py) provides diagnostic checks and stage execution:

### 1. Diagnostics & System Status
```bash
# Check environment variables and API readiness
python main.py --status

# View the Hermes multi-agent roster and Kanban pipeline
python main.py --pipeline

# Test live Hermes-3 / OpenRouter LLM connectivity
python main.py --test-hermes
```

### 2. Multi-Stage Pipeline Execution
```bash
# Stage 1: Scrape active Meta Ads via Apify
python main.py --stage ads --max-ads 5

# Stage 2: Dissect ad hooks, angles, and CTAs via Hermes-3
python main.py --stage analyze --max-ads 5

# Stage 3: Ground pain points in cited market research (Tavily/Exa)
python main.py --stage research

# Stage 4: Synthesize proprietary data & generate 3 storyboards
python main.py --stage creative
```

---

## Demo / Reproducibility Mode

A reviewer or developer can reproduce and evaluate the approved Phase 22 broadcast master immediately:

```
Command: python scripts/render_final_cinematic_ad_phase22.py
Input:   Verified local seed data + procedural 2.5D motion primitives
Process: 30 fps procedural rendering, collision checking, neural TTS, audio mixing
Output:  outputs/videos/final_cinematic_ad_phase22.mp4
```

To execute:
```bash
python scripts/render_final_cinematic_ad_phase22.py
```

Rendering executes locally in approximately 60–90 seconds depending on CPU specifications.

---

## Output & Technical Specifications

The final broadcast deliverable complies with commercial social advertising standards:

- **File Path:** [`outputs/videos/final_cinematic_ad_phase22.mp4`](outputs/videos/final_cinematic_ad_phase22.mp4)
- **Resolution:** `1080x1920` (9:16 Vertical format)
- **Duration:** `48.50` seconds
- **Frame Rate:** `30.0 fps` (1,455 frames)
- **Video Codec:** `H.264 (libx264, yuv420p)`
- **Audio Codec:** `AAC stereo 44.1 kHz, 192 kbps`
- **File Size:** `~3.73 MB` (3,912,488 bytes)
- **Compliance:** 0 text collisions, 100% margin clearance verified by [`VisualCollisionGuard`](tools/visual_collision_guard.py)

---

## 🎬 Final Demo

The approved Phase 22 master broadcast advertisement is saved at:

📂 **[`outputs/videos/final_cinematic_ad_phase22.mp4`](outputs/videos/final_cinematic_ad_phase22.mp4)**

Accompanied by the technical audit report:
- **Compliance Audit:** [`outputs/videos/phase22_cleanup_report.json`](outputs/videos/phase22_cleanup_report.json)
- **Keyframe Previews:** `outputs/videos/p22_frame_001.png` through `p22_frame_006.png`

---

## Testing

Verify codebase integrity and motion engine algorithms with the included test suite:

```bash
# 1. Bytecode syntax and import verification across the entire project
python -m compileall .

# 2. Procedural motion engine unit tests (7/7 tests)
python tests/test_vox_motion_engine.py

# 3. Schema validation for Meta ad scraping payloads
python tests/test_ads_schema.py

# 4. Storyboard duration, word-rate, and data-anchoring validation
python tests/run_storyboard_validation.py
```

All 4 test suites pass with 100% compliance.

---

## Troubleshooting

| Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| `FFmpeg executable not found` | FFmpeg is missing from system `PATH` | Install FFmpeg via `winget install Gyan.FFmpeg` or `apt install ffmpeg` and verify with `ffmpeg -version`. |
| `[PENDING CONFIG] Hermes LLM Not Connected` | `.env` is missing or `OPENROUTER_API_KEY` is empty | Copy `.env.example` to `.env` and set an active OpenRouter API key. (Not required for local demo rendering). |
| `Audio generation falls back to pyttsx3` | Temporary network timeout to Edge-TTS servers | VoiceTool automatically falls back to offline local OS speech synthesis without disruption. |
| `Image.Image.getdata is deprecated` | Non-fatal Pillow 10+ warning | Harmless deprecation notice from PIL internal methods; rendering proceeds normally. |

For detailed resolutions, refer to [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).

---

## Security

- **Strict Secret Exclusion:** No API keys, credentials, or personal access tokens are committed to version control. All secrets reside in `.env`, which is ignored by `.gitignore`.
- **Pre-Flight Scanned:** Verified by an automated security pre-flight audit ([`reports/phase24_github_preflight.md`](reports/phase24_github_preflight.md)) confirming zero active keys in tracked files.
- **Large Binary Protection:** Raw footage and test files over 100 MB are strictly excluded from git tracking to prevent push failures.

---

## Reproducibility

To reproduce the exact master ad:
1. Clone the repository and install dependencies from `requirements.txt`.
2. Ensure FFmpeg is accessible on your system `PATH`.
3. Run `python scripts/render_final_cinematic_ad_phase22.py`.
4. Compare output against the reference values in [`outputs/videos/phase22_cleanup_report.json`](outputs/videos/phase22_cleanup_report.json).

---

## Development History

The video production engine was iteratively refined across multiple design phases:
- **Phases 1–8:** Initial multi-agent architecture, Meta ad scraping, and competitor analysis.
- **Phases 9–14:** Initial video pipeline experiments.
- **Phases 15–18:** Creative pivot to Vox-inspired visual journalism and motion graphics proofs.
- **Phases 19–21:** Extension to full 48.5s cinematic timeline, neural voice integration, and dynamic captions.
- **Phase 22:** Precision visual cleanup (complete removal of the top financial ticker and extraneous template labels, rapid stat counter lock, and collision guard enforcement).
- **Phases 23–25:** Production cleanup, read-only pre-flight security scan, and comprehensive open-source documentation.

---

## License

License: To be determined.

---

## Credits / Technologies

- **LLM Orchestration:** [Nous Research Hermes-3](https://nousresearch.com/) via [OpenRouter](https://openrouter.ai/)
- **Scraping & Research:** [Apify](https://apify.com/), [Tavily](https://tavily.com/), [Exa](https://exa.ai/)
- **Motion Graphics & Image Processing:** [Pillow](https://python-pillow.org/), [NumPy](https://numpy.org/)
- **Speech Synthesis:** [edge-tts](https://github.com/rany2/edge-tts) / [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- **Media Encoding:** [FFmpeg](https://ffmpeg.org/) via [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg)
- **Terminal UI:** [Rich](https://github.com/Textualize/rich)
