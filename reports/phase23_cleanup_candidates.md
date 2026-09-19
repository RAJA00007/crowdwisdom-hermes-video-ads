# Phase 23: Codebase Cleanup Candidates Assessment

> **Purpose**: Formal audit of potentially unused, legacy, or orphaned Python files.  
> **Policy**: AUDIT ONLY — Zero files deleted. When in doubt, preserve.  
> **Date**: September 20, 2026

---

## 1. Candidate Evaluation Matrix

### Candidate 1: `scripts/probe_footage.py`
- **FILE**: `scripts/probe_footage.py`
- **STATUS**: LEGACY_UNREFERENCED
- **WHY IT APPEARS UNUSED**: 11-line ad-hoc utility created during Phase 14 to run `ffprobe` on a single local `.ogv` file.
- **REFERENCED BY**: None.
- **IMPORTERS**: None.
- **RUNTIME REFERENCES**: None.
- **SAFE TO DELETE**: YES
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: Safe to remove prior to final submission if repository trimming is desired, or keep as a test script.

---

### Candidate 2: `scripts/fetch_footage.py`
- **FILE**: `scripts/fetch_footage.py`
- **STATUS**: LEGACY_UNREFERENCED
- **WHY IT APPEARS UNUSED**: Downloaded Pexels and Wikimedia Commons stock video clips during Phase 14. Stock video was eliminated in Phase 15 in favor of procedural motion graphics.
- **REFERENCED BY**: `outputs/videos/footage_manifest.json` (historical record only).
- **IMPORTERS**: None.
- **RUNTIME REFERENCES**: None.
- **SAFE TO DELETE**: YES
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: Safe to remove or archive; not required by Phase 22.

---

### Candidate 3: `scripts/generate_overlays.py`
- **FILE**: `scripts/generate_overlays.py`
- **STATUS**: LEGACY_UNREFERENCED
- **WHY IT APPEARS UNUSED**: Generated static PNG title cards and subtitle plates for the Phase 14 stock-footage compositor.
- **REFERENCED BY**: Phase 14 test records.
- **IMPORTERS**: None.
- **RUNTIME REFERENCES**: None.
- **SAFE TO DELETE**: YES
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: Safe to archive.

---

### Candidate 4: `scripts/extract_phase14_frames.py`
- **FILE**: `scripts/extract_phase14_frames.py`
- **STATUS**: LEGACY_UNREFERENCED
- **WHY IT APPEARS UNUSED**: Standalone utility script extracting frames from `final_cinematic_ad_phase14.mp4`.
- **REFERENCED BY**: None.
- **IMPORTERS**: None.
- **RUNTIME REFERENCES**: None.
- **SAFE TO DELETE**: YES
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: Safe to remove.

---

### Candidate 5: `scripts/test_synth_p19.py`
- **FILE**: `scripts/test_synth_p19.py`
- **STATUS**: TEST / SCRATCH
- **WHY IT APPEARS UNUSED**: One-off 32-line test script created during Phase 19 to verify Edge TTS speech synthesis speed.
- **REFERENCED BY**: None.
- **IMPORTERS**: None.
- **RUNTIME REFERENCES**: None.
- **SAFE TO DELETE**: YES
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: Keep in `tests/` or safe to delete if strictly minimizing file count.

---

### Candidate 6: `tools/video_tool.py`
- **FILE**: `tools/video_tool.py`
- **STATUS**: POTENTIALLY_UNUSED
- **WHY IT APPEARS UNUSED**: 50-line legacy wrapper around OpenCV/imageio. Phase 22 uses `tools/ffmpeg_tool.py` directly.
- **REFERENCED BY**: None.
- **IMPORTERS**: None.
- **RUNTIME REFERENCES**: None.
- **SAFE TO DELETE**: YES
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: Safe to remove or keep as legacy fallback.

---

### Candidate 7: `agents/style_prompt_validator.py`
- **FILE**: `agents/style_prompt_validator.py`
- **STATUS**: POTENTIALLY_UNUSED
- **WHY IT APPEARS UNUSED**: Validated Midjourney/Runway generative text prompts during Phase 9. Neither `main.py` nor `video_agent.py` calls it directly.
- **REFERENCED BY**: `tests/test_phase9_art_direction.py`.
- **IMPORTERS**: `tests/test_phase9_art_direction.py`.
- **RUNTIME REFERENCES**: Invoked during `pytest` execution.
- **SAFE TO DELETE**: NO (Breaks existing unit test suite).
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: DO NOT DELETE. Retain to ensure unit test suite passes.

---

