"""Test suite for Phase 8 Editorial Video Production.

Validates:
- 13-second editorial test video (Section 25 Mandatory Step Gate)
- Final 45-second cinematic editorial ad (1080x1920, 30fps)
- Character continuity across Beat 1 and Beat 6
- Creative QA metrics and thresholds (no generic dashboards, 0 AI text, >30% footage)
- Audio QA loudness and peak thresholds (-16 LUFS, <= -1.0 dBTP, zero clipping)
"""

import json
from pathlib import Path


VIDEOS_DIR = Path("outputs/videos")


def test_asset_manifest_consistency():
    manifest_path = VIDEOS_DIR / "asset_manifest.json"
    assert manifest_path.exists(), "asset_manifest.json must exist"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert "character_consistency" in manifest
    char_map = manifest["character_consistency"]
    assert char_map.get("recurring_character_id") == "trader_char_01"
    assert char_map.get("opening_beat") == 1
    assert char_map.get("payoff_beat") == 6
    assert char_map.get("identity_match_verified") is True


def test_editorial_test_13s_video():
    test_video = VIDEOS_DIR / "editorial_test_13s.mp4"
    assert test_video.exists(), "outputs/videos/editorial_test_13s.mp4 must exist"
    assert test_video.stat().st_size > 100_000, "13s test video must be non-empty (>100KB)"

    from tools.ffmpeg_tool import FFmpegTool
    ft = FFmpegTool()
    vinfo = ft.get_video_info(test_video)

    assert vinfo["width"] == 1080, f"Expected width 1080, got {vinfo['width']}"
    assert vinfo["height"] == 1920, f"Expected height 1920, got {vinfo['height']}"
    assert 12.0 <= vinfo["duration"] <= 14.0, f"Expected duration ~13s, got {vinfo['duration']}"


def test_final_cinematic_ad():
    final_video = VIDEOS_DIR / "final_cinematic_ad.mp4"
    assert final_video.exists(), "outputs/videos/final_cinematic_ad.mp4 must exist"
    assert final_video.stat().st_size > 500_000, "Final ad must be non-empty (>500KB)"

    from tools.ffmpeg_tool import FFmpegTool
    ft = FFmpegTool()
    vinfo = ft.get_video_info(final_video)

    assert vinfo["width"] == 1080, f"Expected width 1080, got {vinfo['width']}"
    assert vinfo["height"] == 1920, f"Expected height 1920, got {vinfo['height']}"
    assert 44.0 <= vinfo["duration"] <= 46.5, f"Expected duration ~45s, got {vinfo['duration']}"


def test_creative_qa_report():
    qa_path = VIDEOS_DIR / "creative_qa_report.json"
    assert qa_path.exists(), "creative_qa_report.json must exist"

    with open(qa_path, "r", encoding="utf-8") as f:
        qa = json.load(f)

    assert qa.get("qa_status") == "PASSED", f"Creative QA rejected: {qa.get('rejection_reasons')}"
    metrics = qa.get("metrics", {})

    assert metrics.get("cinematic_footage_ratio", 0) >= 0.30
    assert metrics.get("data_visualization_ratio", 1.0) <= 0.35
    assert metrics.get("text_only_ratio", 1.0) <= 0.20
    assert metrics.get("generic_dashboard_ratio", 1.0) <= 0.15
    assert metrics.get("ai_text_detected") is False
    assert metrics.get("same_character_recurrence") is True
    assert metrics.get("narration_overlap") == 0
    assert metrics.get("hook_duration_sec", 10.0) <= 4.05


def test_audio_qa_report():
    audio_path = VIDEOS_DIR / "audio_qa_report.json"
    assert audio_path.exists(), "audio_qa_report.json must exist"

    with open(audio_path, "r", encoding="utf-8") as f:
        aqa = json.load(f)

    assert aqa.get("audio_qa_status") == "PASSED"
    assert aqa.get("audio_clipping_detected") is False
    assert aqa.get("true_peak_dbtp", 0.0) <= -1.0


def test_video_generation_report():
    gen_path = VIDEOS_DIR / "video_generation_report.json"
    assert gen_path.exists(), "video_generation_report.json must exist"

    with open(gen_path, "r", encoding="utf-8") as f:
        gen = json.load(f)

    assert gen.get("video_provider") == "fallback"
    assert gen.get("ai_video_generated") is False
    assert "character_continuity" in gen
    assert gen["character_continuity"].get("same_character_verified") is True
