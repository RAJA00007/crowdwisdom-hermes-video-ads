"""tests/test_cinematic_vox_system.py

Phase 15 Test Suite:
Validates the complete Cinematic Vox Visual Journalism Creative System
integrated with the CrowdWisdom Company Art Direction system.

Verifies:
- every scene has narration
- every narration segment has visual argument
- every scene has company style
- every scene has camera
- every scene has depth
- every scene has transformation
- approved numbers only
- AVOID block present
- no unsupported claims.
"""

import json
import re
import sys
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tools.cinematic_vox_system import (
    ALL_VOX_CONCEPTS,
    APPROVED_STATISTICAL_CLAIMS,
    COMPANY_ART_DIRECTION_REFERENCE,
    FORBIDDEN_PATTERNS,
    MODE_DEEP_DIORAMA,
    MODE_FLAT_PARALLAX,
    MODE_LOCKED_STAGE,
    VALID_STYLE_MODES,
    CinematicVoxSystem,
)
from tools.style_prompt_system import (
    COMPANY_AVOID_DEEP_DIORAMA,
    COMPANY_AVOID_FLAT_PARALLAX_LOCKED_STAGE,
    COMPANY_STYLE_BLOCK_A_FLAT_PARALLAX,
    COMPANY_STYLE_BLOCK_B_DEEP_DIORAMA,
    COMPANY_STYLE_BLOCK_C_LOCKED_STAGE,
)
from agents.creative_agent import CreativeAgent


def load_storyboard_data():
    path = ROOT_DIR / "outputs" / "videos" / "phase15_cinematic_storyboard.json"
    assert path.exists(), f"Storyboard file not found at {path}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_script_data():
    path = ROOT_DIR / "outputs" / "videos" / "cinematic_script.json"
    assert path.exists(), f"Script file not found at {path}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_schema_data():
    path = ROOT_DIR / "outputs" / "videos" / "phase15_cinematic_storyboard_schema.json"
    assert path.exists(), f"Schema file not found at {path}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# TEST CASES
# ============================================================

def test_01_vox_concepts_and_constants():
    """Verify all 14 Vox storytelling concepts and 3 dynamic modes are defined."""
    assert len(ALL_VOX_CONCEPTS) == 14, f"Expected 14 Vox concepts, got {len(ALL_VOX_CONCEPTS)}"
    expected = [
        "VOX_HOOK", "VOX_VISUAL_ARGUMENT", "VOX_VISUAL_METAPHOR", "VOX_EDITORIAL_COLLAGE",
        "VOX_DATA_EXPLANATION", "VOX_MAP_SEQUENCE", "VOX_PHOTO_CUTOUT", "VOX_KINETIC_TYPE",
        "VOX_MATCH_CUT", "VOX_TRANSFORMATION", "VOX_2_5D_CAMERA", "VOX_INFORMATION_BUILD",
        "VOX_INFORMATION_COLLAPSE", "VOX_PAYOFF"
    ]
    for exp in expected:
        assert exp in ALL_VOX_CONCEPTS, f"Missing Vox concept: {exp}"

    assert len(VALID_STYLE_MODES) == 3
    assert MODE_DEEP_DIORAMA in VALID_STYLE_MODES
    assert MODE_FLAT_PARALLAX in VALID_STYLE_MODES
    assert MODE_LOCKED_STAGE in VALID_STYLE_MODES


def test_02_company_art_direction_preserved():
    """Verify official company prompt blocks, avoid blocks, and reference image are preserved."""
    assert len(COMPANY_STYLE_BLOCK_A_FLAT_PARALLAX) > 50
    assert len(COMPANY_STYLE_BLOCK_B_DEEP_DIORAMA) > 50
    assert len(COMPANY_STYLE_BLOCK_C_LOCKED_STAGE) > 50
    assert "AVOID:" in COMPANY_AVOID_FLAT_PARALLAX_LOCKED_STAGE
    assert "AVOID:" in COMPANY_AVOID_DEEP_DIORAMA
    ref_path = ROOT_DIR / COMPANY_ART_DIRECTION_REFERENCE
    assert ref_path.name == "company_art_direction.png"


