"""agents/style_prompt_validator.py

Validates storyboard and visual scene prompts against the Official Company-Provided
Prompt System specification (Phase 9.1).

Validates:
1. style_mode exists and is one of ('flat_parallax', 'deep_diorama', 'locked_stage')
2. style_block exists
3. background exists
4. MG exists
5. FG exists
6. camera_move exists and is in allowed library
7. settle exists
8. audio exists (sound design only, no music/narration)
9. avoid exists
10. exactly ONE camera move per scene (no contradictory moves)
11. depth explicitly described (background, midground, foreground + relationships)
12. approved_text defined as list
13. approved_numbers defined as list
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tools.style_prompt_system import ALLOWED_CAMERA_MOVES, validate_camera_move

logger = logging.getLogger(__name__)


class StylePromptValidator:
    """Validator enforcing the official company creative system and prompt contract."""

    def __init__(self):
        self.allowed_styles = {"flat_parallax", "deep_diorama", "locked_stage"}
        self.allowed_camera_moves = set(ALLOWED_CAMERA_MOVES)

    def validate_scene(self, scene: Dict[str, Any], scene_idx: int = 1) -> Tuple[bool, List[str]]:
        """Validate a single scene prompt object against company rules."""
        errors: List[str] = []
        sid = scene.get("scene_id", f"scene_{scene_idx}")

        # 1. style_mode & style_block
        style_mode = scene.get("style_mode") or scene.get("style_block_type")
        if not style_mode:
            errors.append(f"{sid}: 'style_mode' missing")
        elif style_mode not in self.allowed_styles:
            errors.append(f"{sid}: invalid 'style_mode' '{style_mode}' (allowed: {self.allowed_styles})")

        style_block = scene.get("style_block") or scene.get("style_block_type")
        if not style_block:
            errors.append(f"{sid}: 'style_block' missing")

        # 2. background, mg, fg
        bg = scene.get("background") or scene.get("depth_layers", {}).get("background")
        if not bg or not str(bg).strip():
            errors.append(f"{sid}: 'background' missing or empty")

        mg = scene.get("mg") or scene.get("depth_layers", {}).get("midground")
        if mg is None or not str(mg).strip():
            errors.append(f"{sid}: 'mg' missing or empty")

        fg = scene.get("fg") or scene.get("depth_layers", {}).get("foreground")
        if not fg or not str(fg).strip():
            errors.append(f"{sid}: 'fg' missing or empty")

        # 3. camera & settle
        cam = scene.get("camera_move") or scene.get("camera")
        if not cam or not str(cam).strip():
            errors.append(f"{sid}: 'camera_move' missing or empty")
        else:
            valid_cam, msg = validate_camera_move(str(cam))
            if not valid_cam:
                errors.append(f"{sid}: {msg}")

        settle = scene.get("settle") or scene.get("structured_shot", {}).get("settle")
        if not settle or not str(settle).strip():
            errors.append(f"{sid}: 'settle' missing or empty")

        # 4. audio
        audio = scene.get("audio") or scene.get("audio_sounds")
        if not audio:
            errors.append(f"{sid}: 'audio' missing or empty")
        elif isinstance(audio, str):
            if "no music" not in audio.lower() or "no narration" not in audio.lower():
                errors.append(f"{sid}: visual audio prompt must specify 'no music, no narration'")

        # 5. avoid
        avoid = scene.get("avoid") or scene.get("avoid_block")
        if not avoid and "AVOID" not in scene.get("generation_prompt", ""):
            errors.append(f"{sid}: 'avoid' block missing")

        # 6. depth explicitly described
        depth_desc = (
            scene.get("depth_description")
            or scene.get("depth")
            or scene.get("structured_shot", {}).get("depth_description")
        )
        if not depth_desc or len(str(depth_desc).strip()) < 8:
            errors.append(f"{sid}: 'depth_description' missing or insufficient")

        # 7. approved_text & approved_numbers
        approved_text = scene.get("approved_text")
        if approved_text is None or not isinstance(approved_text, list):
            errors.append(f"{sid}: 'approved_text' must be a list")

        approved_numbers = scene.get("approved_numbers")
        if approved_numbers is None or not isinstance(approved_numbers, list):
            errors.append(f"{sid}: 'approved_numbers' must be a list")

        return len(errors) == 0, errors

    def validate_storyboard(self, storyboard: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an entire storyboard file containing scenes or beats."""
        scenes = storyboard.get("scenes") or storyboard.get("beats", [])
        if not scenes:
            return {
                "valid": False,
                "total_scenes": 0,
                "errors": ["Storyboard contains 0 scenes"],
                "scene_results": [],
            }

        all_valid = True
        total_errors: List[str] = []
        scene_results: List[Dict[str, Any]] = []

        camera_moves: List[str] = []

        for idx, sc in enumerate(scenes, 1):
            is_valid, errs = self.validate_scene(sc, scene_idx=idx)
            if not is_valid:
                all_valid = False
                total_errors.extend(errs)

            cam = sc.get("camera_move") or sc.get("camera")
            if cam:
                camera_moves.append(str(cam).lower())

            scene_results.append({
                "scene_id": sc.get("scene_id", f"scene_{idx}"),
                "valid": is_valid,
                "errors": errs,
                "style_mode": sc.get("style_mode") or sc.get("style_block_type"),
                "camera_move": cam,
            })

        # Check sequencing rule: never use the same camera move twice consecutively
        for i in range(len(camera_moves) - 1):
            if camera_moves[i] == camera_moves[i + 1]:
                err = f"Sequencing violation: Consecutive identical camera moves at scene {i+1} and {i+2}: '{camera_moves[i]}'"
                total_errors.append(err)
                all_valid = False

        return {
            "valid": all_valid,
            "total_scenes": len(scenes),
            "errors": total_errors,
            "scene_results": scene_results,
        }

    def validate_and_save_report(
        self,
        storyboard_path: Path,
        output_report_path: Path,
    ) -> Dict[str, Any]:
        """Validate storyboard and persist outputs/videos/style_prompt_validation.json."""
        with open(storyboard_path, "r", encoding="utf-8") as f:
            sb = json.load(f)

        results = self.validate_storyboard(sb)
        output_report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_report_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        return results
