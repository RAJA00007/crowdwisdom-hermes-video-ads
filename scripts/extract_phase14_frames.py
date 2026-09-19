"""scripts/extract_phase14_frames.py

Extracts key representative frames from final_cinematic_ad_phase14.mp4 for visual audit.
"""

import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.ffmpeg_tool import FFmpegTool

ff = FFmpegTool()
video_path = Path("outputs/videos/final_cinematic_ad_phase14.mp4")
frames_dir = Path("outputs/videos/phase14_frames")
frames_dir.mkdir(parents=True, exist_ok=True)

sample_times = [
    ("beat_01_hook", "00:00:02.5"),
    ("beat_02_overload", "00:00:07.5"),
    ("beat_03_signal_prob", "00:00:12.5"),
    ("beat_04_crowd_stat", "00:00:18.0"),
    ("beat_05_data_proof", "00:00:24.5"),
    ("beat_06_payoff", "00:00:31.5"),
    ("beat_07_product_radar", "00:00:38.0"),
    ("beat_08_cta", "00:00:43.0")
]

for label, ts in sample_times:
    out_img = frames_dir / f"{label}.png"
    cmd = [
        ff.ffmpeg_path, "-y",
        "-ss", ts,
        "-i", str(video_path),
        "-frames:v", "1",
        str(out_img)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Extracted {out_img.name} at {ts}")