def test_03_storyboard_schema_structure():
    """Verify phase15_cinematic_storyboard_schema.json defines all required fields."""
    schema_data = load_schema_data()
    scene_props = schema_data["properties"]["scenes"]["items"]["properties"]
    required_fields = [
        "scene_id", "start", "end", "narration", "visual_argument",
        "visual_metaphor", "style_mode", "background", "midground",
        "foreground", "company_style_components", "vox_visual_components",
        "camera_move", "depth", "transition_in", "transformation",
        "transition_out", "sound_events", "approved_text", "approved_numbers"
    ]
    for rf in required_fields:
        assert rf in scene_props, f"Missing required scene property: {rf}"


def test_04_script_agent_output_structure():
    """Verify cinematic_script.json matches Section 11 structure."""
    script_data = load_script_data()
    assert "concept" in script_data and script_data["concept"]
    assert "hook" in script_data and script_data["hook"]
    assert "target_icp" in script_data and script_data["target_icp"]
    assert "pain_point" in script_data and script_data["pain_point"]
    assert "core_insight" in script_data and script_data["core_insight"]
    assert "narration" in script_data and script_data["narration"]
    assert "scenes" in script_data and len(script_data["scenes"]) >= 6

    for sc in script_data["scenes"]:
        assert "narration" in sc and sc["narration"], f"Missing narration in script scene {sc.get('scene_id')}"
        assert "visual_argument" in sc and sc["visual_argument"], f"Missing visual_argument in script scene {sc.get('scene_id')}"
        assert "visual_metaphor" in sc and sc["visual_metaphor"], f"Missing visual_metaphor in script scene {sc.get('scene_id')}"
        assert "company_style" in sc and sc["company_style"], f"Missing company_style in script scene {sc.get('scene_id')}"
        assert "camera" in sc and sc["camera"], f"Missing camera in script scene {sc.get('scene_id')}"
        assert "transition" in sc and sc["transition"], f"Missing transition in script scene {sc.get('scene_id')}"
        assert "sound" in sc and sc["sound"], f"Missing sound in script scene {sc.get('scene_id')}"


def test_05_every_scene_has_narration():
    """Test: every scene has narration."""
    sb = load_storyboard_data()
    for sc in sb["scenes"]:
        narr = sc.get("narration", "").strip()
        assert narr, f"Scene {sc.get('scene_id')} has empty narration."


def test_06_every_narration_segment_has_visual_argument():
    """Test: every narration segment has visual argument (Vox non-negotiable rule)."""
    sb = load_storyboard_data()
    for sc in sb["scenes"]:
        v_arg = sc.get("visual_argument", "").strip()
        assert v_arg, f"Scene {sc.get('scene_id')} missing visual argument for narration: {sc.get('narration')}"
        assert len(v_arg) > 15, f"Scene {sc.get('scene_id')} visual argument too brief/generic."


def test_07_every_scene_has_company_style():
    """Test: every scene has company style components."""
    sb = load_storyboard_data()
    for sc in sb["scenes"]:
        comps = sc.get("company_style_components", [])
        assert isinstance(comps, list) and len(comps) > 0, (
            f"Scene {sc.get('scene_id')} missing company_style_components."
        )


def test_08_every_scene_has_camera():
    """Test: every scene has committed camera movement."""
    sb = load_storyboard_data()
    for sc in sb["scenes"]:
        cam = sc.get("camera_move", "").strip()
        assert cam, f"Scene {sc.get('scene_id')} missing camera_move."


def test_09_every_scene_has_depth():
    """Test: every scene has 2.5D depth planes (foreground, midground, background)."""
    sb = load_storyboard_data()
    for sc in sb["scenes"]:
        bg = sc.get("background", "").strip()
        mg = sc.get("midground", "").strip()
        fg = sc.get("foreground", "").strip()
        depth = sc.get("depth", "").strip()

        assert bg, f"Scene {sc.get('scene_id')} missing background layer."
        assert mg, f"Scene {sc.get('scene_id')} missing midground layer."
        assert fg, f"Scene {sc.get('scene_id')} missing foreground layer."
        assert depth, f"Scene {sc.get('scene_id')} missing depth description."


def test_10_every_scene_has_transformation():
    """Test: every scene has transformation for continuous visual flow."""
    sb = load_storyboard_data()
    for sc in sb["scenes"]:
        trans = sc.get("transformation", "").strip()
        assert trans, f"Scene {sc.get('scene_id')} missing visual transformation."


