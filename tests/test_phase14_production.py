"""tests/test_phase14_production.py

Quality Gates for Phase 14:
1. Final Master Video Exists (outputs/videos/final_cinematic_ad_phase14.mp4)
2. Exact Duration (30–60s) and Resolution (1080x1920 portrait)
3. Valid H.264 MP4 with Audio Track
4. Audio Loudness Target (-17 LUFS approx, True Peak <= -1.0 dBFS, zero clipping)
5. Zero Narration Overlaps
6. Strictly Approved Metrics (1,482,930 | 68.4% | 14.6 HOURS) and Zero Unsupported Statistics
7. Brand and CTA Verification (CROWDWISDOM TRADING, SEE THE SIGNAL INSIDE THE NOISE, crowdwisdomtrading.com)
8. Honest Production Mode (ai_video_generation: False, no fake AI claim)
9. Footage Manifest Integrity (verified public domain / CC licenses)
10. Multi-agent Hermes Architecture Preserved
"""

import json
import os
import subprocess
import sys
from pathlib import Path
# pytest optional

# Add project root
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tools.ffmpeg_tool import FFmpegTool
from tools.video_provider import VideoProviderRouter
from workflows.marketing_pipeline import MarketingPipeline

ff_tool = FFmpegTool()

VIDEO_PATH = ROOT_DIR / "outputs" / "videos" / "final_cinematic_ad_phase14.mp4"
STORYBOARD_PATH = ROOT_DIR / "outputs" / "videos" / "phase14_storyboard.json"
PRODUCTION_MODE_PATH = ROOT_DIR / "outputs" / "videos" / "video_production_mode.json"
FOOTAGE_MANIFEST_PATH = ROOT_DIR / "outputs" / "videos" / "footage_manifest.json"
MASTER_AUDIO_PATH = ROOT_DIR / "outputs" / "videos" / "phase14_master_audio.wav"


def test_01_final_master_exists():
    """Verify final master video exists and has non-trivial size (> 5MB)."""
    assert VIDEO_PATH.exists(), f"Missing final video: {VIDEO_PATH}"
    size_mb = VIDEO_PATH.stat().st_size / (1024 * 1024)
    assert size_mb >= 5.0, f"Final video file size too small: {size_mb:.2f} MB"


def test_02_duration_and_resolution():
    """Verify video duration is between 30 and 60 seconds, and resolution is 1080x1920 portrait."""
    info = ff_tool.get_video_info(VIDEO_PATH)
    assert info["exists"] is True
    dur = info["duration"]
    assert 30.0 <= dur <= 60.0, f"Duration {dur}s outside required 30-60s range"
    assert info["width"] == 1080, f"Width {info['width']} != 1080"
    assert info["height"] == 1920, f"Height {info['height']} != 1920"
    assert info["has_audio"] is True, "Video has no audio track"


