"""Test suite for Phase 11: Cinematic AI Video Overhaul.

Covers:
- test_phase11_prompt_architecture
- test_phase11_storyboard_structure
- test_phase11_verified_statistics
- test_phase11_provider_detection
- test_phase11_production_halt_when_no_ai_provider
"""

import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.phase11_prompt_system import (
    get_phase11_storyboard_definitions,
    build_phase11_cinematic_prompt,
    PHASE11_NEGATIVE_PROMPT,
)
from tools.video_provider import VideoProviderHierarchy

VIDEOS_DIR = Path("outputs/videos")


def test_phase11_prompt_architecture():
    """Verify all 8 beats implement the full 16-field cinematic AI prompt specification."""
    beats = get_phase11_storyboard_definitions()
    assert len(beats) == 8

    required_fields = [
        "subject", "environment", "time_of_day", "lighting", "material",
        "camera", "lens_feel", "depth", "foreground", "midground",
        "background", "motion", "atmosphere", "editorial_style", "color",
        "transition_intent"
    ]

    for b in beats:
        pdata = b["prompt_data"]
        for f in required_fields:
            assert f in pdata, f"Beat {b['beat_id']} missing required prompt field: {f}"
            assert len(pdata[f].strip()) > 10, f"Beat {b['beat_id']} prompt field {f} too brief"

        full_prompt = build_phase11_cinematic_prompt(**pdata)
        assert "SUBJECT:" in full_prompt
        assert "CAMERA:" in full_prompt
        assert "LENS FEEL:" in full_prompt
        assert "DEPTH:" in full_prompt
        assert "FOREGROUND:" in full_prompt
        assert "MIDGROUND:" in full_prompt
        assert "BACKGROUND:" in full_prompt

    # Negative prompt verification
    assert "plastic humans" in PHASE11_NEGATIVE_PROMPT
    assert "wax faces" in PHASE11_NEGATIVE_PROMPT
    assert "fake charts" in PHASE11_NEGATIVE_PROMPT
    assert "gibberish text" in PHASE11_NEGATIVE_PROMPT
    assert "slideshow appearance" in PHASE11_NEGATIVE_PROMPT


def test_phase11_storyboard_structure():
    """Verify outputs/videos/phase11_cinematic_storyboard.json structure and rhythm."""
    sb_path = VIDEOS_DIR / "phase11_cinematic_storyboard.json"
    assert sb_path.exists(), f"Missing {sb_path}"

    with open(sb_path, "r", encoding="utf-8") as f:
        sb = json.load(f)

    assert sb.get("total_duration_sec") == 45.0
    scenes = sb.get("scenes", [])
    assert len(scenes) == 8

    expected_rhythm = [
        (0.0, 5.0, 5.0),
        (5.0, 10.0, 5.0),
        (10.0, 14.0, 4.0),
        (14.0, 20.0, 6.0),
        (20.0, 27.0, 7.0),
        (27.0, 34.0, 7.0),
        (34.0, 40.0, 6.0),
        (40.0, 45.0, 5.0),
    ]

    for idx, (st, et, dur) in enumerate(expected_rhythm):
        sc = scenes[idx]
        assert sc["start_time"] == st
        assert sc["end_time"] == et
        assert sc["duration"] == dur


def test_phase11_verified_statistics():
    """Verify verified stats exist and 98.4M is strictly absent from Phase 11 storyboard."""
    sb_path = VIDEOS_DIR / "phase11_cinematic_storyboard.json"
    with open(sb_path, "r", encoding="utf-8") as f:
        sb_text = f.read()

    assert "98.4M" not in sb_text
    assert "98.4" not in sb_text
    assert "1,482,930" in sb_text or "1482930" in sb_text or "1.48 million" in sb_text
    assert "68.4" in sb_text
    assert "14.6" in sb_text


def test_phase11_provider_detection():
    """Verify that VideoProviderHierarchy exposes all AI video providers."""
    hierarchy = VideoProviderHierarchy()
    status = hierarchy.get_hierarchy_status()

    expected_providers = [
        "openmontage", "hyperframes", "leronx", "runway", "veo",
        "replicate", "luma", "kling", "pika", "fallback_editorial_compositor"
    ]
    hierarchy_list = status.get("extended_hierarchy", status["hierarchy"])
    for p in expected_providers:
        assert p in hierarchy_list, f"Missing {p} from provider hierarchy"


def test_phase11_production_halt_when_no_ai_provider():
    """Verify Phase 11 stops production with AI_VIDEO_PROVIDER_UNAVAILABLE if no AI credentials exist."""
    hierarchy = VideoProviderHierarchy()
    if not hierarchy.has_active_ai_provider():
        audit = hierarchy.run_phase11_preflight(
            storyboard={"scenes": [{"scene_id": "beat_01", "duration": 5.0}]},
            output_dir=VIDEOS_DIR,
        )
        assert audit["status"] == "AI_VIDEO_PROVIDER_UNAVAILABLE"
        assert audit["production_halted"] is True
        assert "STOP PRODUCTION" in audit["message"]


if __name__ == "__main__":
    print("============================================================")
    print("RUNNING PHASE 11 CINEMATIC TEST SUITE")
    print("============================================================")
    tests = [
        ("test_phase11_prompt_architecture", test_phase11_prompt_architecture),
        ("test_phase11_storyboard_structure", test_phase11_storyboard_structure),
        ("test_phase11_verified_statistics", test_phase11_verified_statistics),
        ("test_phase11_provider_detection", test_phase11_provider_detection),
        ("test_phase11_production_halt_when_no_ai_provider", test_phase11_production_halt_when_no_ai_provider),
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

    print(f"\n[OK] ALL {passed}/{len(tests)} PHASE 11 TESTS PASSED SUCCESSFULLY!")