### Candidate 8: `scripts/render_vox_motion_proof_v2.py`
- **FILE**: `scripts/render_vox_motion_proof_v2.py`
- **STATUS**: LEGACY_BUT_HISTORICAL_REFERENCE
- **WHY IT APPEARS UNUSED**: Renders the 10-second motion proof approved in Phase 19 (`outputs/videos/vox_motion_proof_v2.mp4`).
- **REFERENCED BY**: Prompts, walkthrough documentation, and design specifications as the definitive visual style lock reference.
- **IMPORTERS**: None.
- **RUNTIME REFERENCES**: None.
- **SAFE TO DELETE**: NO (Essential project historical reference).
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: DO NOT DELETE. Retain as visual reference evidence.

---

### Candidate 9: `scripts/render_final_cinematic_ad_phase20.py`
- **FILE**: `scripts/render_final_cinematic_ad_phase20.py`
- **STATUS**: ACTIVE_SUPPORT (DEPENDENCY PROVIDER)
- **WHY IT APPEARS UNUSED**: It is an earlier phase renderer.
- **REFERENCED BY**: `scripts/render_final_cinematic_ad_phase21.py` and `scripts/render_final_cinematic_ad_phase22.py`.
- **IMPORTERS**: `scripts/render_final_cinematic_ad_phase22.py` lines 59–66.
- **RUNTIME REFERENCES**: Provides `NotificationAlertBubble`, `MicroChartFragment`, `EditorialCaptionObject`, `AccuracyComparisonCardAudited`, and `TimelineLeadObjectAudited`.
- **SAFE TO DELETE**: **ABSOLUTELY NO (CRITICAL: WILL BREAK PRODUCTION PHASE 22)**
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: **MUST NOT BE DELETED.**

---

### Candidate 10: `scripts/render_final_cinematic_ad_phase19.py`
- **FILE**: `scripts/render_final_cinematic_ad_phase19.py`
- **STATUS**: ACTIVE_SUPPORT (DEPENDENCY PROVIDER)
- **WHY IT APPEARS UNUSED**: It is an earlier phase renderer.
- **REFERENCED BY**: `scripts/render_final_cinematic_ad_phase20.py`, `scripts/render_final_cinematic_ad_phase21.py`, and `scripts/render_final_cinematic_ad_phase22.py`.
- **IMPORTERS**: `scripts/render_final_cinematic_ad_phase22.py` lines 67–70.
- **RUNTIME REFERENCES**: Provides `BrandResolutionLockup` and `RadarDirectionalObject`.
- **SAFE TO DELETE**: **ABSOLUTELY NO (CRITICAL: WILL BREAK PRODUCTION PHASE 22)**
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: **MUST NOT BE DELETED.**

---

### Candidate 11: `scripts/render_final_cinematic_ad_phase21.py`
- **FILE**: `scripts/render_final_cinematic_ad_phase21.py`
- **STATUS**: LEGACY_UNREFERENCED
- **WHY IT APPEARS UNUSED**: Superseded by `render_final_cinematic_ad_phase22.py`.
- **REFERENCED BY**: Documentation and audit reports.
- **IMPORTERS**: None.
- **RUNTIME REFERENCES**: None.
- **SAFE TO DELETE**: YES (Functionally superseded, but valuable milestone record).
- **CONFIDENCE**: HIGH
- **RECOMMENDED ACTION**: Retain in repository as proof of progression or archive cleanly.

---

## 2. Decision Summary

| File | Status | Safe to Delete? | Deletion Executed? |
| :--- | :--- | :---: | :---: |
| `scripts/probe_footage.py` | Orphaned Utility | YES | NO (Preserved per safety rule) |
| `scripts/fetch_footage.py` | Discontinued Downloader | YES | NO (Preserved per safety rule) |
| `scripts/generate_overlays.py` | Discontinued Overlay Tool | YES | NO (Preserved per safety rule) |
| `scripts/extract_phase14_frames.py` | One-off Frame Tool | YES | NO (Preserved per safety rule) |
| `scripts/test_synth_p19.py` | Scratch Audio Test | YES | NO (Preserved per safety rule) |
| `tools/video_tool.py` | Legacy Wrapper | YES | NO (Preserved per safety rule) |
| `agents/style_prompt_validator.py` | Test-Referenced Validator | **NO** | NO (Protected) |
| `scripts/render_vox_motion_proof_v2.py` | Milestone Visual Proof | **NO** | NO (Protected) |
| `scripts/render_final_cinematic_ad_phase20.py` | Active Component Provider | **NO** | NO (Protected) |
| `scripts/render_final_cinematic_ad_phase19.py` | Active Component Provider | **NO** | NO (Protected) |
| `scripts/render_final_cinematic_ad_phase21.py` | Milestone Ad Renderer | YES | NO (Preserved per safety rule) |
