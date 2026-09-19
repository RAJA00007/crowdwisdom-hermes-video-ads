"""Test suite for Phase 10: Final OpenMontage Video Generation + 45s Master Ad.

Covers:
- test_openmontage_provider
- test_provider_fallback
- test_generated_clips_manifest
- test_phase10_storyboard
- test_no_unsupported_statistics
- test_phase10_final_video
- test_phase10_final_qa
- test_provider_truthfulness
"""

import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.video_provider import (
    OpenMontageProvider,
    HyperframesProvider,
    LeronxProvider,
    FallbackEditorialProvider,
    VideoProviderHierarchy,
    ProviderNotConfiguredError,
)
from tools.ffmpeg_tool import FFmpegTool

VIDEOS_DIR = Path("outputs/videos")


def test_openmontage_provider():
    """Verify OpenMontage provider interface and configuration handling."""
    provider = OpenMontageProvider()
    assert provider.get_provider_name() == "openmontage"
    assert provider.supports_image_reference() is True

    status = provider.get_status()
    assert "status" in status
    assert "configured" in status

    # When no API key or local binary exists, it must report OPENMONTAGE_NOT_CONFIGURED
    if not provider.is_configured():
        assert status["status"] == "OPENMONTAGE_NOT_CONFIGURED"
        raised = False
        try:
            provider.generate_clip({"scene_id": "test"}, Path("dummy.mp4"))
        except ProviderNotConfiguredError:
            raised = True
        assert raised, "Expected ProviderNotConfiguredError when OpenMontage is not configured"


def test_provider_fallback():
    """Verify provider fallback hierarchy defaults gracefully and truthfully."""
    hierarchy = VideoProviderHierarchy()
    h_status = hierarchy.get_hierarchy_status()

    assert h_status["hierarchy"] == ["openmontage", "hyperframes", "leronx", "fallback_editorial_compositor"]
    assert "openmontage_status" in h_status
    assert "active_primary_provider" in h_status

    # If OpenMontage credentials not set, fallback must be engaged
    if h_status["openmontage_status"] == "OPENMONTAGE_NOT_CONFIGURED":
        assert h_status["fallback_engaged"] is True
        assert h_status["active_primary_provider"] == "fallback_editorial_compositor"


def test_generated_clips_manifest():
    """Verify outputs/videos/generated_clips_manifest.json contains truthful clip entries."""
    manifest_path = VIDEOS_DIR / "generated_clips_manifest.json"
    assert manifest_path.exists(), f"Missing {manifest_path}"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["total_clips"] == 8
    assert "openmontage_status" in manifest
    assert "active_primary_provider" in manifest
    assert "fallback_engaged" in manifest
    assert len(manifest["clips"]) == 8

    # Verify no secret credentials or API keys were written
    manifest_str = json.dumps(manifest)
    assert "api_key" not in manifest_str.lower() or '"has_api_key":' in manifest_str

    for clip in manifest["clips"]:
        assert "scene_id" in clip
        assert "provider" in clip
        assert "prompt" in clip
        assert "style_mode" in clip
        assert "duration" in clip
        assert "resolution" in clip
        assert "generation_status" in clip
        assert "output_path" in clip
        assert Path(clip["output_path"]).exists(), f"Clip file missing: {clip['output_path']}"


def test_phase10_storyboard():
    """Verify Phase 10 storyboard strictly adheres to company style system and 8 beats."""
    sb_path = VIDEOS_DIR / "editorial_storyboard.json"
    assert sb_path.exists(), f"Missing {sb_path}"

    with open(sb_path, "r", encoding="utf-8") as f:
        sb = json.load(f)

    scenes = sb.get("scenes", sb.get("beats", []))
    assert len(scenes) == 8, f"Expected 8 scenes, got {len(scenes)}"
    assert round(sb.get("total_duration_sec", 0), 1) == 45.0

    valid_style_blocks = {"flat_parallax", "deep_diorama", "locked_stage"}
    for sc in scenes:
        assert sc.get("style_mode") in valid_style_blocks
        prompt = sc.get("generation_prompt", "")
        assert "STYLE BLOCK" in prompt
        assert "SHOT" in prompt
        assert "AUDIO" in prompt
        assert "AVOID" in prompt
        assert sc.get("camera_move"), "Each scene must commit to exactly one camera movement"


