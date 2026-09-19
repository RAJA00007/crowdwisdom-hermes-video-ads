"""scripts/generate_phase16_storyboard.py

Generates Phase 16 outputs grounded strictly in research:
- outputs/videos/phase16_original_script.json
- outputs/videos/phase16_cinematic_storyboard.json
- outputs/videos/phase16_script_readable.md
"""

import json
from pathlib import Path

OUT_DIR = Path("outputs/videos")
OUT_DIR.mkdir(parents=True, exist_ok=True)

RESEARCH_METRICS = {
    "trader_inputs": "1,482,930",
    "directional_accuracy": "68.4%",
    "early_warning_lead": "14.6 HOURS",
    "tracked_tickers": 428
}

SCRIPT_DATA = {
    "project": "CrowdWisdomTrading - Phase 16 Cinematic Vox Storyboard",
    "target_icp": {
        "profile": "Discretionary retail & macro trader",
        "core_frustration": "Information overwhelm, lagging indicators, emotional second-guessing",
        "desired_state": "Calm, rules-based directional conviction ahead of price breakout"
    },
    "narrative_premise": {
        "hook": "At 2:17 in the morning, a trader isn't fighting the market. They're drowning in it.",
        "central_problem": "More data does not equal more clarity; it creates cognitive paralysis.",
        "central_insight": "True market edge comes from mathematically weighting peer consensus rather than consuming infinite news.",
        "provenance_claims": [
            "1,482,930 verified trader inputs",
            "68.4% directional accuracy",
            "14.6 hours early warning lead"
        ],
        "cta": "crowdwisdomtrading.com"
    },
    "total_target_duration_sec": 45.0,
    "scenes": [
        {
            "scene_id": "scene_01",
            "time_range": "0.0s - 5.0s",
            "duration": 5.0,
            "beat_title": "The Hook / Isolation",
            "narration": "At 2:17 in the morning, a trader isn't fighting the market. They're drowning in it.",
            "visual_argument": "Establish individual trader isolation against an uncaring, sleepless global market. The trader is solitary, framed by nocturnal city glow and rain streaks.",
            "visual_metaphor": "The lone lighthouse keeper surrounded by a silent storm.",
            "vox_components": [
                "halftone cutout of lone trader at desk",
                "archival paper border",
                "rough off-white keylines",
                "corner red crosshairs",
                "timestamp badge: [● 2:17 AM]"
            ],
            "depth_planes": {
                "fg": "Thin keyline framing, corner crosshairs, monospace session timestamp",
                "mg": "Trader cutout with soft drop shadow and subtle glow from twin monitors",
                "bg": "Nocturnal city bokeh with raindrops sliding down glass pane"
            },
            "camera": "Slow cinematic push-in (zoom 1.0 -> 1.05) maintaining trader centered",
            "transformation": "Still nocturnal calm pierced by low sub-bass pulse",
            "sound": "Room tone, distant clock tick, low tension sub-bass hit at 0.2s"
        },
        {
            "scene_id": "scene_02",
            "time_range": "5.0s - 10.0s",
            "duration": 5.0,
            "beat_title": "Information Overload / The Deluge",
            "narration": "Every second brings twenty new headlines, hundreds of opinions, and endless conflicting charts.",
            "visual_argument": "Visually demonstrate that data volume shrinks human decision-making capacity. As news cards multiply exponentially, the trader physically shrinks in the frame.",
            "visual_metaphor": "The Information Flood: news cards cascading and stacking until they smother the subject.",
            "vox_components": [
                "cascading archival headline fragments",
                "hot red warning banner: TOO MUCH INFORMATION",
                "scrolling ticker tape overlay",
                "halftone gray dot texture",
                "warning bracket keylines"
            ],
            "depth_planes": {
                "fg": "Hot Red warning banner, rapid scrolling financial ticker tape",
                "mg": "Cascading newspaper fragments and conflicting chart cutouts stacking forward",
                "bg": "Dim desk with frantic keyboard typing"
            },
            "camera": "Rapid camera pull-back (Ken Burns reverse) exaggerating spatial claustrophobia",
            "transformation": "INFORMATION FLOOD: Spatial expansion of noise pushing trader into background",
            "sound": "Rapid typewriter / keyboard clicks, rising high-frequency tension riser"
        },
        {
            "scene_id": "scene_03",
            "time_range": "10.0s - 15.0s",
            "duration": 5.0,
            "beat_title": "The Signal Problem / The Collapse",
            "narration": "More data doesn't create clarity. It creates noise.",
            "visual_argument": "Sudden total cessation of noise to create dramatic cognitive relief and focus on the fundamental failure of traditional retail information gathering.",
            "visual_metaphor": "The Vacuum Collapse: an explosion played in reverse, collapsing into a single stark question.",
            "vox_components": [
                "archival tan card (#C9BB9C)",
                "ink black typography: NOT ENOUGH SIGNAL.",
                "signature Hot Red offset underline (+12px)",
                "torn paper edge transition",
                "monospace metadata: EFFICIENCY < 0.2%"
            ],
            "depth_planes": {
                "fg": "Signature Hot Red hand-drawn underline expanding beneath 'NOT ENOUGH SIGNAL.'",
                "mg": "Crisp paper card with drop shadow floating centered",
                "bg": "Terminal monitor code freezing mid-stream into dark monochrome"
            },
            "camera": "Instant lock to dead-center stillness (zero camera drift)",
            "transformation": "INFORMATION COLLAPSE: 20 moving layers collapse instantly into 1 centered card",
            "sound": "Sudden vacuum cut of noise, 50 Hz sub-bass drop, paper friction snap"
        },
        {
            "scene_id": "scene_04",
            "time_range": "15.0s - 21.0s",
            "duration": 6.0,
            "beat_title": "The Insight / Collective Convergence",
            "narration": "CrowdWisdom unites the collective intelligence of 1,482,930 trader inputs.",
            "visual_argument": "Shift from solitary isolation to collective intelligence. Individual noisy data points synchronize into a single directional wave.",
            "visual_metaphor": "TRADER TO NETWORK: Isolated dots connecting into a glowing constellation of market consensus.",
            "vox_components": [
                "giant stat card: 1,482,930",
                "hot red pill badge: TRADER INPUTS",
                "topographical network keylines",
                "halftone crowd cutout overlay",
                "archival tan card with paper drop shadow"
            ],
            "depth_planes": {
                "fg": "Giant Impact stat hero: '1,482,930' with red 'TRADER INPUTS' badge",
                "mg": "Synchronized vector network lines connecting global trading hubs",
                "bg": "Dynamic pedestrian crowd movement treated with duotone print grain"
            },
            "camera": "Smooth upward tilt with parallax separation between network and crowd",
            "transformation": "NETWORK EXPANSION: Fragmented noise resolves into unified mathematical consensus",
            "sound": "Filtered crowd murmur resolving into clear bell-like harmonic data chimes (1175 Hz)"
        },
        {
            "scene_id": "scene_05",
            "time_range": "21.0s - 28.0s",
            "duration": 7.0,
            "beat_title": "The Proof / Empirical Edge",
            "narration": "68.4 percent accuracy. 14.6 hours of early warning.",
            "visual_argument": "Provide indisputable empirical proof grounded in the company's verified benchmark metrics. Hard numbers presented with institutional authority.",
            "visual_metaphor": "The Institutional Weighing Scale: Speculation vs Verified Historical Benchmark.",
            "vox_components": [
                "verified metric card 1: 68.4% DIRECTIONAL ACCURACY",
                "verified metric card 2: 14.6 HOURS EARLY WARNING LEAD",
                "institutional verification stamp: VERIFIED PERFORMANCE DATA",
                "mustard tag accent (#D9A441)",
                "rough white keyline borders"
            ],
            "depth_planes": {
                "fg": "Dual archival cards with Hot Red and Mustard accent blocks",
                "mg": "Real-world stock exchange price board and trading floor bell display",
                "bg": "Exchange trading floor with dynamic motion"
            },
            "camera": "Slow cinematic pan with steady card stabilization in foreground",
            "transformation": "METRIC STAMP: Dual proof cards slam down onto paper diorama surface",
            "sound": "Acoustic stock exchange bell strike (440/880 Hz), precision mechanical camera shutter click"
        },
        {
            "scene_id": "scene_06",
            "time_range": "28.0s - 35.0s",
            "duration": 7.0,
            "beat_title": "The Trader Payoff / Noise to Action",
            "narration": "Because an edge isn't more information. It's knowing which information matters.",
            "visual_argument": "Show the emotional and strategic payoff: from anxiety to calm, decisive action. The trader takes execution before the breakout is public.",
            "visual_metaphor": "NOISE TO SIGNAL TO ACTION: The red alert wash resolves into green execution clarity.",
            "vox_components": [
                "full-screen Hot Red alert wash flash (0.4s)",
                "hero card: NOISE → SIGNAL → ACTION",
                "hot red badge: EXECUTION ADVANTAGE",
                "paper diorama card with rough off-white keylines",
                "monospace status: SIGNAL CONVICTION CONFIRMED"
            ],
            "depth_planes": {
                "fg": "Hot Red alert wash flash (0.4s) fading into crisp 'NOISE → SIGNAL → ACTION' card",
                "mg": "Market momentum display showing breakout confirmation",
                "bg": "Trading floor / trader workspace shifting from chaotic to stabilized"
            },
            "camera": "Dynamic push into stabilized signal resolution",
            "transformation": "ALERT WASH: Brief 0.4s full-screen flash clearing the visual slate for decisive action",
            "sound": "Alert wash swell, clean keyboard Enter key stroke, warm low-frequency resolve chord"
        },
        {
            "scene_id": "scene_07",
            "time_range": "35.0s - 41.0s",
            "duration": 6.0,
            "beat_title": "The Product / CrowdWisdom Platform",
            "narration": "CrowdWisdom Trading.",
            "visual_argument": "Introduce the platform not as a generic software demo, but as the mathematical radar instrument that produces the edge.",
            "visual_metaphor": "The Alpha Radar: Cardinal compass points scanning the market horizon for high-conviction setups.",
            "vox_components": [
                "concentric polar radar reticle with cardinal axes",
                "pulsing alpha target blips with callout tags",
                "product header: CROWDWISDOM INTELLIGENCE PLATFORM",
                "sub-badge: REAL-TIME ALPHA SIGNALS",
                "archival paper frame margins"
            ],
            "depth_planes": {
                "fg": "Radar reticle, sweeping green/red scan line, +ALPHA target tags",
                "mg": "Archival tan card with platform title and alpha score gauges",
                "bg": "Blurred technical data stream in deep dark slate"
            },
            "camera": "Slow rotational drift and subtle scale (1.0 -> 1.04)",
            "transformation": "RADAR SWEEP: Continuous sweeping scan line locating verified market divergences",
            "sound": "High-tech radar ping, low warm analog synth pad sustained"
        },
        {
            "scene_id": "scene_08",
            "time_range": "41.0s - 45.0s",
            "duration": 4.0,
            "beat_title": "Brand Resolution & CTA",
            "narration": "See the signal inside the noise.",
            "visual_argument": "Deliver the final brand positioning with clean, authoritative permanence. High contrast, memorable, and uncluttered.",
            "visual_metaphor": "The Definitive Signature: The brand stamp resolving the entire 45-second inquiry.",
            "vox_components": [
                "headline: CROWDWISDOM TRADING",
                "positioning tagline: SEE THE SIGNAL INSIDE THE NOISE.",
                "hot red keyline divider bar",
                "cta domain pill: crowdwisdomtrading.com in Ink Black on Red",
                "monochrome copyright footer"
            ],
            "depth_planes": {
                "fg": "Hot red domain pill button and crisp white tagline",
                "mg": "Archival card with bold Ink Black brand title",
                "bg": "Dark nocturnal vignette with subtle rain bokeh"
            },
            "camera": "Static locked frame with gradual fade to black beginning at 44.5s",
            "transformation": "FINAL RESOLVE: All editorial elements lock into place, fading gracefully to black",
            "sound": "Final warm orchestral/synth chord resolve with natural decay, silence on fade"
        }
    ]
}


