"""Automated verification test for Phase 5: Proprietary Data Ingestion, Creative Director, and Storyboard Generation."""

import json
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.storyboard_validator import StoryboardValidator, ALLOWED_GENERATION_METHODS
from tools.proprietary_data_tool import ProprietaryDataTool
from agents.creative_agent import CreativeAgent
from agents.storyboard_agent import StoryboardAgent


def test_phase5_pipeline():
    # 1. Test Proprietary Data Ingestion
    tool = ProprietaryDataTool()
    summary, summary_path = tool.extract_and_summarize()
    assert Path(summary_path).exists(), f"Summary path {summary_path} does not exist"
    assert "factual_data" in summary
    assert "calculated_metrics" in summary
    assert "llm_interpretations" in summary
    assert summary["factual_data"]["total_trader_inputs_indexed"] == 1482930
    assert summary["calculated_metrics"]["crowd_consensus_directional_accuracy_pct"] == 68.4
    print("[PASS] 1. Proprietary data ingestion and normalization verified.")

    # 2. Test Creative Director
    creative = CreativeAgent()
    context = creative.load_context_data()
    concepts = creative.develop_three_concepts(context)
    assert len(concepts) == 3, f"Expected 3 concepts, got {len(concepts)}"
    for c in concepts:
        assert "hook_visual" in c, f"Concept {c.get('concept_id')} missing hook_visual"
        assert "target_icp" in c, f"Concept {c.get('concept_id')} missing target_icp"
        assert "pain_point" in c, f"Concept {c.get('concept_id')} missing pain_point"
    print("[PASS] 2. Creative Director generated 3 distinct concepts with visual hooks.")

    # 3. Test Storyboard Generation
    storyboard_agent = StoryboardAgent()
    sb_result = storyboard_agent.run_storyboard_generation(concepts, summary, verbose=False)
    assert sb_result["success"] is True
    storyboards = sb_result["storyboards"]
    assert len(storyboards) == 3

    # 4. Verify Output Files Exist and are valid JSON
    output_dir = Path(__file__).resolve().parent.parent / "outputs" / "scripts"
    assert (output_dir / "concept_01.json").exists()
    assert (output_dir / "concept_02.json").exists()
    assert (output_dir / "concept_03.json").exists()
    assert (output_dir / "all_concepts.json").exists()

    with open(output_dir / "all_concepts.json", "r", encoding="utf-8") as f:
        loaded_all = json.load(f)
    assert len(loaded_all["storyboards"]) == 3
    print("[PASS] 3 & 4. All concept files and all_concepts.json exist and are valid JSON.")

    # 5. Verify Scenes, Durations, Generation Methods, and Hooks
    validator = StoryboardValidator(summary)
    val_report = validator.validate_all(storyboards)
    assert val_report["all_valid"] is True, f"Validation failed: {val_report}"

    for sb in storyboards:
        cid = sb["concept_id"]
        scenes = sb["scenes"]
        total_dur = sb["total_duration_sec"]
        assert 8 <= len(scenes) <= 12, f"{cid} scene count {len(scenes)} out of bounds"
        assert 30 <= total_dur <= 60, f"{cid} duration {total_dur} out of bounds"

        # Check generation methods
        for s in scenes:
            assert s["generation_method"] in ALLOWED_GENERATION_METHODS, f"Invalid method {s['generation_method']} in {cid}"
            assert len(s["visual"]) >= 30, f"Visual description too short in {cid} scene {s['scene_id']}"
            assert isinstance(s["sound_effects"], list), f"sound_effects must be a list in {cid}"
            assert "camera" in s and isinstance(s["camera"], dict), f"camera must be dict in {cid}"

        # Check proprietary data presence
        prop_scenes = [s for s in scenes if s.get("data_source") == "proprietary_data_summary.json"]
        assert len(prop_scenes) >= 1, f"{cid} missing proprietary data scene"

        # Check CTA presence
        has_cta = any("crowdwisdomtrading.com" in s.get("on_screen_text", "").lower() or "crowdwisdomtrading.com" in s.get("voiceover", "").lower() for s in scenes[-2:])
        assert has_cta, f"{cid} missing crowdwisdomtrading.com in closing CTA"

    print("[PASS] 5, 6, 7, 8. Every scene has valid generation method, visual hook, CrowdWisdom data, and passes strict validation.")
    print("\nALL PHASE 5 AUTOMATED VERIFICATION CHECKS PASSED!")


if __name__ == "__main__":
    test_phase5_pipeline()
