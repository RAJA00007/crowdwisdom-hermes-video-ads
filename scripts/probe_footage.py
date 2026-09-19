import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.ffmpeg_tool import FFmpegTool

ff = FFmpegTool()
raw_dir = Path("outputs/videos/raw_footage")
for f in raw_dir.glob("*.*"):
    info = ff.get_video_info(str(f))
    print(f"{f.name}: {info.get('width')}x{info.get('height')}, {info.get('duration')}s, fps={info.get('fps')}")