def test_11_approved_numbers_only():
    """Test: approved numbers only (1,482,930; 68.4%; 14.6 hours; 2:17 AM)."""
    sb = load_storyboard_data()
    sc = load_script_data()

    full_text = " ".join([
        sc.get("narration", ""),
        sc.get("core_insight", ""),
        " ".join(s.get("narration", "") for s in sb["scenes"]),
        " ".join(s.get("visual_argument", "") for s in sb["scenes"]),
        " ".join(" ".join(s.get("approved_numbers", [])) for s in sb["scenes"]),
    ])

    assert "1,482,930" in full_text, "Missing approved metric: 1,482,930"
    assert "68.4%" in full_text, "Missing approved metric: 68.4%"
    assert "14.6" in full_text, "Missing approved metric: 14.6 hours"
    assert "2:17" in full_text, "Missing approved narrative device: 2:17 AM"


def test_12_avoid_block_present():
    """Test: AVOID block is present in prompt generation for every scene."""
    vox_sys = CinematicVoxSystem()
    sb = load_storyboard_data()
    for s in sb["scenes"]:
        prompt_info = vox_sys.build_scene_prompt(s)
        assert "avoid_block" in prompt_info
        assert "AVOID:" in prompt_info["avoid_block"]
        assert "AVOID:" in prompt_info["full_prompt"]


def test_13_no_unsupported_claims():
    """Test: no unsupported claims (no 98.4M headlines, no unverified stats)."""
    sb = load_storyboard_data()
    sc = load_script_data()
    full_corpus = json.dumps(sb) + " " + json.dumps(sc)

    for pat in FORBIDDEN_PATTERNS:
        matches = re.findall(pat, full_corpus, re.IGNORECASE)
        assert len(matches) == 0, f"Found forbidden claim matching '{pat}': {matches}"

    assert "98.4" not in full_corpus, "Found unsupported claim 98.4"


def test_14_system_storyboard_validator():
    """Test: CinematicVoxSystem.validate_storyboard passes with zero errors."""
    vox_sys = CinematicVoxSystem()
    sb = load_storyboard_data()
    is_valid, errors = vox_sys.validate_storyboard(sb)
    assert is_valid, f"Storyboard validation failed with errors: {errors}"
    assert len(errors) == 0


# ============================================================
# TEST RUNNER (STANDALONE)
# ============================================================

def run_all_tests():
    tests = [
        ("01_vox_concepts_and_constants", test_01_vox_concepts_and_constants),
        ("02_company_art_direction_preserved", test_02_company_art_direction_preserved),
        ("03_storyboard_schema_structure", test_03_storyboard_schema_structure),
        ("04_script_agent_output_structure", test_04_script_agent_output_structure),
        ("05_every_scene_has_narration", test_05_every_scene_has_narration),
        ("06_every_narration_segment_has_visual_argument", test_06_every_narration_segment_has_visual_argument),
        ("07_every_scene_has_company_style", test_07_every_scene_has_company_style),
        ("08_every_scene_has_camera", test_08_every_scene_has_camera),
        ("09_every_scene_has_depth", test_09_every_scene_has_depth),
        ("10_every_scene_has_transformation", test_10_every_scene_has_transformation),
        ("11_approved_numbers_only", test_11_approved_numbers_only),
        ("12_avoid_block_present", test_12_avoid_block_present),
        ("13_no_unsupported_claims", test_13_no_unsupported_claims),
        ("14_system_storyboard_validator", test_14_system_storyboard_validator),
    ]

    print("\n============================================================")
    print("PHASE 15: CINEMATIC VOX SYSTEM TEST SUITE")
    print("============================================================\n")

    passed = 0
    failed = 0
    results = {}

    for name, fn in tests:
        try:
            fn()
            print(f" [PASS] {name}")
            results[name] = "PASSED"
            passed += 1
        except Exception as e:
            print(f" [FAIL] {name}: {e}")
            results[name] = f"FAILED: {e}"
            failed += 1

    print("\n------------------------------------------------------------")
    print(f"Summary: {passed} passed, {failed} failed out of {len(tests)} tests.")
    print("------------------------------------------------------------\n")

    report_path = ROOT_DIR / "outputs" / "videos" / "phase15_test_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "phase": "Phase 15",
            "total_tests": len(tests),
            "passed": passed,
            "failed": failed,
            "results": results,
            "all_passed": failed == 0,
            "status": "CREATIVE_SYSTEM_READY" if failed == 0 else "FAILURES_DETECTED"
        }, f, indent=2)

    print(f"Wrote Phase 15 test report to: {report_path}")

    if failed > 0:
        sys.exit(1)
    else:
        print("\nCREATIVE_SYSTEM_READY\n")


if __name__ == "__main__":
    run_all_tests()
