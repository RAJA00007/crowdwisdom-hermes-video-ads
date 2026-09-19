"""scripts/generate_phase14_storyboard.py

Generates outputs/videos/phase14_storyboard.json for Phase 14:
- 8 beats (~45s total)
- Strictly verified metrics:
  - 1,482,930 trader inputs
  - 68.4% directional accuracy
  - 14.6 hours early warning lead
- No invented numbers (strictly zero unverified statistics)
- Full storyboard schema with footage, graphics, camera, voiceover, sound design, approved text.
"""

import json
from pathlib import Path

OUT_DIR = Path("outputs/videos")
OUT_DIR.mkdir(parents=True, exist_ok=True)

STORYBOARD = {
    "project": "CrowdWisdomTrading Video Ads - Phase 14",
    "total_duration_sec": 45.0,
    "resolution": {"width": 1080, "height": 1920, "aspect_ratio": "9:16"},
    "target_platform": "Meta / Instagram Reels / TikTok / YouTube Shorts",
    "production_mode": "cinematic_licensed_footage",
    "ai_video_generation": False,
    "art_direction": {
        "reference": "assets/style_reference/company_art_direction.png",
        "editorial_palette": {
            "archival_tan": "#EAE4D9",
            "ink_black": "#111215",
            "hot_red": "#E02E2E",
            "mustard": "#E5A93C",
            "halftone_gray": "#555860",
            "pure_white": "#FFFFFF"
        },
        "visual_language": "financial documentary + cinematic newsroom + editorial magazine + modern trading intelligence"
    },
    "verified_claims": [
        {"metric": "trader_inputs", "value": "1,482,930", "unit": "inputs"},
        {"metric": "directional_accuracy", "value": "68.4%", "unit": "percentage"},
        {"metric": "early_warning_lead", "value": "14.6 HOURS", "unit": "hours"}
    ],
    "beats": [
        {
            "scene_id": "beat_01",
            "beat_number": 1,
            "title": "The Problem / Hero Hook",
            "duration": 5.0,
            "start_time": 0.0,
            "end_time": 5.0,
            "visual_goal": "Cinematic nighttime trader scene. A trader alone at a desk late at night. Monitor glow. City/night atmosphere. Slow push-in. Subtle tension.",
            "footage_requirements": [
                "raw_footage/beat_01_night_window.webm",
                "Raindrops against dark city window with distant neon bokeh",
                "Dark moody desk atmosphere"
            ],
            "graphic_requirements": [
                "Editorial header: 2:17 AM in Archival Tan badge",
                "Main typography: THE MARKET NEVER SLEEPS in Ink Black on Tan card",
                "Rough white keylines framing the shot"
            ],
            "camera": "Slow cinematic push-in (zoom 1.0 -> 1.06)",
            "narration": "At 2:17 in the morning, the market is still moving.",
            "sound_design": [
                "Rain on window ambience",
                "Subtle distant clock tick",
                "Low tension hit"
            ],
            "approved_text": ["2:17 AM", "THE MARKET NEVER SLEEPS."],
            "approved_numbers": []
        },
        {
            "scene_id": "beat_02",
            "beat_number": 2,
            "title": "Information Overload",
            "duration": 5.0,
            "start_time": 5.0,
            "end_time": 10.0,
            "visual_goal": "Fast cinematic montage: financial headlines, charts, market movement, phones, news feeds, multiple information sources. Fast lateral movement and parallax.",
            "footage_requirements": [
                "raw_footage/beat_02_typing.ogv",
                "Rapid trading keyboard inputs",
                "High density information stream"
            ],
            "graphic_requirements": [
                "Headline: TOO MUCH INFORMATION",
                "Fast financial headline tape scrolling",
                "Hot Red warning ticker overlay"
            ],
            "camera": "Fast lateral drift with subtle camera shake",
            "narration": "News is everywhere. Opinions are everywhere.",
            "sound_design": [
                "Rapid keyboard typing clicks",
                "Overlapping digital notification beeps",
                "Rising high-frequency tension"
            ],
            "approved_text": ["TOO MUCH INFORMATION."],
            "approved_numbers": []
        },
        {
            "scene_id": "beat_03",
            "beat_number": 3,
            "title": "Signal Problem",
            "duration": 5.0,
            "start_time": 10.0,
            "end_time": 15.0,
            "visual_goal": "Visual slows down. Noise freezes and collapses. Cinematic realization moment. Company red underline and archival keyline framing.",
            "footage_requirements": [
                "raw_footage/beat_03_monitor.ogv",
                "Terminal data flow freezing in mid-stream",
                "Monochrome data lines"
            ],
            "graphic_requirements": [
                "Headline: NOT ENOUGH SIGNAL",
                "Company signature Hot Red hand-drawn style underline",
                "Archival keyline bounding box"
            ],
            "camera": "Instant noise collapse to dead-center stillness",
            "narration": "Signals are buried inside the noise.",
            "sound_design": [
                "Sudden noise cutoff / vacuum collapse",
                "Sub bass drop (50 Hz)",
                "Paper friction snap"
            ],
            "approved_text": ["NOT ENOUGH SIGNAL."],
            "approved_numbers": []
        },
        {
            "scene_id": "beat_04",
            "beat_number": 4,
            "title": "Crowd Signal Convergence",
            "duration": 6.0,
            "start_time": 15.0,
            "end_time": 21.0,
            "visual_goal": "Introduce the CrowdWisdom concept. Multiple traders and information streams converging into one unified visual signal.",
            "footage_requirements": [
                "raw_footage/beat_04_crowd.webm",
                "Self-organized pedestrian crowd flow",
                "Halftone particulate layer overlay"
            ],
            "graphic_requirements": [
                "Giant verified stat card: 1,482,930",
                "Subhead: TRADER INPUTS",
                "Editorial badge: CROWD WISDOM COLLECTIVE INTELLIGENCE"
            ],
            "camera": "Gentle upward tilt with parallax grid",
            "narration": "CrowdWisdom unites 1,482,930 trader inputs.",
            "sound_design": [
                "Filtered crowd murmur resolving into clear harmonic tone",
                "Data chime (1200 Hz)",
                "Warm analog synth pad entry"
            ],
            "approved_text": ["1,482,930", "TRADER INPUTS", "COLLECTIVE INTELLIGENCE"],
            "approved_numbers": ["1,482,930"]
        },
        {
            "scene_id": "beat_05",
            "beat_number": 5,
            "title": "Data Proof & Directional Accuracy",
            "duration": 7.0,
            "start_time": 21.0,
            "end_time": 28.0,
            "visual_goal": "Build a strong visual proof sequence. Dual verified metrics on archival cards over high-res stock exchange trading floor footage.",
            "footage_requirements": [
                "raw_footage/beat_05_exchange.webm",
                "Stock exchange bell ceremony and active trading floor",
                "Price board displays"
            ],
            "graphic_requirements": [
                "Card 1: 68.4% Directional Accuracy",
                "Card 2: 14.6 HOURS Early Warning Lead",
                "Editorial keyline grid with Hot Red highlight bars"
            ],
            "camera": "Slow cinematic pan with steady card focus",
            "narration": "68.4 percent accuracy. 14.6 hours of early warning.",
            "sound_design": [
                "Acoustic exchange bell strike with natural decay",
                "Crisp mechanical shutter click",
                "Precision sub-bass pulse"
            ],
            "approved_text": ["68.4%", "DIRECTIONAL ACCURACY", "14.6 HOURS", "EARLY WARNING LEAD"],
            "approved_numbers": ["68.4%", "14.6 HOURS"]
        },
        {
            "scene_id": "beat_06",
            "beat_number": 6,
            "title": "Trader Payoff / Noise to Action",
            "duration": 7.0,
            "start_time": 28.0,
            "end_time": 35.0,
            "visual_goal": "Show trader reacting BEFORE market movement becomes obvious. Noise -> signal -> action. One major ALERT WASH only here.",
            "footage_requirements": [
                "raw_footage/beat_05_exchange.webm",
                "Market floor momentum shift",
                "High contrast editorial treatment"
            ],
            "graphic_requirements": [
                "Brief Hot Red alert wash flash (0.4s)",
                "Headline: NOISE -> SIGNAL -> ACTION",
                "Archival label: EXECUTION ADVANTAGE"
            ],
            "camera": "Dynamic push into stabilized signal resolution",
            "narration": "Because the edge isn't more information. It's knowing which information matters.",
            "sound_design": [
                "Resonant cinematic alert wash swell",
                "Clean keyboard Enter stroke",
                "Warm low-frequency resolve"
            ],
            "approved_text": ["NOISE -> SIGNAL -> ACTION", "EXECUTION ADVANTAGE"],
            "approved_numbers": []
        },
        {
            "scene_id": "beat_07",
            "beat_number": 7,
            "title": "CrowdWisdom Product Platform",
            "duration": 6.0,
            "start_time": 35.0,
            "end_time": 41.0,
            "visual_goal": "Show CrowdWisdom Trading platform and signal radar in restrained cinematic archival framing. Product feels like the definitive solution.",
            "footage_requirements": [
                "raw_footage/beat_03_monitor.ogv",
                "Real-time signal tracking and platform display",
                "Technical interface layer"
            ],
            "graphic_requirements": [
                "CrowdWisdom Radar Frame with cardinal compass bearings",
                "Product title: CROWDWISDOM INTELLIGENCE PLATFORM",
                "Sub-badge: REAL-TIME ALPHA SIGNALS",
                "Editorial paper frame margins"
            ],
            "camera": "Slow rotational drift and subtle scale (1.0 -> 1.04)",
            "narration": "CrowdWisdom Trading.",
            "sound_design": [
                "Subtle high-tech radar ping",
                "Low warm analog pad sustained",
                "Interface activate tone"
            ],
            "approved_text": ["CROWDWISDOM INTELLIGENCE PLATFORM", "REAL-TIME ALPHA SIGNALS"],
            "approved_numbers": []
        },
        {
            "scene_id": "beat_08",
            "beat_number": 8,
            "title": "CTA / Brand Resolution",
            "duration": 4.0,
            "start_time": 41.0,
            "end_time": 45.0,
            "visual_goal": "Clean final brand resolution frame. Bold typography, CrowdWisdom Trading identity, positioning slogan, website URL. Held long enough to read.",
            "footage_requirements": [
                "raw_footage/beat_01_night_window.webm",
                "Subtle dark ambient background with warm vignette"
            ],
            "graphic_requirements": [
                "Logo badge: CROWDWISDOM TRADING",
                "Tagline: SEE THE SIGNAL INSIDE THE NOISE.",
                "Hot Red keyline bar",
                "Domain pill: crowdwisdomtrading.com in Ink Black on Tan"
            ],
            "camera": "Static locked frame with soft fade-to-black at 44.5s",
            "narration": "See the signal inside the noise.",
            "sound_design": [
                "Final orchestral/synth chord resolve",
                "Warm natural reverb decay",
                "Clean silence on fade out"
            ],
            "approved_text": [
                "CROWDWISDOM TRADING",
                "SEE THE SIGNAL INSIDE THE NOISE.",
                "crowdwisdomtrading.com"
            ],
            "approved_numbers": []
        }
    ]
}

def main():
    sb_path = OUT_DIR / "phase14_storyboard.json"
    with open(sb_path, "w", encoding="utf-8") as f:
        json.dump(STORYBOARD, f, indent=2)
    print(f"Generated Phase 14 Storyboard: {sb_path}")
    print(f"Total Duration: {STORYBOARD['total_duration_sec']}s across {len(STORYBOARD['beats'])} beats.")

if __name__ == "__main__":
    main()
