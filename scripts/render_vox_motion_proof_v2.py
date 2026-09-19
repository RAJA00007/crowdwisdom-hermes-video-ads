"""scripts/render_vox_motion_proof_v2.py

Generates the 10.0-second pure Cinematic Vox Motion Graphics Proof (v2):
- Built entirely as an animated 2.5D visual composition using tools/vox_motion_engine.py
- Zero stock footage rectangle overlays. Zero PowerPoint card slides.
- Visibly demonstrates:
    1. Objects moving independently in 2.5D depth
    2. Camera movement through multi-plane layers
    3. Visual transformations:
       - TRADER cutout drops in with spring overshoot
       - DUPLICATE into 5 network nodes spreading across space
       - INFORMATION FLOOD: tumbling 3D newspaper fragments
       - VACUUM COLLAPSE: all 20 elements contract inward into dead-center card
       - UNDERLINE to baseline snap
       - DATA ANIMATION: accelerated counting 1 -> 1,482,930
    4. Kinetic typography as physical objects
    5. Company art direction materials (halftone cutouts, white keylines, offset red strokes, archival tan)
    6. Synchronized narration & motivated sound design
- Produces: outputs/videos/vox_motion_proof_v2.mp4
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Add project root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.ffmpeg_tool import FFmpegTool
from tools.vox_motion_engine import build_vox_motion_proof_sequence
from tools.voice_tool import VoiceTool
from tools.audio_tool import AudioTool

OUT_DIR = ROOT / "outputs" / "videos"
AUDIO_DIR = OUT_DIR / "temp_audio_p17"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

ff_tool = FFmpegTool()
ffmpeg = ff_tool.ffmpeg_path
voice_tool = VoiceTool(ffmpeg_path=ffmpeg)
audio_tool = AudioTool()


def generate_synchronized_audio(output_wav: Path, duration_sec: float = 10.0) -> Path:
    """Generate tightly synchronized narration, sound effects, and sub-bass hits."""
    print("--- 1. Synthesizing Synchronized Motion Audio ---")
    
    # Narration for the 10-second sequence:
    # 0.5s - 4.5s: "At 2:17 in the morning, a trader isn't fighting the market. They're drowning in it."
    # 5.0s - 7.0s: "Thousands of alerts. Endless noise."
    # 7.2s - 9.8s: "Until 1,482,930 inputs reveal the signal."
    v1_path = AUDIO_DIR / "v2_proof_v1.wav"
    v2_path = AUDIO_DIR / "v2_proof_v2.wav"
    v3_path = AUDIO_DIR / "v2_proof_v3.wav"

    voice_tool.synthesize_speech_segment(
        "At 2:17 in the morning, a trader isn't fighting the market. They're drowning in it.",
        v1_path
    )
    voice_tool.synthesize_speech_segment(
        "Thousands of alerts. Endless noise.",
        v2_path
    )
    voice_tool.synthesize_speech_segment(
        "Until 1,482,930 inputs reveal the signal.",
        v3_path
    )

    # Motivated SFX
    sfx_clock = AUDIO_DIR / "v2_clock.wav"
    sfx_snap = AUDIO_DIR / "v2_snap.wav"
    sfx_chime = AUDIO_DIR / "v2_chime.wav"

    audio_tool.generate_motivated_sfx("clock", sfx_clock, duration=2.0)
    audio_tool.generate_motivated_sfx("keyboard", sfx_snap, duration=2.0)
    audio_tool.generate_motivated_sfx("chime", sfx_chime, duration=2.0)

    filter_complex = (
        # Narration timing
        "[0:a]adelay=400|400,volume=1.3[n1];"
        "[1:a]adelay=4400|4400,volume=1.3[n2];"
        "[2:a]adelay=7200|7200,volume=1.3[n3];"
        "[n1][n2][n3]amix=inputs=3:dropout_transition=0:normalize=0[narr];"

        # SFX timing:
        # Clock tick at start
        "[3:a]adelay=100|100,volume=0.4[s1];"
        # Paper tumble / clicks at 4.0s
        "[4:a]adelay=4000|4000,volume=0.35[s2];"
        # Harmonic chime at collapse / counter reveal (7.0s)
        "[5:a]adelay=7000|7000,volume=0.55[s3];"
        "[s1][s2][s3]amix=inputs=3:dropout_transition=0:normalize=0[sfx];"

        # Sub-bass hit on collapse at 6.8s
        "aevalsrc=0.04*sin(2*PI*50*t):s=44100:d=10.0[sub];"
        "[sub]afade=t=in:st=6.8:d=0.05,afade=t=out:st=7.8:d=0.5[sub_hit];"

        # Mix all
        "[narr][sfx][sub_hit]amix=inputs=3:dropout_transition=0:normalize=0[mixed];"
        "[mixed]loudnorm=I=-16.8:TP=-1.0:LRA=7.0[out_audio]"
    )

    cmd = [
        ffmpeg, "-y",
        "-i", str(v1_path),
        "-i", str(v2_path),
        "-i", str(v3_path),
        "-i", str(sfx_clock),
        "-i", str(sfx_snap),
        "-i", str(sfx_chime),
        "-filter_complex", filter_complex,
        "-map", "[out_audio]",
        "-c:a", "pcm_s16le",
        "-ar", "44100",
        "-t", str(duration_sec),
        str(output_wav)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"  Mastered synchronized audio: {output_wav.name}")
    return output_wav


def render_motion_proof_v2():
    t0 = time.time()
    print("============================================================")
    print("PHASE 17/18: RENDERING VOX MOTION GRAPHICS PROOF V2 (10.0s)")
    print("============================================================\n")

    # 1. Build Composition
    print("--- 2. Compiling 2.5D Motion Graphics Sequence ---")
    comp = build_vox_motion_proof_sequence(duration_sec=10.0)
    print(f"  Loaded {len(comp.objects)} animated motion objects across 2.5D Z-space")

    # 2. Render Motion Video via Pipe
    temp_video = OUT_DIR / "temp_motion_raw_v2.mp4"
    print("--- 3. Rendering Frames to H.264 Video via Direct Engine Pipe ---")
    comp.render_video(temp_video, ffmpeg_path=ffmpeg)
    print(f"  Rendered visual motion stream: {temp_video.stat().st_size // 1024} KB")

    # 3. Generate Audio
    master_audio = AUDIO_DIR / "v2_proof_master_audio.wav"
    generate_synchronized_audio(master_audio, duration_sec=10.0)

    # 4. Mux Video + Audio
    final_output = OUT_DIR / "vox_motion_proof_v2.mp4"
    print("\n--- 4. Muxing Final Motion Graphics Proof ---")
    cmd_mux = [
        ffmpeg, "-y",
        "-i", str(temp_video),
        "-i", str(master_audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-shortest",
        str(final_output)
    ]
    subprocess.run(cmd_mux, check=True, capture_output=True)
    print(f"\n[SUCCESS] CREATED VOX MOTION GRAPHICS PROOF: {final_output}")
    print(f"File Size: {final_output.stat().st_size // 1024} KB")

    # 5. Technical Probe
    info = ff_tool.get_video_info(str(final_output))
    print(f"\n--- 5. Technical Probe Verification ---")
    print(f"  Duration: {info.get('duration'):.2f}s (Target: 8.0s - 12.0s)")
    print(f"  Resolution: {info.get('width')}x{info.get('height')} (Target: 1080x1920)")
    print(f"  Framerate: {info.get('fps')} fps")
    print(f"  Audio Present: {info.get('has_audio')}")
    print(f"  Total Production Time: {time.time() - t0:.1f}s")

    return final_output


if __name__ == "__main__":
    render_motion_proof_v2()
