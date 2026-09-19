# API Configuration Guide — CrowdWisdom Hermes AI Video Advertising System

This document describes all environment variables used by the CrowdWisdom Hermes system, where they are consumed in the codebase, whether they are required, and fallback behavior when they are absent.

> **CRITICAL SECURITY RULE:**  
> Never commit `.env` into version control. Only edit your local `.env` file created from `.env.example`.

---

## Environment Variables Matrix

| Environment Variable | Service / Purpose | Where Used in Code | Required for Full Pipeline | Required for Local Video Demo | Behavior When Missing |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `OPENROUTER_API_KEY` | Hermes 3 LLM agent reasoning | `config/settings.py`, `tools/llm_tool.py` | **YES** | **NO** | Multi-agent reasoning fails with configuration notice; offline fallback data used if available. |
| `OPENROUTER_BASE_URL` | OpenRouter endpoint URL | `config/settings.py`, `tools/llm_tool.py` | Optional | **NO** | Defaults to `https://openrouter.ai/api/v1`. |
| `HERMES_MODEL` | OpenRouter target model | `config/settings.py`, `tools/llm_tool.py` | Optional | **NO** | Defaults to `nousresearch/hermes-3-llama-3.1-70b`. |
| `LLM_TEMPERATURE` | LLM generation temperature | `config/settings.py`, `tools/llm_tool.py` | Optional | **NO** | Defaults to `0.7`. |
| `LLM_MAX_TOKENS` | LLM token generation limit | `config/settings.py`, `tools/llm_tool.py` | Optional | **NO** | Defaults to `4096`. |
| `APIFY_API_TOKEN` | Meta Ad Library scraping | `config/settings.py`, `tools/apify_tool.py`, `agents/ads_manager.py` | **YES** (for Stage 1) | **NO** | Live scraping disabled; pipeline falls back to cached `data/processed/ads.json`. |
| `APIFY_META_ADS_ACTOR_ID`| Target Apify actor ID | `config/settings.py`, `tools/apify_tool.py` | Optional | **NO** | Defaults to `apify/facebook-ads-scraper`. |
| `TAVILY_API_KEY` | Cited financial search | `config/settings.py`, `tools/tavily_tool.py`, `agents/research_agent.py`| **YES** (for Stage 3) | **NO** | Live web search skipped; falls back to cached research findings. |
| `EXA_API_KEY` | Neural semantic search | `config/settings.py`, `tools/exa_tool.py`, `agents/research_agent.py` | Optional | **NO** | Neural forum search skipped; relies solely on Tavily or cached research data. |
| `FAL_KEY` | External GenAI video (optional legacy) | `tools/video_provider.py`, `scripts/run_phase12_hero.py` | Optional | **NO** | Phase 22 video rendering runs 100% locally via procedural engine and does not use Fal.ai. |
| `OPENMONTAGE_BIN_PATH` | OpenMontage executable path | `config/settings.py`, `tools/openmontage_tool.py` | Optional | **NO** | Automatically defaults to `Path.home() / "OpenMontage"`. |
| `VIDEO_OUTPUT_RESOLUTION`| Vertical video dimensions | `config/settings.py` | Optional | **NO** | Defaults to `1080x1920`. |
| `VIDEO_DEFAULT_DURATION_SEC`| Standard ad length | `config/settings.py` | Optional | **NO** | Defaults to `48.5`. |

---

## Detailed Variable Specifications

### 1. `OPENROUTER_API_KEY`
- **Description:** API authorization key for OpenRouter, providing access to Nous Research Hermes-3.
- **Acquisition:** Register at [openrouter.ai](https://openrouter.ai/) and generate an API key.
- **Consumption:** Initialized via `config/settings.py` and passed into `HermesLLMClient` (`tools/llm_tool.py`).
- **Validation:** Run `python main.py --test-hermes` to verify connectivity.

### 2. `APIFY_API_TOKEN`
- **Description:** API token for Apify to invoke the Meta Ad Library scraper actor (`apify/facebook-ads-scraper`).
- **Acquisition:** Create an account at [apify.com](https://apify.com/) and retrieve your Personal API Token from Account Settings.
- **Consumption:** Consumed by `ApifyTool` (`tools/apify_tool.py`) in `AdsManagerAgent` (`agents/ads_manager.py`).
- **Execution:** Invoked during `python main.py --stage ads`.

### 3. `TAVILY_API_KEY`
- **Description:** Search API designed specifically for LLM agents to retrieve clean, cited financial articles.
- **Acquisition:** Obtain an API key from [tavily.com](https://tavily.com/).
- **Consumption:** Consumed by `TavilyTool` (`tools/tavily_tool.py`) in `ResearchAgent` (`agents/research_agent.py`).
- **Execution:** Invoked during `python main.py --stage research`.

### 4. `EXA_API_KEY`
- **Description:** Neural search engine for semantic similarity and forum discussion extraction (Reddit, trading communities).
- **Acquisition:** Obtain an API key from [exa.ai](https://exa.ai/).
- **Consumption:** Consumed by `ExaTool` (`tools/exa_tool.py`) in `ResearchAgent` (`agents/research_agent.py`).
- **Execution:** Invoked during `python main.py --stage research`.

### 5. `FAL_KEY` (Optional)
- **Description:** External API key for Fal.ai generative video models (Kling, Luma, Fast-SVD).
- **Consumption:** Present in `tools/video_provider.py` as an optional fallback provider.
- **Important Note:** The approved Phase 22 master advertisement is rendered entirely via procedural Python/PIL/NumPy/FFmpeg algorithms. **`FAL_KEY` is not required** to produce the final video advertisement.

---

## Step-by-Step Configuration

1. Copy the secret-free template:
   ```bash
   cp .env.example .env
   ```
2. Populate the keys using any text editor:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxx
   APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxx
   TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx
   EXA_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```
3. Verify your configuration status:
   ```bash
   python main.py --status
   ```
