"""scripts/generate_phase14_audio.py

Generates professional cinematic audio for Phase 14:
- Narration using edge-tts (en-US-ChristopherNeural) aligned with 8 beats
- Motivated documentary sound design (rain/room tone, keyboard clicks, data chimes, bell strike, alert wash)
- Restrained cinematic ambient score with ducking
- Broadcast mastering: -17 LUFS integrated, < -1 dBTP true peak, 0 clipping
"""

import asyncio
import json
import math
import os
import struct
import subprocess
import sys
import wave
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.ffmpeg_tool import FFmpegTool
from tools.audio_tool import AudioTool

OUT_DIR = Path("outputs/videos")
OUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUT_DIR / "temp_audio_p14"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

ff_tool = FFmpegTool()
audio_tool = AudioTool(sample_rate=44100)

BEAT_NARRATIONS = [
    {
        "beat": "beat_01",
        "text": "At 2:17 in the morning, the market is still moving.",
        "start_cue": 0.5,
        "rate": "+10%"
    },
    {
        "beat": "beat_02",
        "text": "News is everywhere. Opinions are everywhere.",
        "start_cue": 5.4,
        "rate": "+15%"
    },
    {
        "beat": "beat_03",
        "text": "Signals are buried inside the noise.",
        "start_cue": 10.4,
        "rate": "+12%"
    },
    {
        "beat": "beat_04",
        "text": "CrowdWisdom unites 1,482,930 trader inputs.",
        "start_cue": 15.2,
        "rate": "+15%"
    },
    {
        "beat": "beat_05",
        "text": "68.4 percent accuracy. 14.6 hours of early warning.",
        "start_cue": 21.2,
        "rate": "+12%"
    },
    {
        "beat": "beat_06",
        "text": "Because the edge isn't more information. It's knowing which information matters.",
        "start_cue": 28.4,
        "rate": "+12%"
    },
    {
        "beat": "beat_07",
        "text": "CrowdWisdom Trading.",
        "start_cue": 35.6,
        "rate": "+8%"
    },
    {
        "beat": "beat_08",
        "text": "See the signal inside the noise.",
        "start_cue": 41.4,
        "rate": "+8%"
    }
]


async def synthesize_speech(text: str, output_mp3: Path, rate: str = "+8%"):
    import edge_tts
    comm = edge_tts.Communicate(
        text=text,
        voice="en-US-ChristopherNeural",
        rate=rate,
        pitch="-1Hz"
    )
    await comm.save(str(output_mp3))