def build_readable_markdown(script_data: dict) -> str:
    md = []
    md.append("# Phase 16: Research-Driven Original Script & Cinematic Vox Storyboard\n")
    md.append("## Target ICP & Strategic Foundation\n")
    md.append(f"- **Target Trader**: {script_data['target_icp']['profile']}")
    md.append(f"- **Core Frustration**: {script_data['target_icp']['core_frustration']}")
    md.append(f"- **Desired Emotional Shift**: {script_data['target_icp']['desired_state']}\n")
    md.append("## Core Research Claims (Strictly Verified)\n")
    for claim in script_data["narrative_premise"]["provenance_claims"]:
        md.append(f"- **{claim}**")
    md.append("\n---\n")

    md.append("## 45-Second Narrative Storyboard Breakdown\n")

    for sc in script_data["scenes"]:
        md.append(f"### {sc['scene_id'].upper()}: {sc['beat_title'].upper()}")
        md.append(f"- **Time**: `{sc['time_range']}` ({sc['duration']}s)")
        md.append(f"- **Narration**: *\"{sc['narration']}\"*")
        md.append(f"- **Visual Argument**: {sc['visual_argument']}")
        md.append(f"- **Visual Metaphor**: {sc['visual_metaphor']}")
        md.append(f"- **Vox Components**: {', '.join(sc['vox_components'])}")
        md.append(f"- **2.5D Depth Structure**:")
        md.append(f"  - **FG**: {sc['depth_planes']['fg']}")
        md.append(f"  - **MG**: {sc['depth_planes']['mg']}")
        md.append(f"  - **BG**: {sc['depth_planes']['bg']}")
        md.append(f"- **Camera Movement**: {sc['camera']}")
        md.append(f"- **Visual Transformation**: `{sc['transformation']}`")
        md.append(f"- **Sound Design**: {sc['sound']}\n")

    md.append("---\n")
    md.append("## Human Review Summary: STORY_READY_FOR_RENDER\n")
    md.append("- **Target ICP**: Discretionary retail & macro traders suffering from information overload")
    md.append("- **Central Problem**: Data volume creates noise, second-guessing, and emotional mistakes")
    md.append("- **Central Insight**: Alpha comes from mathematically weighting collective conviction, not reading more news")
    md.append("- **Hook**: 'At 2:17 in the morning, a trader isn't fighting the market. They're drowning in it.'")
    md.append("- **Narrative Arc**: Hook (Isolation) → Escalation (Flood) → Collapse (Question) → Insight (Network) → Proof (68.4% / 14.6h) → Payoff (Action) → Product (Radar) → CTA")
    md.append("- **Strongest Visual Metaphor**: The Information Flood collapsing instantly into a single stark red underline, then expanding into a global predictive network")
    md.append("- **Approved Statistics**: 1,482,930 trader inputs | 68.4% directional accuracy | 14.6 hours early warning lead")
    md.append("- **CTA**: crowdwisdomtrading.com | SEE THE SIGNAL INSIDE THE NOISE.\n")

    return "\n".join(md)


