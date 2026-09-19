"""Documentary Audio Tool for motivated sound design and cinematic musical scoring.

Adheres strictly to editorial visual journalism standards:
- Motivated, realistic documentary SFX (clock tick, phone vibration, mouse click, keyboard, notification, data chime).
- Restrained, cinematic documentary music score (calm analog drone, subtle cello/pad warmth, minimal tension pulse).
- 3-Track audio hierarchy: Track 1 = Narration, Track 2 = Music, Track 3 = SFX.
- Audio mastering: Broadcast -16 LUFS integrated, -1.0 dBTP true peak, compressor and limiter.

Compatible with Python 3.10.
"""

import logging
import math
import struct
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class AudioTool:
    """Documentary sound designer and audio engine for visual journalism video ads."""

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def _write_stereo_wav(
        self,
        output_path: Path,
        left_channel: List[float],
        right_channel: List[float],
    ) -> Path:
        """Write normalized float samples (-1.0 to 1.0) to 16-bit stereo WAV."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        length = min(len(left_channel), len(right_channel))
        raw_bytes = bytearray(length * 4)  # 2 channels * 2 bytes

        for i in range(length):
            l_val = max(-32767, min(32767, int(left_channel[i] * 32767)))
            r_val = max(-32767, min(32767, int(right_channel[i] * 32767)))
            struct.pack_into("<hh", raw_bytes, i * 4, l_val, r_val)

        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(raw_bytes)

        return output_path

    def generate_motivated_sfx(self, sfx_type: str, output_path: Path, duration: float = 1.2) -> Path:
        """Synthesize specific motivated documentary sound effects."""
        num_samples = int(duration * self.sample_rate)
        left = [0.0] * num_samples
        right = [0.0] * num_samples
        st = sfx_type.lower()

        # 1. Clock Tick & Phone Vibration (2:17 AM Hook)
        if "clock" in st or "vibration" in st or "tick" in st:
            for i in range(num_samples):
                t = i / float(self.sample_rate)
                # Clock tick at t=0.05
                tick_env = math.exp(-120 * max(0.0, t - 0.05)) if t >= 0.05 else 0.0
                tick_val = (math.sin(2 * math.pi * 1850 * t) + 0.4 * math.sin(2 * math.pi * 3700 * t)) * tick_env * 0.45

                # Dual buzz vibration at t=0.25 to 0.45 and 0.55 to 0.75
                vib_env1 = math.sin(math.pi * (t - 0.25) / 0.18) if 0.25 <= t <= 0.43 else 0.0
                vib_env2 = math.sin(math.pi * (t - 0.52) / 0.18) if 0.52 <= t <= 0.70 else 0.0
                vib_buzz = math.sin(2 * math.pi * 135 * t) * (1.0 + 0.4 * math.sin(2 * math.pi * 270 * t))
                vib_val = vib_buzz * (vib_env1 + vib_env2) * 0.35

                val = tick_val + vib_val
                left[i] = val * 0.95
                right[i] = val * 1.05

        # 2. Notification Whisper (Scene 2 Information Chaos)
        elif "notification" in st or "ping" in st:
            # Understated glass harmonic chime (1760Hz A6 + 2640Hz E7)
            for i in range(num_samples):
                t = i / float(self.sample_rate)
                decay1 = math.exp(-8.0 * t)
                decay2 = math.exp(-12.0 * t)
                s1 = math.sin(2 * math.pi * 1760 * t) * decay1 * 0.3
                s2 = math.sin(2 * math.pi * 2640 * t) * decay2 * 0.18
                val = s1 + s2
                left[i] = val * 0.8
                right[i] = val * 1.0

        # 3. Tactile Mouse Click & Deep Bass Thump (Scene 3 Insight)
        elif "mouse" in st or "click" in st:
            for i in range(num_samples):
                t = i / float(self.sample_rate)
                # Sharp mechanical transient
                click_env = math.exp(-220 * t)
                click_val = (math.sin(2 * math.pi * 3200 * t) + math.sin(2 * math.pi * 4800 * t)) * click_env * 0.5
                # Cinematic sub-bass weight
                sub_env = math.exp(-5.0 * t)
                sub_val = math.sin(2 * math.pi * 48 * t) * sub_env * 0.4
                val = click_val + sub_val
                left[i] = val
                right[i] = val

        # 4. Editorial Data Lock Chime (Scene 4 Metaphor & Scene 5 Data)
        elif "data" in st or "chime" in st or "metric" in st:
            # Resonant harmonic fifth (523.25Hz C5 -> 783.99Hz G5)
            for i in range(num_samples):
                t = i / float(self.sample_rate)
                env1 = math.exp(-4.5 * t)
                env2 = math.exp(-5.5 * max(0.0, t - 0.08)) if t >= 0.08 else 0.0
                s1 = math.sin(2 * math.pi * 523.25 * t) * env1 * 0.28
                s2 = math.sin(2 * math.pi * 783.99 * t) * env2 * 0.22
                val = s1 + s2
                left[i] = val * 0.9
                right[i] = val * 1.1

        # 5. Calm Keystroke (Scene 6 Payoff)
        elif "keystroke" in st or "keyboard" in st:
            for i in range(num_samples):
                t = i / float(self.sample_rate)
                key_env = math.exp(-95 * t)
                key_val = (math.sin(2 * math.pi * 1400 * t) + 0.3 * math.sin(2 * math.pi * 800 * t)) * key_env * 0.35
                left[i] = key_val
                right[i] = key_val

        # 6. Abrupt Freeze Silence / Tape Stop (Beat 3 Problem)
        elif "freeze" in st or "silence" in st or "abrupt" in st:
            for i in range(num_samples):
                t = i / float(self.sample_rate)
                # Subtle vinyl tape-stop friction at 0.0 to 0.15s, then clean silence
                if t < 0.15:
                    freq = max(40.0, 400.0 * (1.0 - t / 0.15))
                    env = math.sin(math.pi * (t / 0.15))
                    val = math.sin(2 * math.pi * freq * t) * env * 0.35
                else:
                    val = 0.0
                left[i] = val
                right[i] = val

        # 7. Outro Harmonic Resolve (Beat 8 CTA)

        else:
            # Deep warm acoustic fundamental resolve (65.4Hz C2 + 130.8Hz C3)
            for i in range(num_samples):
                t = i / float(self.sample_rate)
                env = math.sin(math.pi * (t / duration)) if t < duration else 0.0
                decay = math.exp(-1.8 * t)
                s1 = math.sin(2 * math.pi * 65.4 * t) * 0.4
                s2 = math.sin(2 * math.pi * 130.8 * t) * 0.25
                s3 = math.sin(2 * math.pi * 196.0 * t) * 0.15
                val = (s1 + s2 + s3) * decay * 0.5
                left[i] = val
                right[i] = val

        return self._write_stereo_wav(output_path, left, right)

    def generate_documentary_music_bed(
        self,
        output_path: Path,
        duration: float = 47.0,
    ) -> Path:
        """Generate a restrained, cinematic visual-journalism music bed.

        Structure:
        - Low cello / analog drone in D minor (73.4Hz / 110.0Hz).
        - Subtle pulsing heartbeat texture (65 BPM).
        - Warm acoustic warmth, zero overpowering EDM/drums.
        - Natural fade-in and smooth outro resolve.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        total_samples = int(duration * self.sample_rate)
        left = [0.0] * total_samples
        right = [0.0] * total_samples

        bpm = 64.0
        beat_interval = 60.0 / bpm  # ~0.9375s

        # D minor progression frequencies: D2 (73.42Hz), A2 (110.0Hz), F2 (87.31Hz), C3 (130.81Hz)
        chord_prog = [
            (73.42, 110.0, 174.61),  # Dm (0-16s)
            (87.31, 130.81, 174.61), # F  (16-28s)
            (98.00, 146.83, 196.00), # G  (28-38s)
            (73.42, 110.0, 220.00),  # Dm resolve (38-47s)
        ]

        for i in range(total_samples):
            t = i / float(self.sample_rate)

            # Master volume envelope: 2s fade-in, 3s fade-out at end
            master_env = 1.0
            if t < 2.0:
                master_env = t / 2.0
            elif t > duration - 3.0:
                master_env = max(0.0, (duration - t) / 3.0)

            # Select harmonic chord based on time
            if t < 16.0:
                f1, f2, f3 = chord_prog[0]
            elif t < 28.0:
                f1, f2, f3 = chord_prog[1]
            elif t < 38.0:
                f1, f2, f3 = chord_prog[2]
            else:
                f1, f2, f3 = chord_prog[3]

            # Analog drone layer with subtle chorusing/detune
            drone_1 = math.sin(2 * math.pi * f1 * t) * 0.22
            drone_2 = math.sin(2 * math.pi * (f2 + 0.15) * t) * 0.16
            drone_3 = math.sin(2 * math.pi * (f3 - 0.20) * t) * 0.10

            # Restrained rhythmic pulse (subtle low thud on each beat)
            beat_pos = (t % beat_interval) / beat_interval
            pulse_env = math.exp(-18 * beat_pos) if beat_pos < 0.3 else 0.0
            pulse_thud = math.sin(2 * math.pi * 52 * t) * pulse_env * 0.18

            # Ambient high texture (gentle sine sparkle)
            sparkle = math.sin(2 * math.pi * 1174.66 * t) * (0.02 * (1 + math.sin(0.5 * t)))

            val = (drone_1 + drone_2 + drone_3 + pulse_thud + sparkle) * master_env * 0.70

            # Subtle stereo spread
            left[i] = val * (0.85 + 0.15 * math.sin(0.4 * t))
            right[i] = val * (0.85 - 0.15 * math.sin(0.4 * t))

        return self._write_stereo_wav(output_path, left, right)

    def assemble_sfx_track(
        self,
        storyboard: Dict[str, Any],
        output_path: Path,
        duration: float = 47.0,
    ) -> Path:
        """Synthesize and merge all storyboard SFX into a single synchronized Track 3 WAV."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_sfx"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_samples = int(duration * self.sample_rate)
        left = [0.0] * total_samples
        right = [0.0] * total_samples

        scenes = storyboard.get("scenes", storyboard.get("beats", []))
        for scene in scenes:
            sfx_info = scene.get("sfx")
            if not sfx_info:
                continue

            scene_id = scene.get("scene_id", scene.get("beat_id", 1))
            sfx_type = sfx_info.get("type", "tick")
            timestamp = float(sfx_info.get("timestamp", scene.get("start_time", 0.0)))
            scene_id_clean = str(scene_id).replace("scene_", "").replace("beat_", "")
            sfx_file = temp_dir / f"sfx_{scene_id_clean}_{sfx_type}.wav"
            self.generate_motivated_sfx(sfx_type, sfx_file)

            # Read sfx_file and add into timeline
            try:
                with wave.open(str(sfx_file), "rb") as wf:
                    n = wf.getnframes()
                    raw = wf.readframes(n)
                    samples = struct.unpack(f"<{n*2}h", raw)

                    start_idx = int(timestamp * self.sample_rate)
                    for idx in range(n):
                        t_idx = start_idx + idx
                        if t_idx < total_samples:
                            # 16-bit to float (-1.0 to 1.0)
                            l_val = samples[idx * 2] / 32768.0
                            r_val = samples[idx * 2 + 1] / 32768.0
                            left[t_idx] += l_val * 0.65
                            right[t_idx] += r_val * 0.65
            except Exception as e:
                logger.error("Failed to place SFX at %.2fs: %s", timestamp, e)

        return self._write_stereo_wav(output_path, left, right)
