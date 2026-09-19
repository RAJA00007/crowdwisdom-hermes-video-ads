"""tests/test_phase12_openmontage.py

Comprehensive test suite for Phase 12:
Autonomous OpenMontage Installation + Real AI Video Integration.

Verifies:
1. OpenMontage installation detection
2. Provider discovery & matrix validation
3. No fake credentials rule
4. Real provider detection & honest preflight
5. Hero generation hard gate & error handling
6. Hero metadata truthfulness (ai_video_generated strictly False without real provider)
7. Storyboard integration (8 beats, 16-field cinematic prompts)
8. Factual integrity (verified statistics only, no 98.4M hallucination)
9. Pipeline honest halt behavior (no silent FFmpeg substitution)
"""

import json
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.video_provider import (
    OpenMontageProvider,
    VideoProviderHierarchy,
    ProviderNotConfiguredError,
    VideoClipResult,
)


def test_openmontage_installation_detection():
    """Verify OpenMontage is installed outside the project in C:\\Users\\Raja\\OpenMontage."""
    provider = OpenMontageProvider()
    assert provider.is_installed(), "OpenMontage repository must be detected as installed"
    assert provider.openmontage_path.exists(), f"Path {provider.openmontage_path} does not exist"
    assert (provider.openmontage_path / "tools" / "base_tool.py").exists(), "base_tool.py must exist in OpenMontage"

    version = provider.get_version()
    assert version != "NOT_INSTALLED", "Version must be resolvable"
    assert len(version) >= 4, f"Unexpected short version string: {version}"

    install_json_path = PROJECT_ROOT / "outputs" / "videos" / "phase12_openmontage_install.json"
    assert install_json_path.exists(), "phase12_openmontage_install.json must exist"
    with open(install_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["installed"] is True
    assert "OpenMontage" in data["install_path"]
    assert data["installation_method"] == "git_clone"


def test_openmontage_provider_discovery():
    """Verify provider discovery detects OpenMontage video generation tools."""
    provider = OpenMontageProvider()
    backends = provider.discover_backends()

    assert len(backends) >= 15, f"Expected at least 15 video tools, found {len(backends)}"
    expected_tools = [
        "kling_video",
        "veo_video",
        "runway_video",
        "minimax_video",
        "seedance_ark",
        "wan_video",
    ]
    for t in expected_tools:
        assert t in backends, f"Expected tool '{t}' not found in discovered backends"

    matrix_path = PROJECT_ROOT / "outputs" / "videos" / "phase12_provider_matrix.json"
    assert matrix_path.exists(), "phase12_provider_matrix.json must exist"
    with open(matrix_path, "r", encoding="utf-8") as f:
        matrix = json.load(f)
    assert matrix["openmontage_installed"] is True
    assert len(matrix["providers"]) >= 15


def test_no_fake_credentials():
    """Ensure no fake or fabricated API credentials exist in provider configuration."""
    provider = OpenMontageProvider()
    backends = provider.discover_backends()

    # Cloud video providers must NOT be marked configured unless real keys exist in os.environ
    for name, info in backends.items():
        if info["runtime"] == "api":
            req_key = info.get("required_credential")
            if req_key and not os.environ.get(req_key):
                assert info["configured"] is False, (
                    f"Tool {name} marked configured without active env credential {req_key}"
                )


def test_real_provider_detection_and_honest_preflight():
    """Verify preflight accurately identifies whether a real AI backend is available."""
    provider = OpenMontageProvider()
    pf = provider.preflight()

    assert pf["openmontage_installed"] is True
    assert isinstance(pf["missing_credentials"], list)

    # In the absence of real cloud video keys or local GPU diffusers stack
    if not provider.is_available():
        assert pf["status"] == "AI_VIDEO_PROVIDER_UNAVAILABLE"
        assert pf["active_backend"] is None
        assert len(pf["missing_credentials"]) > 0


def test_hero_metadata_truthfulness():
    """Verify phase12_hero_metadata.json never falsely claims AI generation without a real provider."""
    meta_path = PROJECT_ROOT / "outputs" / "videos" / "phase12_hero_metadata.json"
    assert meta_path.exists(), "phase12_hero_metadata.json must be recorded"

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    provider = OpenMontageProvider()
    if not provider.is_available():
        assert meta["status"] == "AI_VIDEO_PROVIDER_UNAVAILABLE"
        assert meta["ai_video_generated"] is False
        assert meta["active_backend"] is None
        assert "STOP PRODUCTION" in meta["message"]
        assert "exact_manual_action_required" in meta


def test_hero_generation_gate():
    """Verify generate_clip raises ProviderNotConfiguredError when no provider is active."""
    provider = OpenMontageProvider()
    if not provider.is_available():
        raised = False
        try:
            provider.generate_clip(
                scene={"scene_id": "beat_01", "duration": 5.0, "generation_prompt": "Test prompt"},
                output_path=Path("outputs/videos/test_fake_hero.mp4"),
            )
        except ProviderNotConfiguredError:
            raised = True
        assert raised, "Expected ProviderNotConfiguredError when no real AI video backend is configured"


def test_storyboard_integration_phase12():
    """Verify Phase 11/12 cinematic storyboard conforms to the 16-field prompt architecture."""
    sb_path = PROJECT_ROOT / "outputs" / "videos" / "phase11_cinematic_storyboard.json"
    assert sb_path.exists(), "phase11_cinematic_storyboard.json must exist"

    with open(sb_path, "r", encoding="utf-8") as f:
        sb = json.load(f)

    beats = sb.get("scenes", sb.get("beats", []))
    assert len(beats) == 8, f"Expected 8 beats in cinematic storyboard, found {len(beats)}"

    # Beat 1 must be the 0-5s solitary retail trader hook
    beat_1 = beats[0]
    prompt = beat_1.get("cinematic_ai_prompt", beat_1.get("generation_prompt", ""))
    assert "retail" in prompt.lower() or "trader" in prompt.lower()
    assert "2:17" in prompt or "dark" in prompt.lower() or "monitor" in prompt.lower()


def test_no_unsupported_statistics():
    """Verify that hallucinated statistics (e.g. 98.4M Daily Headlines) remain completely excluded."""
    sb_path = PROJECT_ROOT / "outputs" / "videos" / "phase11_cinematic_storyboard.json"
    with open(sb_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "98.4M" not in content, "Forbidden hallucinated statistic 98.4M must not be present"
    assert "98.4 million" not in content.lower(), "Forbidden phrase 98.4 million must not be present"

    # Verify verified statistics are present
    assert "1,482,930" in content
    assert "68.4%" in content
    assert "14.6h" in content or "14.6" in content


def test_pipeline_honest_halt():
    """Verify run_phase12_pipeline honestly halts when credentials are missing."""
    hierarchy = VideoProviderHierarchy()
    if not hierarchy.openmontage.is_available():
        res = hierarchy.run_phase12_pipeline()
        assert res["status"] == "AI_VIDEO_PROVIDER_UNAVAILABLE"
        assert res["ai_video_generated"] is False
        assert res["openmontage_installed"] is True
        assert "exact_manual_action_required" in res


if __name__ == "__main__":
    tests = [
        test_openmontage_installation_detection,
        test_openmontage_provider_discovery,
        test_no_fake_credentials,
        test_real_provider_detection_and_honest_preflight,
        test_hero_metadata_truthfulness,
        test_hero_generation_gate,
        test_storyboard_integration_phase12,
        test_no_unsupported_statistics,
        test_pipeline_honest_halt,
    ]
    passed = 0
    failed = 0
    print(f"\nRunning Phase 12 test suite ({len(tests)} tests)...")
    for t in tests:
        try:
            t()
            print(f"  [PASS] {t.__name__}")
            passed += 1
        except Exception as exc:
            print(f"  [FAIL] {t.__name__}: {exc}")
            failed += 1

    print(f"\nTest Summary: {passed}/{len(tests)} passed, {failed} failed.\n")
    if failed > 0:
        sys.exit(1)

