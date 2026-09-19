"""OpenMontage Tool for composition, timeline orchestration, and rendering.

Interfaces with the OpenMontage video production architecture.
Maintains timeline metadata and delegates to OpenMontage or high-performance FFmpeg fallback.
Compatible with Python 3.10.
"""

import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from config.settings import get_settings
from tools.ffmpeg_tool import FFmpegTool

logger = logging.getLogger(__name__)


class OpenMontageTool:
    """Tool for structuring OpenMontage projects and compiling final multi-track video advertisements."""

    def __init__(
        self,
        bin_path: Optional[str] = None,
        ffmpeg_tool: Optional[FFmpegTool] = None,
    ):
        settings = get_settings()
        self.bin_path = bin_path or settings.openmontage_bin_path
        self.ffmpeg = ffmpeg_tool or FFmpegTool()
        self.is_installed = self._check_openmontage_installed()

    def _check_openmontage_installed(self) -> bool:
        """Verify whether OpenMontage binary or CLI is accessible."""
        if self.bin_path and Path(self.bin_path).exists():
            return True
        found = shutil.which("openmontage") is not None
        return found

    def create_project_manifest(
        self,
        concept_id: str,
        project_dir: Path,
        scenes: List[Dict[str, Any]],
        video_clips: List[Path],
        voiceover_track: Optional[Path],
        music_track: Optional[Path],
        sfx_tracks: List[Dict[str, Any]],
        total_duration: float,
        resolution: Tuple[int, int] = (1080, 1920),
        fps: int = 30,
    ) -> Path:
        """Create a complete OpenMontage project and timeline manifest."""
        project_dir.mkdir(parents=True, exist_ok=True)
        manifest_file = project_dir / "openmontage_project.json"

        timeline_tracks = {
            "video_track": [
                {
                    "scene_id": s.get("scene_id"),
                    "clip_path": str(c.resolve()) if c.exists() else None,
                    "start_time": s.get("start_time", 0),
                    "duration": s.get("duration", 4),
                    "transition": s.get("transition", "hard_cut"),
                    "generation_method": s.get("generation_method", "ai_video"),
                }
                for s, c in zip(scenes, video_clips)
            ],
            "audio_tracks": {
                "voiceover": {
                    "path": str(voiceover_track.resolve()) if voiceover_track and voiceover_track.exists() else None,
                    "volume_db": 0.0,
                },
                "music": {
                    "path": str(music_track.resolve()) if music_track and music_track.exists() else None,
                    "volume_db": -20.0,
                    "ducking_db": -26.0,
                },
                "sfx": sfx_tracks,
            },
        }

        project_manifest = {
            "version": "1.0",
            "system": "OpenMontage Agentic Video Framework",
            "project_id": concept_id,
            "format": {
                "width": resolution[0],
                "height": resolution[1],
                "aspect_ratio": "9:16",
                "fps": fps,
                "duration_sec": total_duration,
            },
            "timeline": timeline_tracks,
            "status": "ready_to_render",
        }

        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(project_manifest, f, indent=2, ensure_ascii=False)

        return manifest_file

    def render_final_ad(
        self,
        concept_id: str,
        montage_dir: Path,
        scenes: List[Dict[str, Any]],
        video_clips: List[Path],
        voiceover_track: Optional[Path],
        music_track: Optional[Path],
        sfx_tracks: List[Dict[str, Any]],
        total_duration: float,
        output_mp4: Path,
    ) -> Dict[str, Any]:
        """Render the complete video advertisement through OpenMontage or clean FFmpeg fallback."""
        output_mp4.parent.mkdir(parents=True, exist_ok=True)
        manifest_path = self.create_project_manifest(
            concept_id=concept_id,
            project_dir=montage_dir,
            scenes=scenes,
            video_clips=video_clips,
            voiceover_track=voiceover_track,
            music_track=music_track,
            sfx_tracks=sfx_tracks,
            total_duration=total_duration,
        )

        engine_used = "FFmpeg Production Engine (OpenMontage Fallback)"

        # If OpenMontage binary is directly available, attempt native invocation
        if self.is_installed and self.bin_path:
            try:
                cmd = [self.bin_path, "render", "--project", str(manifest_path), "--output", str(output_mp4)]
                subprocess.run(cmd, check=True)
                engine_used = "Native OpenMontage CLI"
                return {
                    "success": True,
                    "engine": engine_used,
                    "manifest_path": str(manifest_path),
                    "output_path": str(output_mp4),
                }
            except Exception as e:
                logger.warning("OpenMontage native render failed: %s. Falling back to FFmpeg engine.", str(e))

        # Standard robust execution: Concatenate scene clips, mix multi-track audio, and encode H.264
        concat_video = montage_dir / "temp_video_track.mp4"
        self.ffmpeg.concatenate_scene_clips(
            clip_paths=video_clips,
            output_path=concat_video,
            width=1080,
            height=1920,
            fps=30,
        )

        self.ffmpeg.mix_cinematic_audio(
            video_track=concat_video,
            voiceover_track=voiceover_track,
            music_track=music_track,
            sfx_tracks=sfx_tracks,
            output_path=output_mp4,
            target_duration=total_duration,
        )

        concat_video.unlink(missing_ok=True)

        return {
            "success": True,
            "engine": engine_used,
            "manifest_path": str(manifest_path),
            "output_path": str(output_mp4),
        }