def main():
    # 1. Write phase16_original_script.json
    script_json_path = OUT_DIR / "phase16_original_script.json"
    with open(script_json_path, "w", encoding="utf-8") as f:
        json.dump(SCRIPT_DATA, f, indent=2)
    print(f"Wrote script to {script_json_path}")

    # 2. Write phase16_cinematic_storyboard.json
    storyboard_data = {
        "project": "CrowdWisdomTrading - Phase 16 Cinematic Vox Storyboard",
        "total_duration_sec": SCRIPT_DATA["total_target_duration_sec"],
        "resolution": {"width": 1080, "height": 1920, "aspect_ratio": "9:16", "fps": 30},
        "style_mode": "cinematic_vox_explainer",
        "company_art_direction": "assets/style_reference/company_art_direction.png",
        "verified_statistics": RESEARCH_METRICS,
        "scenes": SCRIPT_DATA["scenes"]
    }
    storyboard_json_path = OUT_DIR / "phase16_cinematic_storyboard.json"
    with open(storyboard_json_path, "w", encoding="utf-8") as f:
        json.dump(storyboard_data, f, indent=2)
    print(f"Wrote cinematic storyboard to {storyboard_json_path}")

    # 3. Write phase16_script_readable.md
    readable_md_path = OUT_DIR / "phase16_script_readable.md"
    md_content = build_readable_markdown(SCRIPT_DATA)
    with open(readable_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Wrote readable script markdown to {readable_md_path}")


if __name__ == "__main__":
    main()