def convert_to_wav(mp3_path: Path, wav_path: Path):
    cmd = [
        ff_tool.ffmpeg_path, "-y",
        "-i", str(mp3_path),
        "-ar", "44100",
        "-ac", "2",
        str(wav_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def get_wav_duration(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())


def build_narration_track(total_duration: float = 45.0) -> Path:
    sample_rate = 44100
    total_samples = int(total_duration * sample_rate)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    print("Synthesizing narration segments via Edge TTS...")
    segments = []
    for item in BEAT_NARRATIONS:
        mp3 = TEMP_DIR / f"{item['beat']}.mp3"
        wav = TEMP_DIR / f"{item['beat']}.wav"
        asyncio.run(synthesize_speech(item["text"], mp3, rate=item.get("rate", "+8%")))
        convert_to_wav(mp3, wav)
        dur = get_wav_duration(wav)
        print(f"  {item['beat']}: {dur:.2f}s -> cue {item['start_cue']}s: \"{item['text'][:35]}...\"")

        # Read samples
        with wave.open(str(wav), "rb") as wf:
            nframes = wf.getnframes()
            data = wf.readframes(nframes)
            raw = struct.unpack(f"<{nframes * 2}h", data)

        start_idx = int(item["start_cue"] * sample_rate)
        for i in range(nframes):
            idx = start_idx + i
            if idx < total_samples:
                # Add voice sample with gentle leveling
                left[idx] += (raw[i * 2] / 32768.0) * 0.92
                right[idx] += (raw[i * 2 + 1] / 32768.0) * 0.92

        segments.append({
            "beat": item["beat"],
            "start": item["start_cue"],
            "end": item["start_cue"] + dur,
            "duration": dur
        })

    # Check for overlaps
    overlaps = 0
    for k in range(len(segments) - 1):
        if segments[k]["end"] > segments[k + 1]["start"]:
            overlaps += 1
            print(f"WARNING: Voice overlap between {segments[k]['beat']} and {segments[k+1]['beat']}")
    print(f"Voice overlap count: {overlaps} (Strictly 0 expected)")

    narration_wav = TEMP_DIR / "track1_narration.wav"
    audio_tool._write_stereo_wav(narration_wav, left, right)
    return narration_wav


def build_music_score(total_duration: float = 45.0) -> Path:
    """Compose a subtle cinematic ambient score with gentle chord progression."""
    sample_rate = 44100
    total_samples = int(total_duration * sample_rate)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Subtle chord progression: Dm -> Bb -> F -> C -> Dm
    chords = [
        (0.0, 10.0, [146.83, 220.0, 261.63, 349.23]),   # Dm/F
        (10.0, 21.0, [116.54, 174.61, 233.08, 349.23]), # Bb
        (21.0, 35.0, [130.81, 196.0, 261.63, 392.0]),   # C / Suspended
        (35.0, 45.0, [146.83, 220.0, 293.66, 440.0])    # Dm resolve
    ]

    for start_t, end_t, freqs in chords:
        start_idx = int(start_t * sample_rate)
        end_idx = min(total_samples, int(end_t * sample_rate))
        chord_len = end_idx - start_idx
        for i in range(chord_len):
            t = (start_idx + i) / float(sample_rate)
            # Fade in and out
            fade_in = min(1.0, (i / float(sample_rate)) / 1.5)
            fade_out = min(1.0, ((chord_len - i) / float(sample_rate)) / 1.5)
            env = fade_in * fade_out * 0.12  # Restrained warm level (-18dB to -24dB)

            val_l = 0.0
            val_r = 0.0
            for fi, f in enumerate(freqs):
                # Gentle warm sine harmonics with subtle stereo panning
                detune = 0.3 * math.sin(2 * math.pi * 0.2 * t + fi)
                s1 = math.sin(2 * math.pi * (f + detune) * t)
                s2 = 0.3 * math.sin(4 * math.pi * f * t)
                pan = 0.3 * math.sin(fi * 1.5)
                val_l += (s1 + s2) * (0.5 - pan)
                val_r += (s1 + s2) * (0.5 + pan)

            idx = start_idx + i
            left[idx] += val_l * env * 0.35
            right[idx] += val_r * env * 0.35

    music_wav = TEMP_DIR / "track2_music.wav"
    audio_tool._write_stereo_wav(music_wav, left, right)
    return music_wav


def build_sfx_track(total_duration: float = 45.0) -> Path:
    """Assemble motivated sound effects at key narrative beats."""
    sample_rate = 44100
    total_samples = int(total_duration * sample_rate)
    left = [0.0] * total_samples
    right = [0.0] * total_samples

    # Beat 1: Distant clock tick (0.5s) & rain ambience
    for i in range(total_samples):
        t = i / float(sample_rate)
        # Low room tone
        left[i] += (math.sin(2 * math.pi * 55 * t) * 0.02)
        right[i] += (math.sin(2 * math.pi * 55.5 * t) * 0.02)

    def add_hit(cue_sec: float, freq: float, decay: float, vol: float):
        start = int(cue_sec * sample_rate)
        length = int(min(3.0, total_duration - cue_sec) * sample_rate)
        for j in range(length):
            t = j / float(sample_rate)
            env = math.exp(-decay * t)
            sig = math.sin(2 * math.pi * freq * (1.0 - 0.2 * t) * t) * env * vol
            idx = start + j
            if idx < total_samples:
                left[idx] += sig
                right[idx] += sig

    # Beat 1: Low tension hit at 0.2s
    add_hit(0.2, 75.0, 2.5, 0.35)

    # Beat 2: Rapid keystroke clicks (5.2s - 9.0s)
    for click_t in [5.2, 5.5, 5.7, 6.1, 6.4, 6.9, 7.3, 7.8, 8.2, 8.6]:
        add_hit(click_t, 2400.0, 45.0, 0.08)

    # Beat 3: Noise freeze & deep sub drop at 10.1s
    add_hit(10.1, 48.0, 1.8, 0.45)

    # Beat 4: Collective intelligence data chime at 15.2s
    add_hit(15.2, 1174.66, 3.0, 0.18) # D6 bell tone
    add_hit(15.4, 1479.98, 3.0, 0.15) # F#6 bell tone

    # Beat 5: Stock exchange bell strike at 21.0s
    add_hit(21.0, 880.0, 1.2, 0.40)   # A5 brass resonance
    add_hit(21.0, 440.0, 0.9, 0.35)   # A4 core bell

    # Beat 6: Alert wash riser and entry hit at 28.0s
    add_hit(28.0, 110.0, 1.5, 0.38)

    # Beat 8: Clean final resolve chord hit at 41.0s
    add_hit(41.0, 220.0, 1.0, 0.25)
    add_hit(41.0, 329.63, 1.0, 0.20)
    add_hit(41.0, 440.0, 1.0, 0.18)

    sfx_wav = TEMP_DIR / "track3_sfx.wav"
    audio_tool._write_stereo_wav(sfx_wav, left, right)
    return sfx_wav


def master_phase14_audio(total_duration: float = 45.0) -> Path:
    narration = build_narration_track(total_duration)
    music = build_music_score(total_duration)
    sfx = build_sfx_track(total_duration)

    master_wav = OUT_DIR / "phase14_master_audio.wav"

    # FFmpeg multi-track mix with sidechain compression / ducking and loudnorm filter
    cmd = [
        ff_tool.ffmpeg_path, "-y",
        "-i", str(narration),
        "-i", str(music),
        "-i", str(sfx),
        "-filter_complex",
        (
            "[0:a]volume=1.0[voice];"
            "[1:a]volume=0.22[bg_music];"
            "[2:a]volume=0.45[effects];"
            "[bg_music][voice]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=300[ducked_music];"
            "[voice][ducked_music][effects]amix=inputs=3:duration=first:dropout_transition=2[mixed];"
            "[mixed]loudnorm=I=-17:LRA=7:TP=-1.0:print_format=json[mastered]"
        ),
        "-map", "[mastered]",
        "-ar", "44100",
        "-ac", "2",
        str(master_wav)
    ]

    print("Mixing and mastering 3-track audio with FFmpeg loudnorm (-17 LUFS, TP -1.0 dBTP)...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Mastering error:", res.stderr)
        raise RuntimeError(f"FFmpeg audio mastering failed: {res.stderr}")

    print(f"Master audio generated: {master_wav}")
    return master_wav


if __name__ == "__main__":
    master_phase14_audio(45.0)
