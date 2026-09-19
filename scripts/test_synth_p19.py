import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.voice_tool import VoiceTool
from tools.ffmpeg_tool import FFmpegTool

ff = FFmpegTool().ffmpeg_path
vt = VoiceTool(ffmpeg_path=ff)

script_path = ROOT / "outputs" / "videos" / "phase16_original_script.json"
with open(script_path, "r", encoding="utf-8") as f:
    script = json.load(f)

audio_dir = ROOT / "outputs" / "videos" / "temp_audio_phase19"
audio_dir.mkdir(parents=True, exist_ok=True)

total_vo_dur = 0.0
print("=== Synthesizing 8 Scenes for Phase 19 ===")
for sc in script["scenes"]:
    sc_id = sc["scene_id"]
    text = sc["narration"]
    out_wav = audio_dir / f"{sc_id}.wav"
    vt.synthesize_speech_segment(text, out_wav)
    dur = vt.get_wav_duration(out_wav)
    total_vo_dur += dur
    print(f"{sc_id} (slot {sc['start']}s - {sc['end']}s, alloc {sc['duration']}s): VO duration = {dur:.2f}s | \"{text[:45]}...\"")

print(f"\nTotal Raw Speech Duration: {total_vo_dur:.2f}s across 45.0s composition")
