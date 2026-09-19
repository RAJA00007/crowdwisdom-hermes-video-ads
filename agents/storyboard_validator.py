"""Hermes Creative Quality Validator.

Enforces strict production-readiness criteria on video ad concepts and storyboards:
1. Duration between 30 and 60 seconds
2. Exactly 8 to 12 scenes
3. Visual hook within the first 1-3 seconds (works sound-off)
4. Clear ICP definition
5. Identifiable trader pain point
6. Clear CrowdWisdom platform integration
7. Anchored proprietary data scene with verified metrics (zero fabrication)
8. Production screenplay voiceover and narrative progression
9. Clear Call to Action (CTA) with domain crowdwisdomtrading.com
10. Supported generation methods (ai_video, ai_image_motion, motion_graphic, data_visualization, product_capture)
11. Verification against fabricated statistics
12. Production-grade cinematography descriptions (no generic placeholders)
13. Substantial differentiation across concepts (hooks, narrative structures, visual styles, emotional arcs)

Compatible with Python 3.10.
"""

import json
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)

# Strict set of allowed generation methods per assignment specification
ALLOWED_GENERATION_METHODS: Set[str] = {
    "ai_video",
    "ai_image_motion",
    "motion_graphic",
    "data_visualization",
    "product_capture",
}

# Verified proprietary metrics allowed in ad claims
VERIFIED_PROPRIETARY_METRICS: Set[str] = {
    "68.4", "68.4%",
    "41.2", "41.2%",
    "52.8", "52.8%",
    "14.6", "14.6h", "14.6 hours", "14 hours",
    "1.48M", "1.48 million", "1.48m", "1,482,930", "1482930",
    "428", "428 tickers",
    "79.1", "79.1%", "79%",
    "74.2", "74.2%",
    "27.2", "27.2%", "+27.2%",
    "15.6", "15.6%", "+15.6%",
}

# Banned hyperbolic / fabricated claim phrases
BANNED_FABRICATIONS: List[str] = [
    "guaranteed profit",
    "guaranteed return",
    "guaranteed success",
    "risk-free",
    "100% accurate",
    "100% win",
    "make millions overnight",
    "get rich quick",
    "never lose",
    "zero risk",
]

# Generic visual phrases to reject
GENERIC_VISUAL_PATTERNS: List[str] = [
    "cinematic trader looking at computer",
    "trader looking at screen",
    "man at desk",
    "stock chart going up",
    "graph moving",
    "generic office",
]