def test_03_audio_loudness_and_no_clipping():
    """Verify broadcast audio loudness target (-17 LUFS approx) and no clipping (True Peak <= -1.0 dBFS)."""
    cmd = [
        ff_tool.ffmpeg_path,
        "-i", str(VIDEO_PATH),
        "-filter_complex", "ebur128=peak=true",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    lines = res.stderr.strip().split("\n")
    
    integrated_lufs = None
    true_peak = None
    for line in lines:
        if "I:" in line and "LUFS" in line:
            parts = line.split()
            try:
                integrated_lufs = float(parts[1])
            except (IndexError, ValueError):
                pass
        if "Peak:" in line and "dBFS" in line:
            parts = line.split()
            try:
                true_peak = float(parts[1])
            except (IndexError, ValueError):
                pass

    assert integrated_lufs is not None, "Could not measure integrated loudness"
    assert true_peak is not None, "Could not measure true peak"
    # Target: approx -17 LUFS (acceptable broadcast window: -19.0 to -15.0)
    assert -19.0 <= integrated_lufs <= -15.0, f"Integrated loudness {integrated_lufs} outside [-19, -15] LUFS"
    # No clipping: True Peak must not exceed -1.0 dBFS
    assert true_peak <= -1.0, f"Audio clipping detected! True peak {true_peak} > -1.0 dBFS"


def test_04_no_narration_overlap():
    """Verify that all speech segments have strictly zero overlap."""
    assert STORYBOARD_PATH.exists(), f"Missing storyboard: {STORYBOARD_PATH}"
    with open(STORYBOARD_PATH, "r", encoding="utf-8") as f:
        sb = json.load(f)
    beats = sb.get("beats", [])
    assert len(beats) == 8, f"Expected 8 beats, got {len(beats)}"

    for i in range(len(beats) - 1):
        assert beats[i]["end_time"] <= beats[i+1]["start_time"], (
            f"Beat timing overlap between {beats[i]['scene_id']} and {beats[i+1]['scene_id']}"
        )


def test_05_approved_statistics_only():
    """Verify only approved numerical claims are present and unsupported numbers are excluded."""
    with open(STORYBOARD_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Approved statistics MUST be present
    assert "1,482,930" in content, "Missing verified metric 1,482,930 trader inputs"
    assert "68.4%" in content or "68.4 percent" in content, "Missing verified metric 68.4%"
    assert "14.6" in content, "Missing verified metric 14.6 hours"

    # Strictly forbidden unverified numbers MUST NOT be present
    forbidden_numbers = ["98.4M", "98.4 million", "41.2%", "27.2%", "79.1%"]
    for fn in forbidden_numbers:
        assert fn not in content, f"Unsupported statistic detected in storyboard: {fn}"


def test_06_branding_and_cta():
    """Verify CrowdWisdom branding and CTA elements are present."""
    with open(STORYBOARD_PATH, "r", encoding="utf-8") as f:
        sb = json.load(f)

    b8 = sb["beats"][-1]
    text_corpus = " ".join(b8["approved_text"]).lower()
    assert "crowdwisdom trading" in text_corpus, "Missing brand in Beat 8"
    assert "see the signal inside the noise" in text_corpus, "Missing tagline in Beat 8"
    assert "crowdwisdomtrading.com" in text_corpus, "Missing domain CTA in Beat 8"


def test_07_no_fake_ai_generation_claim():
    """Verify production metadata truthfully records production mode without faking AI video."""
    assert PRODUCTION_MODE_PATH.exists(), f"Missing {PRODUCTION_MODE_PATH}"
    with open(PRODUCTION_MODE_PATH, "r", encoding="utf-8") as f:
        mode_data = json.load(f)

    assert mode_data.get("ai_video_generation") is False, "Metadata falsely claimed AI video generation"
    assert mode_data.get("mode") in ["cinematic_licensed_footage", "licensed_cinematic_footage"], (
        f"Unexpected production mode: {mode_data.get('mode')}"
    )
    assert mode_data.get("paid_services_used") is False, "Paid services used contrary to zero-cost requirement"


def test_08_footage_manifest_integrity():
    """Verify footage manifest exists and all assets have legal Creative Commons / Public Domain licenses."""
    assert FOOTAGE_MANIFEST_PATH.exists(), f"Missing {FOOTAGE_MANIFEST_PATH}"
    with open(FOOTAGE_MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert len(manifest) >= 4, "Footage manifest must have at least 4 verified assets"
    for item in manifest:
        lic = item.get("license", "").lower()
        assert any(k in lic for k in ["cc0", "cc by", "public domain", "cc-by"]), (
            f"Asset {item.get('asset_id')} has incompatible license: {lic}"
        )
        assert item.get("source") == "Wikimedia Commons", "Asset must originate from verified Commons"


def test_09_hermes_architecture_preserved():
    """Verify the multi-agent Hermes pipeline components remain intact and functional."""
    pipeline = MarketingPipeline()
    summary = pipeline.get_pipeline_summary()
    assert "agents" in summary
    assert len(summary["agents"]) >= 4

    router = VideoProviderRouter()
    decision = router.decide_production_mode()
    assert decision["mode"] == "cinematic_licensed_footage"


if __name__ == "__main__":
    tests = [
        ("Final Master Video Exists", test_01_final_master_exists),
        ("Duration & 1080x1920 Resolution", test_02_duration_and_resolution),
        ("Broadcast Audio & No Clipping", test_03_audio_loudness_and_no_clipping),
        ("Zero Narration Overlap", test_04_no_narration_overlap),
        ("Approved Statistics Only", test_05_approved_statistics_only),
        ("Branding & CTA Integrity", test_06_branding_and_cta),
        ("Honest Production Mode (No Fake AI)", test_07_no_fake_ai_generation_claim),
        ("Footage Manifest & CC Licensing", test_08_footage_manifest_integrity),
        ("Hermes Multi-Agent Architecture", test_09_hermes_architecture_preserved),
    ]

    print("\n============================================================")
    print("      PHASE 14 PRODUCTION QUALITY GATE VERIFICATION        ")
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

    qa_report_path = ROOT_DIR / "outputs" / "videos" / "phase14_qa_report.json"
    with open(qa_report_path, "w", encoding="utf-8") as f:
        json.dump({
            "phase": "Phase 14",
            "total_tests": len(tests),
            "passed": passed,
            "failed": failed,
            "results": results,
            "all_passed": failed == 0,
            "master_video": str(VIDEO_PATH)
        }, f, indent=2)
    print(f"Wrote QA report to: {qa_report_path}")

    if failed > 0:
        sys.exit(1)