def test_no_unsupported_statistics():
    """Verify approved numbers exist and 98.4M is completely absent."""
    sb_path = VIDEOS_DIR / "editorial_storyboard.json"
    meta_path = VIDEOS_DIR / "final_cinematic_ad_phase10_metadata.json"

    with open(sb_path, "r", encoding="utf-8") as f:
        sb_text = f.read()

    with open(meta_path, "r", encoding="utf-8") as f:
        meta_text = f.read()

    # 1. 98.4M must NOT be in storyboard
    assert "98.4M" not in sb_text
    assert "98.4" not in sb_text
    assert "98,400,000" not in sb_text

    # 2. Approved statistics must be present in storyboard
    assert "1,482,930" in sb_text or "1482930" in sb_text
    assert "68.4%" in sb_text or "68.4" in sb_text
    assert "14.6h" in sb_text or "14.6" in sb_text
    assert "2:17" in sb_text

    # 3. Metadata factual claims
    assert "1,482,930" in meta_text
    assert "68.4%" in meta_text
    assert "14.6h" in meta_text


def test_phase10_final_video():
    """Verify final_cinematic_ad_phase10.mp4 has correct dimensions, duration, and stream."""
    final_video = VIDEOS_DIR / "final_cinematic_ad_phase10.mp4"
    assert final_video.exists(), f"Final ad missing: {final_video}"
    assert final_video.stat().st_size > 500_000, "Final ad file is suspiciously small"

    ft = FFmpegTool()
    vinfo = ft.get_video_info(final_video)

    assert vinfo["width"] == 1080, f"Expected width 1080, got {vinfo['width']}"
    assert vinfo["height"] == 1920, f"Expected height 1920, got {vinfo['height']}"
    assert 40.0 <= vinfo["duration"] <= 60.0, f"Expected 40-60s, got {vinfo['duration']}"
    assert 29.0 <= vinfo["fps"] <= 31.0, f"Expected ~30fps, got {vinfo['fps']}"
    assert vinfo["has_audio"] is True, "Final video must contain an audio track"


def test_phase10_final_qa():
    """Verify Phase 10 final QA report passes all quality gates."""
    qa_path = VIDEOS_DIR / "phase10_final_qa.json"
    assert qa_path.exists(), f"QA report missing: {qa_path}"

    with open(qa_path, "r", encoding="utf-8") as f:
        qa = json.load(f)

    assert qa.get("qa_status") == "PASSED", f"QA did not pass: {qa}"
    assert qa.get("video_status") == "PASS"
    assert qa.get("audio_status") == "PASS"
    assert qa.get("factual_status") == "PASS"
    assert qa.get("style_status") == "PASS"
    assert qa.get("text_status") == "PASS"
    assert qa.get("provider_status") == "PASS"

    # Audio metrics: ~ -17 LUFS, TP <= -1.0 dBTP, 0 clipping
    audio_m = qa.get("audio_metrics", {})
    assert -20.0 <= audio_m.get("integrated_lufs", 0.0) <= -14.0
    assert audio_m.get("true_peak_dbtp", 0.0) <= -1.0
    assert audio_m.get("audio_clipping") is False


def test_provider_truthfulness():
    """Verify metadata honestly and accurately reports fallback usage."""
    meta_path = VIDEOS_DIR / "final_cinematic_ad_phase10_metadata.json"
    assert meta_path.exists(), f"Metadata missing: {meta_path}"

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    provider = meta.get("actual_provider_used")
    fallback_used = meta.get("fallback_used")
    ai_video_generated = meta.get("ai_video_generated")

    if provider == "fallback_editorial_compositor":
        assert fallback_used is True
        assert ai_video_generated is False, "Must not claim AI video generation when fallback compositor was used"
    elif provider == "openmontage":
        assert fallback_used is False
        assert ai_video_generated is True


if __name__ == "__main__":
    print("============================================================")
    print("RUNNING PHASE 10 PRODUCTION TEST SUITE")
    print("============================================================")
    tests = [
        ("test_openmontage_provider", test_openmontage_provider),
        ("test_provider_fallback", test_provider_fallback),
        ("test_generated_clips_manifest", test_generated_clips_manifest),
        ("test_phase10_storyboard", test_phase10_storyboard),
        ("test_no_unsupported_statistics", test_no_unsupported_statistics),
        ("test_phase10_final_video", test_phase10_final_video),
        ("test_phase10_final_qa", test_phase10_final_qa),
        ("test_provider_truthfulness", test_provider_truthfulness),
    ]

    passed = 0
    for name, func in tests:
        try:
            func()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            raise

    print(f"\n[OK] ALL {passed}/{len(tests)} PHASE 10 TESTS PASSED SUCCESSFULLY!")

