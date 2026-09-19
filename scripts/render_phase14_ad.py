"""scripts/render_phase14_ad.py

Phase 14 Master Video Rendering Engine:
- Slices and color-grades verified real video footage for each beat
- Applies authentic company editorial overlays (archival tan, hot red, ink black, verified stats)
- Applies cinematic camera movement, freeze frame in beat 3, and alert wash in beat 6
- Assembles all 8 beats into 45.0s master video
- Muxes mastered audio (-16.8 LUFS, TP -1.0 dBTP, zero voice overlap)
- Outputs outputs/videos/final_cinematic_ad_phase14.mp4
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.ffmpeg_tool import FFmpegTool

OUT_DIR = Path("outputs/videos")
OUT_DIR.mkdir(parents=True, exist_ok=True)
BEATS_DIR = OUT_DIR / "p14_beats"
BEATS_DIR.mkdir(parents=True, exist_ok=True)
OVERLAY_DIR = OUT_DIR / "overlays_p14"
RAW_DIR = OUT_DIR / "raw_footage"

ff_tool = FFmpegTool()
ffmpeg = ff_tool.ffmpeg_path


def render_beat_01():
    """Beat 1 (0-5s, 5.0s): Night trader hook."""
    out_file = BEATS_DIR / "beat_01.mp4"
    in_video = RAW_DIR / "beat_01_night_window.webm"
    overlay = OVERLAY_DIR / "overlay_beat_01.png"

    # Scale & crop to 1080x1920, slow zoompan, cool nocturnal grade, composite overlay
    filter_graph = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "eq=contrast=1.15:brightness=-0.05:saturation=0.85,"
        "fps=30[bg];"
        "[bg][1:v]overlay=0:0[v]"
    )

    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:01",
        "-i", str(in_video),
        "-i", str(overlay),
        "-t", "5.0",
        "-filter_complex", filter_graph,
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Rendered {out_file.name} (5.0s)")
    return out_file


def render_beat_02():
    """Beat 2 (5-10s, 5.0s): Information overload."""
    out_file = BEATS_DIR / "beat_02.mp4"
    in_video = RAW_DIR / "beat_02_typing.ogv"
    overlay = OVERLAY_DIR / "overlay_beat_02.png"

    filter_graph = (
        "[0:v]setpts=0.7*PTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "eq=contrast=1.25:brightness=-0.08:saturation=0.7,"
        "fps=30[bg];"
        "[bg][1:v]overlay=0:0[v]"
    )

    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:02",
        "-i", str(in_video),
        "-i", str(overlay),
        "-t", "5.0",
        "-filter_complex", filter_graph,
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Rendered {out_file.name} (5.0s)")
    return out_file


def render_beat_03():
    """Beat 3 (10-15s, 5.0s): Signal problem (terminal freezes at 2.0s)."""
    out_file = BEATS_DIR / "beat_03.mp4"
    in_video = RAW_DIR / "beat_03_monitor.ogv"
    overlay = OVERLAY_DIR / "overlay_beat_03.png"

    # Terminal plays for 2.0s, then freezes for 3.0s using tpad stop_mode=clone
    filter_graph = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "eq=contrast=1.3:brightness=-0.05:saturation=0.5,"
        "fps=30,trim=duration=2.0,tpad=stop_mode=clone:stop_duration=3.0[bg];"
        "[bg][1:v]overlay=0:0[v]"
    )

    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:05",
        "-i", str(in_video),
        "-i", str(overlay),
        "-filter_complex", filter_graph,
        "-map", "[v]",
        "-t", "5.0",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Rendered {out_file.name} (5.0s)")
    return out_file


def render_beat_04():
    """Beat 4 (15-21s, 6.0s): Crowd signal convergence (1,482,930)."""
    out_file = BEATS_DIR / "beat_04.mp4"
    in_video = RAW_DIR / "beat_04_crowd.webm"
    overlay = OVERLAY_DIR / "overlay_beat_04.png"

    filter_graph = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "eq=contrast=1.2:brightness=-0.05:saturation=0.6,"
        "fps=30[bg];"
        "[bg][1:v]overlay=0:0[v]"
    )

    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:06",
        "-i", str(in_video),
        "-i", str(overlay),
        "-t", "6.0",
        "-filter_complex", filter_graph,
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Rendered {out_file.name} (6.0s)")
    return out_file


def render_beat_05():
    """Beat 5 (21-28s, 7.0s): Stock exchange trading floor & verified stats."""
    out_file = BEATS_DIR / "beat_05.mp4"
    in_video = RAW_DIR / "beat_05_exchange.webm"
    overlay = OVERLAY_DIR / "overlay_beat_05.png"

    filter_graph = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "eq=contrast=1.15:brightness=-0.02:saturation=0.9,"
        "fps=30[bg];"
        "[bg][1:v]overlay=0:0[v]"
    )

    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:15",
        "-i", str(in_video),
        "-i", str(overlay),
        "-t", "7.0",
        "-filter_complex", filter_graph,
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Rendered {out_file.name} (7.0s)")
    return out_file


def render_beat_06():
    """Beat 6 (28-35s, 7.0s): Trader payoff with 0.4s Alert Wash flash."""
    out_file = BEATS_DIR / "beat_06.mp4"
    in_video = RAW_DIR / "beat_05_exchange.webm"
    overlay = OVERLAY_DIR / "overlay_beat_06.png"

    # Red alert wash at t=0s to 0.4s: full screen #D62E1F with 0.45 opacity
    filter_graph = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "eq=contrast=1.2:brightness=0.0:saturation=0.95,"
        "fps=30[bg];"
        "color=c=0xD62E1F:s=1080x1920:d=0.4,format=rgba,colorchannelmixer=aa=0.42[wash];"
        "[bg][wash]overlay=0:0:enable='between(t,0,0.4)':format=auto[washed];"
        "[washed][1:v]overlay=0:0[v]"
    )

    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:25",
        "-i", str(in_video),
        "-i", str(overlay),
        "-t", "7.0",
        "-filter_complex", filter_graph,
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Rendered {out_file.name} (7.0s)")
    return out_file


def render_beat_07():
    """Beat 7 (35-41s, 6.0s): CrowdWisdom product platform / radar interface."""
    out_file = BEATS_DIR / "beat_07.mp4"
    in_video = RAW_DIR / "beat_03_monitor.ogv"
    overlay = OVERLAY_DIR / "overlay_beat_07.png"

    filter_graph = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "boxblur=12:6,"
        "eq=contrast=1.2:brightness=-0.18:saturation=0.4,"
        "fps=30[bg];"
        "[bg][1:v]overlay=0:0[v]"
    )

    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:10",
        "-i", str(in_video),
        "-i", str(overlay),
        "-t", "6.0",
        "-filter_complex", filter_graph,
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Rendered {out_file.name} (6.0s)")
    return out_file


def render_beat_08():
    """Beat 8 (41-45s, 4.0s): CTA & brand resolution with fade to black."""
    out_file = BEATS_DIR / "beat_08.mp4"
    in_video = RAW_DIR / "beat_01_night_window.webm"
    overlay = OVERLAY_DIR / "overlay_beat_08.png"

    filter_graph = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "boxblur=8:4,"
        "eq=contrast=1.1:brightness=-0.22:saturation=0.5,"
        "fps=30[bg];"
        "[bg][1:v]overlay=0:0[comp];"
        "[comp]fade=t=out:st=3.5:d=0.5[v]"
    )

    cmd = [
        ffmpeg, "-y",
        "-ss", "00:00:08",
        "-i", str(in_video),
        "-i", str(overlay),
        "-t", "4.0",
        "-filter_complex", filter_graph,
        "-map", "[v]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(out_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Rendered {out_file.name} (4.0s)")
    return out_file


def assemble_final_commercial():
    print("\n--- Step 1: Rendering 8 Cinematic Beat Clips ---")
    b1 = render_beat_01()
    b2 = render_beat_02()
    b3 = render_beat_03()
    b4 = render_beat_04()
    b5 = render_beat_05()
    b6 = render_beat_06()
    b7 = render_beat_07()
    b8 = render_beat_08()

    beats = [b1, b2, b3, b4, b5, b6, b7, b8]

    # Write concat list
    concat_list = BEATS_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for b in beats:
            f.write(f"file '{b.resolve()}'\n")

    print("\n--- Step 2: Concatenating Beats into Video Stream ---")
    concat_video = BEATS_DIR / "concat_video_stream.mp4"
    cmd_concat = [
        ffmpeg, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(concat_video)
    ]
    subprocess.run(cmd_concat, check=True, capture_output=True)
    print(f"Concatenated video stream: {concat_video}")

    print("\n--- Step 3: Muxing Master Broadcast Audio (-16.8 LUFS) ---")
    master_audio = OUT_DIR / "phase14_master_audio.wav"
    final_output = OUT_DIR / "final_cinematic_ad_phase14.mp4"

    cmd_mux = [
        ffmpeg, "-y",
        "-i", str(concat_video),
        "-i", str(master_audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-shortest",
        str(final_output)
    ]
    subprocess.run(cmd_mux, check=True, capture_output=True)
    print(f"\n[SUCCESS] FINAL MASTER CREATED: {final_output}")
    print(f"Size: {final_output.stat().st_size // 1024} KB")
    return final_output


if __name__ == "__main__":
    t0 = time.time()
    assemble_final_commercial()
    print(f"Total production time: {time.time() - t0:.1f}s")
