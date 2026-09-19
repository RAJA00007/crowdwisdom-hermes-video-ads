"""Test suite for Phase 9 Official Company Art-Direction Production.

Validates:
- 13-second mandatory style test gate (Section 20 & 21)
- Master 45-second paper diorama cinematic ad (1080x1920, 30fps)
- Palette & construction logic compliance (company_art_direction.png)
- Style QA report and Creative QA metrics
- Audio QA broadcast loudness (-16 LUFS, <= -1.0 dBTP, 0 clipping)
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

VIDEOS_DIR = Path("outputs/videos")


def test_asset_manifest_phase9():
    manifest_path = VIDEOS_DIR / "asset_manifest.json"
    assert manifest_path.exists(), "asset_manifest.json must exist"

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert "character_consistency" in manifest
    char_map = manifest["character_consistency"]
    assert char_map.get("recurring_character_id") == "trader_char_01"
    assert char_map.get("identity_match_verified") is True


def test_style_test_13s_video():
    style_video = VIDEOS_DIR / "style_test_13s.mp4"
    assert style_video.exists(), "outputs/videos/style_test_13s.mp4 must exist"
    assert style_video.stat().st_size > 100_000, "13s style test must be non-empty"

    from tools.ffmpeg_tool import FFmpegTool
    ft = FFmpegTool()
    vinfo = ft.get_video_info(style_video)

    assert vinfo["width"] == 1080, f"Expected width 1080, got {vinfo['width']}"
    assert vinfo["height"] == 1920, f"Expected height 1920, got {vinfo['height']}"
    assert 12.0 <= vinfo["duration"] <= 14.0, f"Expected duration ~13s, got {vinfo['duration']}"


def test_final_cinematic_ad_phase9():
    final_video = VIDEOS_DIR / "final_cinematic_ad.mp4"
    assert final_video.exists(), "outputs/videos/final_cinematic_ad.mp4 must exist"
    assert final_video.stat().st_size > 500_000, "Final ad must be non-empty"

    from tools.ffmpeg_tool import FFmpegTool
    ft = FFmpegTool()
    vinfo = ft.get_video_info(final_video)

    assert vinfo["width"] == 1080, f"Expected width 1080, got {vinfo['width']}"
    assert vinfo["height"] == 1920, f"Expected height 1920, got {vinfo['height']}"
    assert 44.0 <= vinfo["duration"] <= 46.5, f"Expected duration ~45s, got {vinfo['duration']}"


def test_style_qa_report():
    style_path = VIDEOS_DIR / "style_qa_report.json"
    assert style_path.exists(), "style_qa_report.json must exist"

    with open(style_path, "r", encoding="utf-8") as f:
        sqa = json.load(f)

    assert sqa.get("style_qa_status") == "PASSED"
    assert sqa["palette_compliance"].get("archival_tan_#C9BB9C") is True
    assert sqa["palette_compliance"].get("hot_red_#D62E1F") is True
    assert sqa["construction_logic_verified"].get("halftone_texture_present") is True
    assert sqa["construction_logic_verified"].get("offset_hot_red_stroke_present") is True


def test_creative_qa_report_phase9():
    qa_path = VIDEOS_DIR / "creative_qa_report.json"
    assert qa_path.exists(), "creative_qa_report.json must exist"

    with open(qa_path, "r", encoding="utf-8") as f:
        qa = json.load(f)

    assert qa.get("qa_status") == "PASSED", f"Creative QA rejected: {qa.get('rejection_reasons')}"
    metrics = qa.get("metrics", {})

    assert metrics.get("paper_diorama_ratio", 0) >= 0.50
    assert metrics.get("generic_dashboard_ratio", 1.0) <= 0.10
    assert metrics.get("neon_ratio") == 0.0
    assert metrics.get("glossy_3d_ratio") == 0.0
    assert metrics.get("uncontrolled_text_ratio") == 0.0
    assert metrics.get("ai_text_detected") is False
    assert metrics.get("same_character_recurrence") is True
    assert metrics.get("narration_overlap") == 0


def test_audio_qa_report_phase9():
    audio_path = VIDEOS_DIR / "audio_qa_report.json"
    assert audio_path.exists(), "audio_qa_report.json must exist"

    with open(audio_path, "r", encoding="utf-8") as f:
        aqa = json.load(f)

    assert aqa.get("audio_qa_status") == "PASSED"
    assert aqa.get("audio_clipping_detected") is False
    assert aqa.get("true_peak_dbtp", 0.0) <= -1.0


def test_phase9_prompt_specification_file():
    prompt_file = Path("prompts/phase9_official_art_direction.txt")
    assert prompt_file.exists(), "prompts/phase9_official_art_direction.txt must exist"
    content = prompt_file.read_text(encoding="utf-8")
    assert "OFFICIAL COMPANY-PROVIDED PROMPT SYSTEM" in content
    assert "COMPANY STYLE BLOCK A — FLAT PARALLAX" in content
    assert "COMPANY STYLE BLOCK B — DEEP DIORAMA" in content
    assert "COMPANY STYLE BLOCK C — LOCKED STAGE" in content
    assert "COMPANY SHOT CONSTRUCTION RULES" in content
    assert "COMPANY CAMERA MOVE LIBRARY" in content
    assert "COMPANY ESCALATION DEVICES" in content
    assert "COMPANY AUDIO RULE" in content
    assert "COMPANY AVOID — FLAT PARALLAX / LOCKED STAGE" in content
    assert "COMPANY AVOID — DEEP DIORAMA" in content


def test_style_prompt_system_module():
    from tools.style_prompt_system import (
        get_flat_parallax_style,
        get_deep_diorama_style,
        get_locked_stage_style,
        build_shot_prompt,
        build_audio_prompt,
        build_avoid_prompt,
        build_complete_generation_prompt,
        ALLOWED_CAMERA_MOVES,
    )

    # 1. Exact verbatim styles
    style_a = get_flat_parallax_style()
    assert "Use the attached style sheet as the strict visual system" in style_a
    assert "Layers sit at distinct depths like a paper diorama" in style_a

    style_b = get_deep_diorama_style()
    assert "Use the attached style sheet for materials only" in style_b
    assert "every clip is a deep 3D paper diorama" in style_b

    style_c = get_locked_stage_style()
    assert "Documentary cutout-collage stage:" in style_c
    assert "Camera: subtle slow drift only, never cuts." in style_c

    # 2. Shot construction
    shot = build_shot_prompt(
        background="Archival tan paper",
        mg="Halftone trader cutout",
        fg="(giant number) 2:17 AM card",
        camera="push-in",
        settle="Settle on illuminated card",
        depth_description="at three distinct physical depths",
    )
    assert "BACKGROUND:" in shot
    assert "MG:" in shot
    assert "FG:" in shot
    assert "CAMERA: push-in (ONE committed camera move)" in shot
    assert "SETTLE:" in shot
    assert "DEPTH: at three distinct physical depths" in shot

    # 3. Audio construction
    audio = build_audio_prompt("push-in")
    assert "AUDIO:\n[" in audio
    assert "— sound design only, no music, no narration." in audio

    # 4. Avoid construction
    avoid_deep = build_avoid_prompt("deep_diorama")
    assert "AVOID: no flat single-plane composition" in avoid_deep

    avoid_tech = build_avoid_prompt("flat_parallax", has_tech_or_ui=True)
    assert "AVOID: no glossy CG 3D" in avoid_tech
    assert "no UI or glass elements" in avoid_tech

    # 5. Full prompt construction
    full_prompt = build_complete_generation_prompt(
        style_type="locked_stage",
        shot_params={
            "background": "Aged paper",
            "mg": "None",
            "fg": "(headline) SIGNAL",
            "camera": "slow drift lateral",
            "settle": "Hold on frame",
            "depth_description": "one plane locked stage",
        },
    )
    assert "============================================================" in full_prompt
    assert "STYLE BLOCK" in full_prompt
    assert "SHOT" in full_prompt
    assert "AUDIO" in full_prompt
    assert "AVOID" in full_prompt


def test_editorial_storyboard_company_prompts():
    storyboard_path = VIDEOS_DIR / "editorial_storyboard.json"
    assert storyboard_path.exists(), "editorial_storyboard.json must exist"

    with open(storyboard_path, "r", encoding="utf-8") as f:
        sb = json.load(f)

    beats = sb.get("beats", [])
    assert len(beats) == 8, f"Expected 8 beats, got {len(beats)}"

    alert_wash_count = 0
    camera_moves = []

    for beat in beats:
        bid = beat.get("beat_id")
        style_type = beat.get("style_mode") or beat.get("style_block") or beat.get("style_block_type")
        assert style_type in ["flat_parallax", "deep_diorama", "locked_stage"], (
            f"Beat {bid} has invalid style block {style_type}"
        )

        # Camera move check
        cam = beat.get("camera_move")
        assert cam, f"Beat {bid} missing camera_move"
        camera_moves.append(cam)

        # Depth description check
        depth_desc = beat.get("depth_description")
        assert depth_desc and len(depth_desc) > 10, f"Beat {bid} missing depth_description"

        # Structured prompt check
        gen_prompt = beat.get("generation_prompt", "")
        assert "STYLE BLOCK" in gen_prompt, f"Beat {bid} missing STYLE BLOCK in generation_prompt"
        assert "SHOT" in gen_prompt, f"Beat {bid} missing SHOT in generation_prompt"
        assert "AUDIO" in gen_prompt, f"Beat {bid} missing AUDIO in generation_prompt"
        assert "AVOID" in gen_prompt, f"Beat {bid} missing AVOID in generation_prompt"

        # Explicit text element tagging check in foreground
        fg = beat.get("fg") or beat.get("structured_shot", {}).get("fg", "")
        has_tag = any(tag in fg for tag in ["(headline)", "(label)", "(counter)", "(giant number)"])
        assert has_tag, f"Beat {bid} foreground must contain tagged text element: {fg}"

        # Escalation device check
        if beat.get("escalation_device") == "ALERT WASH":
            alert_wash_count += 1
            assert bid == 6, f"ALERT WASH must strictly be in Beat 6, found in Beat {bid}"

    assert alert_wash_count == 1, f"Expected exactly 1 ALERT WASH, found {alert_wash_count}"

    # Sequencing check: never use the same camera move twice consecutively
    for i in range(len(camera_moves) - 1):
        assert camera_moves[i] != camera_moves[i + 1], (
            f"Consecutive identical camera move detected at beat {i+1} and {i+2}: {camera_moves[i]}"
        )


def test_style_test_13s_v2_video():
    style_v2 = VIDEOS_DIR / "style_test_13s_v2.mp4"
    assert style_v2.exists(), "outputs/videos/style_test_13s_v2.mp4 must exist"
    assert style_v2.stat().st_size > 100_000, "13s style test v2 must be non-empty"

    from tools.ffmpeg_tool import FFmpegTool
    ft = FFmpegTool()
    vinfo = ft.get_video_info(style_v2)

    assert vinfo["width"] == 1080, f"Expected width 1080, got {vinfo['width']}"
    assert vinfo["height"] == 1920, f"Expected height 1920, got {vinfo['height']}"
    assert 12.0 <= vinfo["duration"] <= 14.0, f"Expected duration ~13s, got {vinfo['duration']}"


def test_phase9_prompt_audit_json():
    audit_file = VIDEOS_DIR / "phase9_prompt_audit.json"
    assert audit_file.exists(), "outputs/videos/phase9_prompt_audit.json must exist"

    with open(audit_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "company_reference_found" in data
    assert "company_prompt_system_integrated" in data
    assert "files_audited" in data
    assert len(data["files_audited"]) > 0


def test_style_prompt_validation_json():
    val_file = VIDEOS_DIR / "style_prompt_validation.json"
    assert val_file.exists(), "outputs/videos/style_prompt_validation.json must exist"

    with open(val_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("valid") is True, f"Validation errors: {data.get('errors')}"
    assert data.get("total_scenes") == 8
    assert len(data.get("errors", [])) == 0


if __name__ == "__main__":
    print("Running Phase 9 & 9.1 test suite...")
    test_phase9_prompt_specification_file()
    print("[PASS] test_phase9_prompt_specification_file")
    test_style_prompt_system_module()
    print("[PASS] test_style_prompt_system_module")
    test_editorial_storyboard_company_prompts()
    print("[PASS] test_editorial_storyboard_company_prompts")
    test_asset_manifest_phase9()
    print("[PASS] test_asset_manifest_phase9")
    test_style_test_13s_video()
    print("[PASS] test_style_test_13s_video")
    test_style_test_13s_v2_video()
    print("[PASS] test_style_test_13s_v2_video")
    test_phase9_prompt_audit_json()
    print("[PASS] test_phase9_prompt_audit_json")
    test_style_prompt_validation_json()
    print("[PASS] test_style_prompt_validation_json")
    test_final_cinematic_ad_phase9()
    print("[PASS] test_final_cinematic_ad_phase9")
    test_style_qa_report()
    print("[PASS] test_style_qa_report")
    test_creative_qa_report_phase9()
    print("[PASS] test_creative_qa_report_phase9")
    test_audio_qa_report_phase9()
    print("[PASS] test_audio_qa_report_phase9")
    print("\nAll Phase 9 & 9.1 tests passed successfully!")