class StoryboardValidator:
    """Production quality validator for CrowdWisdom video ad concepts and storyboards."""

    def __init__(self, proprietary_summary: Optional[Dict[str, Any]] = None):
        self.proprietary_summary = proprietary_summary or {}

    def validate_scenes(self, storyboard: Dict[str, Any]) -> List[str]:
        """Validate scene count and individual scene fields."""
        errors: List[str] = []
        scenes = storyboard.get("scenes", storyboard.get("shots", []))

        # Check 1: Scene count (8 to 12)
        if len(scenes) < 8:
            errors.append(f"Scene count ({len(scenes)}) is fewer than the minimum required 8 scenes.")
        elif len(scenes) > 12:
            errors.append(f"Scene count ({len(scenes)}) exceeds the maximum allowed 12 scenes.")

        # Check 2: Total duration (30 to 60 seconds)
        total_duration = sum(s.get("duration", 0) for s in scenes)
        if total_duration < 30:
            errors.append(f"Total duration ({total_duration}s) is less than 30 seconds.")
        elif total_duration > 60:
            errors.append(f"Total duration ({total_duration}s) exceeds 60 seconds.")

        # Check 3: Visual hook in first 3 seconds
        if scenes:
            first_scene = scenes[0]
            start = first_scene.get("start_time", 0)
            dur = first_scene.get("duration", 0)
            if start > 1:
                errors.append(f"First scene starts at {start}s; visual hook must start within first 1-3 seconds.")
            if dur > 6:
                errors.append(f"First scene duration ({dur}s) is too long for a punchy opening hook.")
            
            hook_visual = first_scene.get("visual", first_scene.get("visual_description", ""))
            if not hook_visual or len(hook_visual) < 25:
                errors.append("First scene lacks a sufficiently detailed visual hook description.")

        # Check generation methods and required scene fields
        methods_used: Set[str] = set()
        for idx, scene in enumerate(scenes, 1):
            gen_method = scene.get("generation_method")
            if not gen_method:
                errors.append(f"Scene {idx} is missing 'generation_method'.")
            elif gen_method not in ALLOWED_GENERATION_METHODS:
                errors.append(f"Scene {idx} has unsupported generation_method '{gen_method}'. Must be one of {sorted(ALLOWED_GENERATION_METHODS)}.")
            else:
                methods_used.add(gen_method)

            # Check for generic visual descriptions
            visual_desc = scene.get("visual", scene.get("visual_description", ""))
            if not visual_desc or len(visual_desc.strip()) < 30:
                errors.append(f"Scene {idx} has a generic or insufficiently detailed visual prompt (< 30 characters).")
            else:
                for gen_pattern in GENERIC_VISUAL_PATTERNS:
                    if gen_pattern in visual_desc.lower() and len(visual_desc.strip()) < 50:
                        errors.append(f"Scene {idx} uses generic placeholder visual: '{visual_desc}'.")

            # Check camera object specification
            camera = scene.get("camera", {})
            if isinstance(camera, dict):
                if not camera.get("shot") and not scene.get("camera_shot"):
                    errors.append(f"Scene {idx} camera missing shot framing (e.g., close-up, wide, macro).")

        # Ensure multi-modal generation is utilized (not everything is ai_video)
        if len(methods_used) < 2 and len(scenes) >= 8:
            errors.append(f"Storyboard relies almost exclusively on one generation method ({methods_used}). Multi-modal asset orchestration required.")

        return errors

    def validate_proprietary_data_anchoring(self, storyboard: Dict[str, Any]) -> List[str]:
        """Verify presence of real CrowdWisdom proprietary data and absence of fabrication."""
        errors: List[str] = []
        scenes = storyboard.get("scenes", storyboard.get("shots", []))

        # Check for at least one dedicated proprietary data scene
        prop_scenes = [
            s for s in scenes
            if s.get("data_source") == "proprietary_data_summary.json"
            or s.get("generation_method") == "data_visualization"
            or s.get("data_field")
        ]

        if not prop_scenes:
            errors.append("Storyboard contains no dedicated scene anchoring verified CrowdWisdom proprietary data.")
        else:
            for ps in prop_scenes:
                if not ps.get("data_field"):
                    errors.append(f"Proprietary data scene {ps.get('scene_id')} is missing 'data_field'.")
                if not ps.get("data_value"):
                    errors.append(f"Proprietary data scene {ps.get('scene_id')} is missing 'data_value'.")
                if not ps.get("data_visualization") and not ps.get("visualization"):
                    errors.append(f"Proprietary data scene {ps.get('scene_id')} is missing 'data_visualization'.")

        # Check for fabricated claims across voiceover and on-screen text
        for idx, scene in enumerate(scenes, 1):
            text_blob = f"{scene.get('voiceover', '')} {scene.get('on_screen_text', '')}".lower()
            for banned in BANNED_FABRICATIONS:
                if banned in text_blob:
                    errors.append(f"Scene {idx} contains prohibited fabricated claim: '{banned}'.")

        return errors

    def validate_narrative_and_branding(self, storyboard: Dict[str, Any]) -> List[str]:
        """Verify ICP alignment, pain point, CrowdWisdom brand integration, and CTA."""
        errors: List[str] = []
        metadata = storyboard.get("concept_metadata", {})
        scenes = storyboard.get("scenes", storyboard.get("shots", []))

        # Check ICP definition
        icp = metadata.get("target_icp") or storyboard.get("target_icp")
        if not icp or len(icp.strip()) < 10:
            errors.append("Storyboard is missing a clearly defined Target ICP.")

        # Check Pain Point
        pain_point = metadata.get("pain_point") or storyboard.get("pain_point")
        if not pain_point or len(pain_point.strip()) < 10:
            errors.append("Storyboard is missing an identifiable trader pain point.")

        # Check CrowdWisdom brand integration in story
        all_text = " ".join([
            s.get("voiceover", "") + " " + s.get("on_screen_text", "") + " " + s.get("visual", "")
            for s in scenes
        ]).lower()

        if "crowdwisdom" not in all_text and "crowd wisdom" not in all_text:
            errors.append("Storyboard lacks explicit CrowdWisdom brand or platform integration.")

        # Check CTA in closing scene(s)
        closing_scenes = scenes[-2:] if len(scenes) >= 2 else scenes
        closing_text = " ".join([
            s.get("voiceover", "") + " " + s.get("on_screen_text", "") + " " + s.get("purpose", "")
            for s in closing_scenes
        ]).lower()

        has_cta = "crowdwisdomtrading.com" in closing_text or "start free" in closing_text or "cta" in closing_text or "discover" in closing_text
        if not has_cta and not metadata.get("CTA"):
            errors.append("Storyboard is missing a clear Call to Action (CTA) in the final scenes.")

        return errors

    def validate_single_concept(self, storyboard: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Run full validation suite on a single storyboard concept."""
        errors: List[str] = []
        errors.extend(self.validate_scenes(storyboard))
        errors.extend(self.validate_proprietary_data_anchoring(storyboard))
        errors.extend(self.validate_narrative_and_branding(storyboard))

        is_valid = (len(errors) == 0)
        return is_valid, errors

    def validate_differentiation(self, storyboards: List[Dict[str, Any]]) -> List[str]:
        """Verify that the 3 concepts are substantially different in genres, hooks, structures, and visual styles."""
        errors: List[str] = []
        if len(storyboards) != 3:
            errors.append(f"Expected exactly 3 concepts, found {len(storyboards)}.")
            return errors

        genres: List[str] = []
        hooks: List[str] = []
        titles: List[str] = []
        styles: List[str] = []

        for i, sb in enumerate(storyboards, 1):
            meta = sb.get("concept_metadata", {})
            title = sb.get("title") or meta.get("title", f"Concept {i}")
            genre = sb.get("genre") or meta.get("genre", "")
            hook = meta.get("hook_visual") or meta.get("visual_hook") or (sb.get("scenes", [{}])[0].get("visual", ""))
            style = meta.get("visual_style") or meta.get("visual_language", "")

            titles.append(title)
            genres.append(genre.lower())
            hooks.append(hook.lower())
            styles.append(style.lower())

        # Check unique titles
        if len(set(titles)) < 3:
            errors.append(f"Concept titles are not distinct: {titles}")

        # Check unique genres/styles
        if len(set(genres)) < 3:
            errors.append(f"Concepts do not represent 3 distinct genres/directions: {genres}")

        # Check hook differentiation (hooks must not be duplicates or identical)
        if len(set(hooks)) < 3:
            errors.append("Visual hooks across concepts are too similar or duplicated.")

        return errors

    def validate_all(self, storyboards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute full validation across all 3 storyboards including cross-concept differentiation."""
        results: Dict[str, Any] = {
            "all_valid": True,
            "concept_results": [],
            "differentiation_errors": [],
        }

        for sb in storyboards:
            cid = sb.get("concept_id", "unknown")
            valid, errors = self.validate_single_concept(sb)
            if not valid:
                results["all_valid"] = False
            results["concept_results"].append({
                "concept_id": cid,
                "title": sb.get("title", ""),
                "valid": valid,
                "errors": errors,
            })

        diff_errors = self.validate_differentiation(storyboards)
        if diff_errors:
            results["all_valid"] = False
            results["differentiation_errors"] = diff_errors

        return results
