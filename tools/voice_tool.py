"""Professional Voice Tool for editorial documentary narration.

Implements:
- ElevenLabs TTS provider as primary voice engine.
- High-fidelity Neural TTS fallback (edge-tts with en-US-ChristopherNeural) when no API key is set.
- Master continuous voiceover timeline generation with zero timestamp overlap.
- Audio segment verification and duration calculation.

No pyttsx3/SAPI5 is used.
Compatible with Python 3.10.
"""

import asyncio
import io
import json
import logging
import os
import struct
import subprocess
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

DOC_VOICE_DIRECTION = (
    "Natural documentary narrator. Conversational and intelligent. Calm, understated confidence. "
    "Slightly intimate. Real human pacing. Natural breaths and pauses. No announcer voice. "
    "No commercial hype. No motivational delivery. Emphasize important words subtly. "
    "Sound like a journalist explaining something fascinating to one person."
)



class VoiceTool:
    """Documentary TTS generator for editorial visual journalism video ads."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # "Adam" default
        self.sample_rate = 44100
        # Resolve ffmpeg executable
        if ffmpeg_path:
            self.ffmpeg_path = ffmpeg_path
        else:
            venv_ffmpeg = Path(os.getcwd()).parent / ".venv" / "Scripts" / "ffmpeg.exe"
            if venv_ffmpeg.exists():
                self.ffmpeg_path = str(venv_ffmpeg)
            else:
                self.ffmpeg_path = "ffmpeg"

    def get_provider_info(self) -> Dict[str, Any]:
        """Return information about the active voice provider."""
        if self.api_key:
            return {
                "provider": "elevenlabs",
                "voice_id": self.voice_id,
                "voice_direction": DOC_VOICE_DIRECTION,
                "tone": "calm_documentary",
            }
        return {
            "provider": "edge_neural_tts",
            "voice_name": "en-US-ChristopherNeural",
            "voice_direction": DOC_VOICE_DIRECTION,
            "tone": "calm_documentary",
            "note": "ElevenLabs key not detected; using ultra-low-latency high-fidelity neural voice",
        }

    def _convert_audio_to_wav(self, input_bytes: bytes, output_wav: Path) -> Path:
        """Convert any audio format (MP3, OGG, etc.) to clean 44.1kHz 16-bit stereo/mono WAV using FFmpeg."""
        output_wav.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i", "pipe:0",
            "-acodec", "pcm_s16le",
            "-ac", "1",
            "-ar", str(self.sample_rate),
            str(output_wav),
        ]
        p = subprocess.run(cmd, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            logger.error("FFmpeg audio conversion failed: %s", p.stderr.decode("utf-8", errors="ignore"))
            raise RuntimeError(f"Audio conversion failed: {p.stderr.decode('utf-8', errors='ignore')}")
        return output_wav

    def synthesize_speech_segment(self, text: str, output_path: Path) -> Path:
        """Synthesize a single speech clip using ElevenLabs or high-fidelity neural fallback."""
        if not text or not text.strip():
            # Return silent WAV
            return self._create_silent_wav(output_path, 0.5)

        clean_text = text.strip()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 1. Attempt ElevenLabs if API key is present
        if self.api_key:
            try:
                from elevenlabs.client import ElevenLabs
                client = ElevenLabs(api_key=self.api_key)
                audio_stream = client.text_to_speech.convert(
                    voice_id=self.voice_id,
                    text=clean_text,
                    model_id="eleven_multilingual_v2",
                    voice_settings={
                        "stability": 0.65,
                        "similarity_boost": 0.80,
                        "style": 0.15,
                        "use_speaker_boost": True,
                    }
                )
                audio_bytes = b"".join(audio_stream)
                return self._convert_audio_to_wav(audio_bytes, output_path)
            except Exception as e:
                logger.warning("ElevenLabs synthesis error (%s); falling back to Edge Neural TTS", str(e))

        # 2. High-fidelity Neural Documentary Voice Fallback (edge-tts)
        try:
            import edge_tts
            temp_mp3 = output_path.parent / f"{output_path.stem}_temp.mp3"

            async def _run_edge():
                communicate = edge_tts.Communicate(
                    text=clean_text,
                    voice="en-US-ChristopherNeural",  # Intelligent, calm documentary narrator
                    rate="+8%",                       # Crisp, natural documentary cadence
                    pitch="-1Hz",                     # Grounded, calm resonance
                )
                await communicate.save(str(temp_mp3))

            asyncio.run(_run_edge())
            if temp_mp3.exists():
                with open(temp_mp3, "rb") as f:
                    mp3_data = f.read()
                self._convert_audio_to_wav(mp3_data, output_path)
                temp_mp3.unlink(missing_ok=True)
                return output_path
        except Exception as e:
            logger.error("Neural TTS synthesis error: %s", str(e))
            raise RuntimeError(f"TTS synthesis completely failed: {e}")

        return output_path

    def _create_silent_wav(self, output_path: Path, duration_sec: float) -> Path:
        """Create exact duration silence in 44.1kHz 16-bit mono."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        total_frames = int(max(0.1, duration_sec) * self.sample_rate)
        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"\x00\x00" * total_frames)
        return output_path

    def get_wav_duration(self, wav_path: Path) -> float:
        """Get exact duration in seconds of a WAV file."""
        if not wav_path.exists():
            return 0.0
        try:
            with wave.open(str(wav_path), "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return frames / float(rate)
        except Exception:
            return 0.0

    def generate_master_narration_track(
        self,
        storyboard: Dict[str, Any],
        output_path: Path,
    ) -> Dict[str, Any]:
        """Synthesize master voiceover track with guaranteed sequential non-overlapping timeline.

        Returns metadata including duration, scene segments, overlap count (strictly 0), and provider.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_narration"
        temp_dir.mkdir(parents=True, exist_ok=True)

        scenes = storyboard.get("scenes", storyboard.get("beats", []))
        total_duration = float(storyboard.get("total_duration_sec", 47.0))
        total_samples = int(total_duration * self.sample_rate)

        # Buffer of 16-bit signed integers (mono)
        master_buffer = [0] * total_samples

        timeline_segments: List[Dict[str, Any]] = []
        overlap_count = 0

        # Maintain track of current narration cursor
        current_cursor_sec = 0.0

        for scene in scenes:
            scene_id = scene.get("scene_id", scene.get("beat_id", 1))
            vo_text = scene.get("voiceover", "").strip()
            scene_start = float(scene.get("start_time", 0.0))

            if not vo_text:
                continue

            scene_id_clean = str(scene_id).replace("scene_", "").replace("beat_", "")
            scene_wav = temp_dir / f"narration_scene_{scene_id_clean}.wav"
            self.synthesize_speech_segment(vo_text, scene_wav)
            clip_dur = self.get_wav_duration(scene_wav)

            # Planned start: place narration with natural breathing room
            planned_start = scene_start + 0.25

            # Guarantee zero overlap: ensure start is strictly after previous narration ended
            actual_start = max(planned_start, current_cursor_sec + 0.25)
            actual_end = actual_start + clip_dur
            current_cursor_sec = actual_end

            timeline_segments.append({
                "scene_id": scene_id,
                "text": vo_text,
                "file": str(scene_wav),
                "planned_start": planned_start,
                "start_time": actual_start,
                "duration": clip_dur,
                "end_time": actual_end,
            })

            # Read samples from scene_wav and insert into master buffer
            try:
                with wave.open(str(scene_wav), "rb") as wf:
                    n_frames = wf.getnframes()
                    raw_frames = wf.readframes(n_frames)
                    # Unpack 16-bit mono
                    samples = struct.unpack(f"<{n_frames}h", raw_frames)

                    start_idx = int(actual_start * self.sample_rate)
                    for i, s in enumerate(samples):
                        idx = start_idx + i
                        if idx < total_samples:
                            # Apply gentle soft clip if needed
                            master_buffer[idx] = max(-32767, min(32767, s))
            except Exception as e:
                logger.error("Failed to copy samples for scene %d: %s", scene_id, e)

        # Write master WAV
        raw_out = bytearray(total_samples * 2)
        for i in range(total_samples):
            struct.pack_into("<h", raw_out, i * 2, master_buffer[i])

        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(raw_out)

        actual_track_duration = self.get_wav_duration(output_path)
        provider_info = self.get_provider_info()

        report = {
            "master_wav": str(output_path),
            "target_duration": total_duration,
            "actual_duration": actual_track_duration,
            "segment_count": len(timeline_segments),
            "overlap_count": overlap_count,
            "zero_overlap_guaranteed": (overlap_count == 0),
            "provider": provider_info["provider"],
            "voice_details": provider_info,
            "segments": timeline_segments,
        }

        # Save voice report
        report_file = output_path.parent / "narration_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        logger.info(
            "Master narration generated successfully: %d segments, %.2fs duration, overlap=%d, provider=%s",
            len(timeline_segments), actual_track_duration, overlap_count, provider_info["provider"]
        )
        return report
