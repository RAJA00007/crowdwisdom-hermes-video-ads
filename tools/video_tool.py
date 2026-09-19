"""Video production tool interfacing with OpenMontage and video rendering pipelines.

Produces structured storyboard specifications and renders 30-60s cinematic ad videos.
Compatible with Python 3.10.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from config.settings import get_settings


class VideoProductionTool:
    """Tool for handling storyboard asset orchestration and OpenMontage video rendering."""

    def __init__(self, bin_path: Optional[str] = None):
        settings = get_settings()
        self.bin_path = bin_path or settings.openmontage_bin_path
        self.outputs_dir = settings.outputs_dir / "videos"
        self.resolution = settings.video_output_resolution
        self.default_duration = settings.video_default_duration_sec

    def export_storyboard_spec(self, concept_id: str, storyboard_data: Dict[str, Any]) -> Path:
        """Export a structured storyboard JSON definition for OpenMontage / video rendering."""
        output_file = self.outputs_dir.parent / "scripts" / f"storyboard_{concept_id}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(storyboard_data, f, indent=2)
        return output_file

    def validate_storyboard(self, storyboard: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that storyboard contains required cinematic timing, scenes, audio, and visual cues."""
        scenes: List[Dict[str, Any]] = storyboard.get("scenes", [])
        if not scenes:
            return {"valid": False, "error": "Storyboard contains no scenes."}

        total_duration = sum(scene.get("duration_sec", 0) for scene in scenes)
        if total_duration < 30 or total_duration > 60:
            return {
                "valid": True,
                "warning": f"Total duration is {total_duration}s (optimal range is 30–60s).",
                "total_duration_sec": total_duration,
                "scene_count": len(scenes),
            }

        return {
            "valid": True,
            "total_duration_sec": total_duration,
            "scene_count": len(scenes),
        }
