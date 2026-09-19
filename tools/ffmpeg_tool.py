"""FFmpeg Tool for cinematic video composition, audio mixing, and encoding.

Handles frame-rate normalization, scaling to 1080x1920 (9:16 vertical), camera motion,
audio mixing with ducking, transitions, and H.264 MP4 export.
Compatible with Python 3.10.
"""

import json
import logging
import math
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class FFmpegTool:
    """Production-grade FFmpeg video finishing and assembly engine."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg_path = self._discover_ffmpeg(ffmpeg_path)

    def _discover_ffmpeg(self, custom_path: Optional[str] = None) -> str:
        """Find the executable path for FFmpeg."""
        if custom_path and Path(custom_path).exists():
            return str(Path(custom_path).resolve())

        # Check virtual environment Scripts
        venv_ffmpeg = Path(__file__).resolve().parent.parent.parent / ".venv" / "Scripts" / "ffmpeg.exe"
        if venv_ffmpeg.exists():
            return str(venv_ffmpeg.resolve())

        # Check imageio_ffmpeg
        try:
            import imageio_ffmpeg
            exe = imageio_ffmpeg.get_ffmpeg_exe()
            if Path(exe).exists():
                return exe
        except Exception:
            pass

        # Check system PATH
        system_exe = shutil.which("ffmpeg")
        if system_exe:
            return system_exe

        return "ffmpeg"

    def get_video_info(self, video_path: Any) -> Dict[str, Any]:
        """Extract duration, resolution, fps, and audio channels using ffprobe or ffmpeg."""
        path_obj = Path(video_path)
        result = {
            "path": str(path_obj),
            "exists": path_obj.exists(),
            "duration": 0.0,
            "width": 1080,
            "height": 1920,
            "fps": 30.0,
            "has_audio": False,
        }
        if not path_obj.exists():
            return result

        try:
            cmd = [
                self.ffmpeg_path,
                "-i", str(path_obj),
                "-hide_banner",
            ]
            p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
            output = p.stderr

            import re
            # Extract duration
            dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", output)
            if dur_match:
                hours, minutes, seconds = dur_match.groups()
                result["duration"] = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

            # Extract resolution
            res_match = re.search(r"(\d{3,4})x(\d{3,4})", output)
            if res_match:
                result["width"] = int(res_match.group(1))
                result["height"] = int(res_match.group(2))

            # Extract fps
            fps_match = re.search(r"(\d+(?:\.\d+)?)\s*fps", output)
            if fps_match:
                result["fps"] = float(fps_match.group(1))

            # Check audio
            if "Audio:" in output:
                result["has_audio"] = True

        except Exception as e:
            logger.warning("Error getting video info: %s", str(e))

        return result

    def create_cinematic_motion_clip(
        self,
        image_path: Path,
        output_path: Path,
        duration: float,
        motion: str = "slow_dolly_in",
        width: int = 1080,
        height: int = 1920,
        fps: int = 30,
    ) -> Path:
        """Transform a static high-res image into a 1080x1920 cinematic clip with camera movement."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        total_frames = int(duration * fps)

        # Build dynamic zoompan filter based on requested camera movement
        scale_prefix = f"scale={width*2}:{height*2}:force_original_aspect_ratio=increase,crop={width*2}:{height*2}"
        if motion in ("slow_dolly_in", "dolly_in", "push_in", "zoom_in"):
            # Subtle documentary push-in with 1.0 -> 1.08 scale
            vf = (
                f"{scale_prefix},"
                f"zoompan=z='min(zoom+0.0006,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s={width}x{height}:fps={fps},"
                f"format=yuv420p"
            )
        elif motion in ("slow_dolly_out", "dolly_out", "push_out", "zoom_out"):
            # Smooth 1.08 -> 1.0 zoom out
            vf = (
                f"{scale_prefix},"
                f"zoompan=z='if(lte(zoom,1.0),1.08,max(1.001,zoom-0.0006))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s={width}x{height}:fps={fps},"
                f"format=yuv420p"
            )
        else:
            # Subtle natural breathing motion
            vf = (
                f"{scale_prefix},"
                f"zoompan=z='1.03+0.02*sin(2*PI*in/{total_frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s={width}x{height}:fps={fps},"
                f"format=yuv420p"
            )


        cmd = [
            self.ffmpeg_path,
            "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-t", str(duration),
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            "-movflags", "+faststart",
            str(output_path),
        ]

        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        if p.returncode != 0:
            logger.error("FFmpeg motion clip error: %s", p.stderr)
            # Fallback simpler static scale
            fallback_cmd = [
                self.ffmpeg_path, "-y", "-loop", "1", "-i", str(image_path),
                "-t", str(duration),
                "-vf", f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},format=yuv420p",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
                "-movflags", "+faststart",
                str(output_path)
            ]
            subprocess.run(fallback_cmd, check=True)

        return output_path

    def concatenate_scene_clips(
        self,
        clip_paths: List[Path],
        output_path: Path,
        width: int = 1080,
        height: int = 1920,
        fps: int = 30,
    ) -> Path:
        """Concatenate individual scene clips into a single video track with normalized specs."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        concat_list_file = output_path.parent / "concat_list.txt"

        with open(concat_list_file, "w", encoding="utf-8") as f:
            for clip in clip_paths:
                # Escape backslashes for FFmpeg on Windows
                clean_path = str(clip.resolve()).replace("\\", "/")
                f.write(f"file '{clean_path}'\n")

        cmd = [
            self.ffmpeg_path,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_file),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black",
            "-movflags", "+faststart",
            str(output_path),
        ]

        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        if p.returncode != 0:
            logger.error("Concat error: %s", p.stderr)
            raise RuntimeError(f"FFmpeg concat failed: {p.stderr}")

        if concat_list_file.exists():
            concat_list_file.unlink(missing_ok=True)

        return output_path

    def mix_cinematic_audio(
        self,
        video_track: Path,
        voiceover_track: Optional[Path],
        music_track: Optional[Path],
        sfx_tracks: Any,
        output_path: Path,
        target_duration: float,
        target_lufs: float = -17.0,
        target_tp: float = -1.5,
    ) -> Path:
        """Professional 3-track editorial audio mixing with sidechain ducking and broadcast mastering.

        TRACK 1 = Narration (normalized, clean, front of mix)
        TRACK 2 = Music (sidechain ducked -8dB during narration)
        TRACK 3 = SFX (clean, synchronized, crisp transients)

        Mastering: High-pass (80Hz) -> De-esser/EQ -> Compressor -> Loudness Normalization (~ -17 LUFS, <= -1 dBTP) -> Limiter.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        inputs = ["-i", str(video_track)]
        filter_complex = []
        input_index = 1

        has_vo = voiceover_track and Path(voiceover_track).exists()
        has_music = music_track and Path(music_track).exists()

        # Handle SFX track (can be Path or list of dicts)
        sfx_wav_path: Optional[Path] = None
        if isinstance(sfx_tracks, (str, Path)) and Path(sfx_tracks).exists():
            sfx_wav_path = Path(sfx_tracks)
        has_sfx = sfx_wav_path is not None

        vo_label = None
        if has_vo:
            inputs.extend(["-i", str(voiceover_track)])
            vo_idx = input_index
            input_index += 1
            # Split VO into mix stream and sidechain trigger stream
            filter_complex.append(f"[{vo_idx}:a]aformat=channel_layouts=stereo:sample_rates=44100,volume=1.0,asplit=2[vo_mix][vo_sc]")
            vo_label = "[vo_mix]"

        music_label = None
        if has_music:
            inputs.extend(["-stream_loop", "-1", "-i", str(music_track)])
            music_idx = input_index
            input_index += 1
            filter_complex.append(f"[{music_idx}:a]aformat=channel_layouts=stereo:sample_rates=44100,volume=0.22[music_raw]")

            if has_vo:
                # Apply sidechain compression ducking: dips music by ~8dB when VO is active
                filter_complex.append(
                    "[music_raw][vo_sc]sidechaincompress=threshold=0.035:ratio=4.5:attack=40:release=350[ducked_music]"
                )
                music_label = "[ducked_music]"
            else:
                music_label = "[music_raw]"

        sfx_label = None
        if has_sfx:
            inputs.extend(["-i", str(sfx_wav_path)])
            sfx_idx = input_index
            input_index += 1
            filter_complex.append(f"[{sfx_idx}:a]aformat=channel_layouts=stereo:sample_rates=44100,volume=0.75[sfx_clean]")
            sfx_label = "[sfx_clean]"
        elif isinstance(sfx_tracks, list):
            # Fallback for individual sfx dicts
            sfx_sources = []
            for sfx in sfx_tracks:
                sf = sfx.get("path")
                st = sfx.get("time_sec", 0.0)
                if sf and Path(sf).exists():
                    inputs.extend(["-i", str(sf)])
                    d_ms = int(st * 1000)
                    filter_complex.append(
                        f"[{input_index}:a]adelay={d_ms}|{d_ms},volume=0.35,aformat=channel_layouts=stereo:sample_rates=44100[sfx{input_index}]"
                    )
                    sfx_sources.append(f"[sfx{input_index}]")
                    input_index += 1
            if sfx_sources:
                filter_complex.append(f"{''.join(sfx_sources)}amix=inputs={len(sfx_sources)}:dropout_transition=2[sfx_clean]")
                sfx_label = "[sfx_clean]"

        # Collect active mix tracks
        mix_inputs = []
        if vo_label:
            mix_inputs.append(vo_label)
        if music_label:
            mix_inputs.append(music_label)
        if sfx_label:
            mix_inputs.append(sfx_label)

        if mix_inputs:
            mix_chain = (
                f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=2,"
                "highpass=f=80,"
                "equalizer=f=6000:t=q:w=2:g=-2,"
                "acompressor=threshold=-18dB:ratio=2.5:attack=15:release=120,"
                f"loudnorm=I={target_lufs}:TP={target_tp}:LRA=11,"
                "volume=0.95[aout]"
            )
            filter_complex.append(mix_chain)

            cmd = [
                self.ffmpeg_path,
                "-y",
                *inputs,
                "-t", str(target_duration),
                "-filter_complex", ";".join(filter_complex),
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "256k",
                "-ar", "44100",
                "-movflags", "+faststart",
                str(output_path),
            ]
        else:
            # Silent fallback
            cmd = [
                self.ffmpeg_path,
                "-y",
                *inputs,
                "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
                "-t", str(target_duration),
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-movflags", "+faststart",
                str(output_path),
            ]

        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        if p.returncode != 0:
            logger.error("Audio mixing error: %s", p.stderr)
            raise RuntimeError(f"FFmpeg audio mixing failed: {p.stderr}")

        return output_path
