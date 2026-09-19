"""Automated test suite for Phase 7 Video Production Redesign.

Validates:
- Storyboard structure and scene definitions.
- Hook test video (Section 11) resolution, duration, and audio.
- Final ad (Section 10) resolution, duration (40-50s), and playable container.
- Creative QA metrics and broadcast audio standards.
"""

import json
from pathlib import Path
from tools.ffmpeg_tool import FFmpegTool



def test_storyboard_phase7_contract():
    script_path = Path("outputs/scripts/concept_phase7_editorial.json")
    assert script_path.exists(), "Phase 7 storyboard contract must exist"
    with open(script_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["concept_id"] == "concept_phase7_editorial"
    assert 40.0 <= data["total_duration_sec"] <= 50.0
    assert len(data["scenes"]) >= 8
    assert data["resolution"]["width"] == 1080
    assert data["resolution"]["height"] == 1920


def test_section11_hook_test_render():
    hook_path = Path("outputs/videos/test_cinematic_hook.mp4")
    assert hook_path.exists(), "Section 11 hook test video must exist"
    assert hook_path.stat().st_size > 50000, "Hook test MP4 must not be empty"

    ft = FFmpegTool()
    info = ft.get_video_info(hook_path)
    assert info["width"] == 1080
    assert info["height"] == 1920
    assert info["duration"] <= 4.05
    assert info["has_audio"] is True


def test_section10_final_cinematic_ad():
    final_path = Path("outputs/videos/final_cinematic_ad.mp4")
    assert final_path.exists(), "Final cinematic ad MP4 must exist"
    assert final_path.stat().st_size > 1000000, "Final ad MP4 must be a full playable video"

    ft = FFmpegTool()
    info = ft.get_video_info(final_path)
    assert info["width"] == 1080
    assert info["height"] == 1920
    assert 40.0 <= info["duration"] <= 50.0
    assert info["has_audio"] is True


def test_creative_qa_report():
    report_path = Path("outputs/videos/creative_qa_report.json")
    assert report_path.exists(), "Creative QA report must exist"
    with open(report_path, "r", encoding="utf-8") as f:
        qa = json.load(f)

    assert qa["qa_status"] == "PASSED"
    assert qa["passed"] is True
    metrics = qa["metrics"]
    assert metrics["actual_video_ratio"] >= 0.30
    assert metrics["data_visualization_ratio"] <= 0.35
    assert metrics["text_only_ratio"] <= 0.20
    assert metrics["narration_overlap"] == 0
    assert metrics["hook_duration_sec"] <= 4.05


def test_audio_qa_report():
    report_path = Path("outputs/videos/audio_qa_report.json")
    assert report_path.exists(), "Audio QA report must exist"
    with open(report_path, "r", encoding="utf-8") as f:
        a_qa = json.load(f)

    assert a_qa["audio_qa_status"] == "PASSED"
    assert a_qa["true_peak_dbtp"] <= -1.0
    assert a_qa["audio_clipping_detected"] is False
    assert a_qa["music_ducking_active"] is True
