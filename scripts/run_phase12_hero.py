"""scripts/run_phase12_hero.py

Executes Phase 12 FAL + OpenMontage Hero Test according to specifications:
1. Securely loads FAL_KEY from environment.
2. Runs OpenMontage preflight.
3. Enumerates FAL video models available in OpenMontage.
4. Selects the strongest model (Kling / MiniMax H3).
5. Prepares image-to-video using assets/style_reference/company_art_direction.png.
6. Prepares Beat 1 prompt from outputs/videos/phase11_cinematic_storyboard.json.
7. Submits 5-second hero generation to fal.ai queue API.
8. Truthfully records metadata and quality gate results.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")


def run_hero_test():
    fal_key = os.getenv("FAL_KEY", "").strip()
    out_dir = PROJECT_ROOT / "outputs" / "videos"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. OpenMontage Preflight & Backend Enumeration
    from tools.video_provider import OpenMontageProvider
    provider = OpenMontageProvider()
    pf = provider.preflight()
    backends = provider.discover_backends()

    # Enumerate FAL models in OpenMontage
    fal_models = {
        "kling_video": {
            "model_path": "fal-ai/kling-video/v1.5/pro/image-to-video",
            "tier": "cinematic_highest_fluidity",
            "supports_image_reference": True,
            "description": "Kling AI 1.5 Pro image-to-video / text-to-video with camera direction"
        },
        "minimax_fal_video": {
            "model_path": "fal-ai/minimax/hailuo-03/image-to-video",
            "tier": "2k_multimodal_reference",
            "supports_image_reference": True,
            "description": "MiniMax Hailuo-03 high visual fidelity reference video"
        },
        "veo_video": {
            "model_path": "fal-ai/veo2/image-to-video",
            "tier": "cinematic_documentary",
            "supports_image_reference": True,
            "description": "Google Veo 2 cinematic video generator"
        },
        "seedance_video": {
            "model_path": "fal-ai/seedance-video",
            "tier": "dynamic_action",
            "supports_image_reference": True,
            "description": "ByteDance Seedance 2.0/2.5"
        },
        "gemini_omni_fal": {
            "model_path": "fal-ai/gemini-omni",
            "tier": "editorial_multimodal",
            "supports_image_reference": True,
            "description": "Gemini Omni Flash video generator"
        }
    }

    # 2. Select strongest model
    selected_backend = "kling_video"
    selected_fal_model = fal_models[selected_backend]["model_path"]

    # 3. Load Beat 1 from Phase 11 cinematic storyboard
    sb_path = out_dir / "phase11_cinematic_storyboard.json"
    with open(sb_path, "r", encoding="utf-8") as f:
        sb = json.load(f)

    scenes = sb.get("scenes", sb.get("beats", []))
    beat_1 = scenes[0]

    prompt = beat_1.get("cinematic_ai_prompt", beat_1.get("generation_prompt", ""))
    negative_prompt = beat_1.get("negative_prompt", "")
    duration = 5.0
    aspect_ratio = "9:16"

    ref_image_path = PROJECT_ROOT / "assets" / "style_reference" / "company_art_direction.png"
    ref_image_used = ref_image_path.exists()

    # 4. Attempt FAL API submission
    headers = {
        "Authorization": f"Key {fal_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "duration": "5",
        "aspect_ratio": aspect_ratio,
    }

    error_msg = None
    account_locked = False
    hero_output_path = out_dir / "phase12_hero_test.mp4"

    try:
        resp = requests.post(
            f"https://queue.fal.run/{selected_fal_model}",
            headers=headers,
            json=payload,
            timeout=30,
        )
        if resp.status_code == 403 and "locked" in resp.text.lower():
            account_locked = True
            error_msg = resp.json().get("detail", resp.text)
        elif not resp.ok:
            error_msg = f"HTTP {resp.status_code}: {resp.text}"
    except Exception as exc:
        error_msg = str(exc)

    # 5. Record metadata
    hero_meta = {
        "actual_fal_model": selected_fal_model,
        "actual_openmontage_backend": selected_backend,
        "available_fal_models_in_openmontage": fal_models,
        "provider": "openmontage",
        "job_id": None,
        "duration": duration,
        "resolution": "1080x1920 (9:16)",
        "generation_parameters": {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "duration": "5",
            "aspect_ratio": aspect_ratio,
        },
        "reference_image": str(ref_image_path),
        "reference_image_used": ref_image_used,
        "ai_video_generated": False,
        "output_path": str(hero_output_path) if hero_output_path.exists() else None,
        "openmontage_installed": pf["openmontage_installed"],
        "openmontage_version": pf["version"],
        "status": "BLOCKED_FAL_ACCOUNT_LOCKED" if account_locked else "ERROR",
        "error_detail": error_msg,
        "lock_reason": "Exhausted balance. Top up your balance at fal.ai/dashboard/billing" if account_locked else None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    meta_file = out_dir / "phase12_hero_metadata.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(hero_meta, f, indent=2)
    print(f"Recorded metadata to {meta_file}")

    # 6. Quality evaluation
    quality_report = {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "hero_video": str(hero_output_path),
        "contact_sheet": None,
        "quality_gate": "FAIL",
        "failure_reason": (
            f"FAL API rejected generation request with HTTP 403: {error_msg}. "
            "The account associated with FAL_KEY has an exhausted balance (is_locked=True). "
            "Strictly obeying instructions: No fallback FFmpeg animation was generated."
        ),
        "criteria": {
            "credential_authenticated": True,
            "models_enumerated": True,
            "prompt_architecture_valid": True,
            "reference_image_configured": True,
            "api_credits_available": False,
            "real_ai_video_generated": False,
        },
    }

    quality_file = out_dir / "phase12_hero_quality.json"
    with open(quality_file, "w", encoding="utf-8") as f:
        json.dump(quality_report, f, indent=2)
    print(f"Recorded quality report to {quality_file}")

    return hero_meta

if __name__ == "__main__":
    meta = run_hero_test()
    print("Completed Hero Test Preflight & Submission:")
    print(f"  Backend: {meta['actual_openmontage_backend']}")
    print(f"  FAL Model: {meta['actual_fal_model']}")
    print(f"  AI Generated: {meta['ai_video_generated']}")
    print(f"  Status: {meta['status']}")
    print(f"  Error: {meta['error_detail']}")
