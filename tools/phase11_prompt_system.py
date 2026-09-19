"""tools/phase11_prompt_system.py

Phase 11 Cinematic AI Video Prompt System for CrowdWisdomTrading Short Film Ad.

Implements the high-fidelity cinematic prompt architecture:
- SUBJECT
- ENVIRONMENT
- TIME
- LIGHTING
- MATERIAL
- CAMERA
- LENS FEEL
- DEPTH
- FOREGROUND
- MIDGROUND
- BACKGROUND
- MOTION
- ATMOSPHERE
- EDITORIAL STYLE
- COLOR
- TRANSITION INTENT

Enforces strict negative prompting to eliminate plastic AI looks, cheesy stock acting, and AI typography.
Compatible with Python 3.10.
"""

from typing import Any, Dict, List, Optional


PHASE11_NEGATIVE_PROMPT = (
    "glossy CGI, plastic humans, wax faces, deformed hands, extra fingers, duplicate people, "
    "floating objects, impossible physics, cyberpunk, neon, futuristic HUD, crypto aesthetic, "
    "generic corporate stock footage, generic office scenes, cheesy acting, smiling businessman, "
    "fake charts, fake UI, random text, gibberish text, invented logos, watermark, excessive lens flare, "
    "oversaturated colors, cartoon style, cheap motion graphics, slideshow appearance, flat 2D animation"
)

PHASE11_EDITORIAL_PALETTE = {
    "archival_tan": "#C9BB9C",
    "ink_black": "#1A1A1A",
    "halftone_gray": "#8C8C8C",
    "hot_red": "#D62E1F",
    "mustard": "#D9A441",
}


def build_phase11_cinematic_prompt(
    subject: str,
    environment: str,
    time_of_day: str,
    lighting: str,
    material: str,
    camera: str,
    lens_feel: str,
    depth: str,
    foreground: str,
    midground: str,
    background: str,
    motion: str,
    atmosphere: str,
    editorial_style: str,
    color: str,
    transition_intent: str,
) -> str:
    """Construct an uncompromising Phase 11 Cinematic AI Video prompt."""
    prompt_blocks = [
        f"SUBJECT: {subject}",
        f"ENVIRONMENT: {environment}",
        f"TIME: {time_of_day}",
        f"LIGHTING: {lighting}",
        f"MATERIAL: {material}",
        f"CAMERA: {camera}",
        f"LENS FEEL: {lens_feel}",
        f"DEPTH: {depth}",
        f"FOREGROUND: {foreground}",
        f"MIDGROUND: {midground}",
        f"BACKGROUND: {background}",
        f"MOTION: {motion}",
        f"ATMOSPHERE: {atmosphere}",
        f"EDITORIAL STYLE: {editorial_style}",
        f"COLOR: {color}",
        f"TRANSITION INTENT: {transition_intent}",
    ]
    return "\n".join(prompt_blocks)


def get_phase11_storyboard_definitions() -> List[Dict[str, Any]]:
    """Return the authoritative 8-beat Cinematic Short Film storyboard definition."""
    return [
        # -------------------------------------------------------------
        # BEAT 1: CINEMATIC HOOK (0-5s)
        # -------------------------------------------------------------
        {
            "beat_id": 1,
            "scene_id": "beat_01",
            "name": "The 2:17 AM Hook",
            "start_time": 0.0,
            "end_time": 5.0,
            "duration": 5.0,
            "prompt_data": {
                "subject": "Exhausted 32-year-old retail options trader sitting alone in deep psychological concentration, eyes reflecting shifting financial data, intense focused expression without melodrama",
                "environment": "Dimly lit city apartment trading room at 2:17 AM, rain-streaked high-rise window in background with distant nocturnal city skyline bokeh",
                "time_of_day": "2:17 AM dead of night",
                "lighting": "Low-key chiaroscuro with cold 6500K monitor luminescence sculpting facial profile contrasted against subtle 2700K warm incandescent practical desk lamp",
                "material": "Authentic tactile skin texture with natural stubble, matte cotton crewneck, aged archival desk paper, print-grain textures embedded on desk surfaces",
                "camera": "Slow deliberate cinematic dolly push-in toward the trader profile from a three-quarters rear-side perspective",
                "lens_feel": "35mm documentary anamorphic prime lens, shallow depth of field (f/1.8), organic chromatic subtlety",
                "depth": "Three distinct spatial planes: out-of-focus monitor edge and paper fragments in near foreground, trader in razor-sharp midground, deep dark room with soft urban window bokeh in background",
                "foreground": "Edge of an illuminated terminal screen and scattered printed market sheets passing softly out of focus near lens",
                "midground": "Trader profile illuminated by terminal glow, hand hovering near analog watch and desk surface",
                "background": "Deep shadowed studio apartment room with second distant monitor glow and dark rainy city window",
                "motion": "Subtle organic breathing and micro-eyetracking, slow smooth camera translation pushing past foreground clutter",
                "atmosphere": "Heavy tension, nocturnal isolation, atmospheric haze catching monitor beam, serious investigative journalism tone",
                "editorial_style": "High-tension Fincher neo-noir meets Vox investigative journalism; tactile, grounded, zero sci-fi glossy plastic",
                "color": "Deep obsidian shadows, cold monitor slate, accented by single strategic warm tungsten amber and subtle archival tan tones (#C9BB9C)",
                "transition_intent": "Camera pushes through rising tension, accelerating slightly at second 4.8 before a hard cut to black silence",
            },
            "post_typography": "TOO MUCH INFORMATION. (deterministic title card post-cut)",
            "sound_design": "Low room tone, faint electrical hum of monitors, quiet distant keyboard click, slow mechanical clock tick, sudden hard cut to silence at 5.0s",
            "narration": "At 2:17 in the morning, the problem isn't a lack of information.",
        },
        # -------------------------------------------------------------
        # BEAT 2: INFORMATION FLOOD (5-10s)
        # -------------------------------------------------------------
        {
            "beat_id": 2,
            "scene_id": "beat_02",
            "name": "Information Flood",
            "start_time": 5.0,
            "end_time": 10.0,
            "duration": 5.0,
            "prompt_data": {
                "subject": "Swarm of authentic financial newsprint columns, archival data sheets, paper ticker strips, and red editorial annotation marks physically suspended and rushing through three-dimensional space",
                "environment": "Architectural media abyss; physical newspaper columns and financial documentation drifting across an infinite dark studio space",
                "time_of_day": "Timeless editorial void",
                "lighting": "Directional rim lighting highlighting torn paper fibers, fibrous paper translucency, and sharp printed ink letters",
                "material": "Aged newsprint, cotton fiber archival parchment (#C9BB9C), textured printer ink, tactile paper edges with physical shadows",
                "camera": "Fast cinematic lateral track passing through physical paper layers, followed by a dramatic hard stop with physical overshoot at second 9.2",
                "lens_feel": "50mm high-speed prime with shallow depth of field, rapid foreground motion blur",
                "depth": "Dense multi-layered spatial field where paper fragments cross within inches of the front element while background stacks recede deeply",
                "foreground": "Torn financial headline fragments and red annotation strokes rushing past the lens with heavy motion blur",
                "midground": "Overlapping conflicting financial statements and analyst reports suspended in mid-motion",
                "background": "Faded dense columns of antique financial newspapers and nautical grid maps receding into soft darkness",
                "motion": "Fast turbulent drifting of paper elements that abruptly snap-freezes in place at second 9.2 with physical spring settling",
                "atmosphere": "Sensory cognitive overload, relentless velocity of market noise, claustrophobic deluge of data",
                "editorial_style": "Editorial documentary montage; physical print collage brought to lifelike physical motion",
                "color": "Archival tan (#C9BB9C), deep newsprint ink black (#1A1A1A), punctuated by sharp Hot Red strokes (#D62E1F)",
                "transition_intent": "Hard freeze at second 9.5 holding on locked chaotic fragments, cutting abruptly into pure minimal calm",
            },
            "post_typography": "ALERT // MARKET NOISE (rendered in post)",
            "sound_design": "Rising cacophony of rustling paper sheets, fluttering ticker tape, digital notification blips, crescendo building to hard snap stop",
            "narration": "It's too much of it.",
        },
        # -------------------------------------------------------------
        # BEAT 3: THE REAL PROBLEM (10-14s)
        # -------------------------------------------------------------
        {
            "beat_id": 3,
            "scene_id": "beat_03",
            "name": "The Real Problem: Noise vs Signal",
            "start_time": 10.0,
            "end_time": 14.0,
            "duration": 4.0,
            "prompt_data": {
                "subject": "Pristine, uncluttered architectural archival paper canvas with microscopic paper fiber weave and subtle tactile grain",
                "environment": "Locked documentary stage with subtle ambient lighting shift from shadows into clarity",
                "time_of_day": "Abstract editorial space",
                "lighting": "Even, soft studio daylight grazing across the paper texture from a 45-degree high angle, casting micro-shadows into paper fibers",
                "material": "Aged museum-grade archival tan paper (#C9BB9C) with subtle linen grain and antique map watermark linework",
                "camera": "Extremely slow, dignified 1% lateral camera drift, rock-steady locked horizon",
                "lens_feel": "85mm architectural prime, zero distortion, razor-sharp edge-to-edge optical clarity",
                "depth": "Deliberately compressed two-plane editorial canvas creating a breathing space of profound calm after chaos",
                "foreground": "Clean empty space reserved for post-production headline typography",
                "midground": "Subtle antique nautical coordinates and grid lines etched faintly into paper texture",
                "background": "Warm archival tan paper grain with soft organic light gradient",
                "motion": "Almost imperceptible smooth camera float, zero chaotic drift",
                "atmosphere": "Profound silence, surgical precision, investigative journalism gravitas",
                "editorial_style": "Premium Vox/Criterion documentary title card aesthetics",
                "color": "Dominated by rich Archival Tan (#C9BB9C) and Ink Black (#1A1A1A) with single Hot Red accent (#D62E1F)",
                "transition_intent": "Holds steadily as kinetic typography lands; smooth seamless match-cut to human crowd montage",
            },
            "post_typography": "TOO MUCH INFORMATION. / NOT ENOUGH SIGNAL. (with Hot Red underline)",
            "sound_design": "Sudden pure silence, deep low-frequency sub pulse (40Hz), single crisp typewriter stamp click",
            "narration": "Thousands of traders are watching the same market from completely different perspectives.",
        },
        # -------------------------------------------------------------
        # BEAT 4: CROWD SIGNAL (14-20s)
        # -------------------------------------------------------------
        {
            "beat_id": 4,
            "scene_id": "beat_04",
            "name": "Crowd Signal Convergence",
            "start_time": 14.0,
            "end_time": 20.0,
            "duration": 6.0,
            "prompt_data": {
                "subject": "Cinematic montage of diverse individual traders in realistic environments: a woman reviewing charts on a laptop in a sunlit Tokyo apartment, a man studying mobile indicators on a train platform, an analyst at a multi-monitor desk",
                "environment": "Authentic realistic global trading environments across distinct time zones and interior settings",
                "time_of_day": "Mixed global day, dusk, and late-night conditions",
                "lighting": "Naturalistic environmental lighting unique to each space: morning daylight, neon train platform ambiance, interior desk lamps",
                "material": "Photorealistic human skin, cotton, wool, glass reflections, layered with subtle halftone dot screening and tactile red thread overlays",
                "camera": "Dynamic rhythmic cutting between intimate documentary portraits, connected by physical red editorial line trajectories",
                "lens_feel": "50mm and 85mm portrait lenses with soft bokeh and authentic optical flares",
                "depth": "Each portrait features realistic depth of field with environmental context, tied together by graphic red signal connections in foreground space",
                "foreground": "Glowing Hot Red editorial vector lines weaving through physical spatial coordinates",
                "midground": "Independent authentic traders engaged in real observation and decision making",
                "background": "Realistic lived-in rooms and transit environments with organic detail",
                "motion": "Subtle natural human gestures (glancing, zooming chart, scrolling) interconnected by energetic red lines drawing between them",
                "atmosphere": "Collective human intelligence, decentralized conviction, emerging order",
                "editorial_style": "Human-centric visual journalism meets editorial motion design",
                "color": "Natural cinematic interior palettes connected by vibrant, electric Hot Red (#D62E1F) signal threads",
                "transition_intent": "Red threads accelerate and converge into a single dense focal point, leading into data proof",
            },
            "post_typography": "1,482,930 / TRADER INPUTS / Fig. 2 - Aggregated Conviction (post-overlay)",
            "sound_design": "Subtle rhythmic pulse, distant ambient urban soundscapes weaving together, rising low-frequency harmonic resonance",
            "narration": "CrowdWisdom turns that collective signal into something you can act on. 1.48 million trader inputs.",
        },
        # -------------------------------------------------------------
        # BEAT 5: SIGNAL BECOMES INTELLIGENCE (20-27s)
        # -------------------------------------------------------------
        {
            "beat_id": 5,
            "scene_id": "beat_05",
            "name": "Signal Becomes Intelligence (Data Proof)",
            "start_time": 20.0,
            "end_time": 27.0,
            "duration": 7.0,
            "prompt_data": {
                "subject": "Swarm of scattered red paper pins and fragmented data cards physically organizing into an elegant, clean directional trajectory and geometric consensus path",
                "environment": "Three-dimensional paper diorama studio with antique navigation charts layered at the base",
                "time_of_day": "Abstract analytical clarity",
                "lighting": "Crisp focused key light illuminating the rising trajectory line with deep cast paper drop shadows",
                "material": "Physical cut-paper cards, white paper borders, Hot Red inked trajectory lines, mustard callout badges (#D9A441)",
                "camera": "Committed quarter-orbit dolly move ascending alongside the directional signal trajectory",
                "lens_feel": "45mm tilt-shift documentary perspective creating crisp selective plane of focus along the signal line",
                "depth": "Clear multi-tiered physical elevation: base navigation chart, midground elevation pins, foreground hero metric display cards",
                "foreground": "Clean paper stat pedestals preparing for post-rendered verification figures",
                "midground": "Sharp Hot Red directional line rising past validation coordinate markers",
                "background": "Muted archival newsprint columns sitting softly out of focus",
                "motion": "Chaotic particles snap cleanly onto the vector line; smooth continuous ascent of camera along trajectory",
                "atmosphere": "Mathematical authority, measurable predictive advantage, indisputable proof",
                "editorial_style": "High-end Financial Times / Economist data journalism brought to physical kinetic reality",
                "color": "Archival Tan (#C9BB9C), Ink Black (#1A1A1A), Hot Red (#D62E1F), and Mustard (#D9A441)",
                "transition_intent": "Camera reaches peak elevation of vector, locking smoothly on the destination coordinates",
            },
            "post_typography": "68.4% DIRECTIONAL ACCURACY / 14.6h EARLY-WARNING LEAD TIME (rendered in post)",
            "sound_design": "Crisp mechanical clock ticks, ascending musical chord build, clean paper pop transients, solid resonant thump on lock",
            "narration": "68.4 percent directional accuracy. And signals arriving up to 14.6 hours earlier.",
        },
        # -------------------------------------------------------------
        # BEAT 6: THE PAYOFF (27-34s)
        # -------------------------------------------------------------
        {
            "beat_id": 6,
            "scene_id": "beat_06",
            "name": "Trader Payoff: The Clarity of Conviction",
            "start_time": 27.0,
            "end_time": 34.0,
            "duration": 7.0,
            "prompt_data": {
                "subject": "Return to the exact same 32-year-old trader from Beat 1, now in a posture of complete calm, composed posture, eyes illuminated by a single clear consensus signal path on screen",
                "environment": "The same 2:17 AM apartment desk room, but transformed from chaotic clutter into focused clarity",
                "time_of_day": "2:17 AM late nocturnal resolution",
                "lighting": "Warm golden-red rim light illuminating trader's profile, dark room softly bathed in focused terminal glow",
                "material": "Authentic human skin, dark cotton crewneck, matte monitor bezel, clean physical paper note on desk with red pin",
                "camera": "Slow confident dolly push-in toward trader's composed face and monitor view",
                "lens_feel": "50mm intimate cinema prime, shallow depth of field (f/2.0), clean natural bokeh",
                "depth": "Traders hands and desk notes in soft foreground, trader face and terminal in sharp midground, rainy window in background",
                "foreground": "Clean organized desk edge with single physical notepad and red marker pin",
                "midground": "Trader looking directly at the verified inflection signal, slight subtle nod of recognition",
                "background": "Calm nocturnal apartment atmosphere, rain on dark window panes",
                "motion": "Subtle natural breath, single deliberate eye motion, camera pushes steadily with cinematic gravity",
                "atmosphere": "Total emotional relief, mastery, calm in the storm, psychological conviction",
                "editorial_style": "Prestige cinematic drama, subtle character acting without exaggerated melodrama",
                "color": "Atmospheric nocturnal blues and blacks accented by warm skin tones, archival tan desk, and Hot Red (#D62E1F) consensus vector",
                "transition_intent": "Brief strategic ALERT_WASH flood at second 29.5 as conviction lands, resolving back to clear focus",
            },
            "post_typography": "CROWD SENTIMENT SIGNAL PATH // PREDICTIVE PATH VERIFIED (rendered in post)",
            "sound_design": "Warm cello note sustaining, tension dissipates into a clean, resonant sub-bass exhale, room tone returns to calm",
            "narration": "Because in markets, seeing everything isn't the advantage. Knowing what matters is.",
        },
        # -------------------------------------------------------------
        # BEAT 7: PRODUCT REVEAL (34-40s)
        # -------------------------------------------------------------
        {
            "beat_id": 7,
            "scene_id": "beat_07",
            "name": "Product Context: Early-Warning Radar",
            "start_time": 34.0,
            "end_time": 40.0,
            "duration": 6.0,
            "prompt_data": {
                "subject": "CrowdWisdom platform interface elegantly mounted inside a tactile cut-paper frame with fine bevel drop shadow and archival paper matte",
                "environment": "Architectural editorial studio stage with aged nautical map background and linen texture",
                "time_of_day": "Timeless editorial environment",
                "lighting": "Refined gallery display lighting, soft rim light grazing the cut-paper borders and screen glass",
                "material": "Real product interface capture, white cardstock matte border, archival tan backing (#C9BB9C), textured drop shadow",
                "camera": "Slow controlled quarter-orbit reveal with subtle 2% push-in, perfectly centered and stable",
                "lens_feel": "60mm macro editorial prime, flat distortion-free perspective, crisp edge micro-contrast",
                "depth": "Receding tactile paper layers: archival tan base canvas, drop shadow, white cut-paper matte mount, mounted platform display",
                "foreground": "Clean lower editorial space for platform category identification",
                "midground": "Mounted CrowdWisdom consensus radar interface with subtle live data pulse",
                "background": "Aged archival paper field with antique coordinate linework",
                "motion": "Gentle fluid camera float, restrained subtle UI data pulse, zero aggressive 3D rotations",
                "atmosphere": "Institutional credibility, technological elegance, restrained mastery",
                "editorial_style": "Minimalist Scandinavian design meets classic financial journalism",
                "color": "Neutral cream white card, Archival Tan (#C9BB9C), Ink Black (#1A1A1A), with Hot Red (#D62E1F) conviction highlights",
                "transition_intent": "Gracefully holds center stage before cutting to the minimal final brand CTA card",
            },
            "post_typography": "CROWDWISDOM TRADING // PROPRIETARY PLATFORM // EARLY-WARNING SENTIMENT RADAR",
            "sound_design": "Deep warm pad, delicate high-frequency interface chime, clean tactile paper settling sound",
            "narration": "CrowdWisdom Trading.",
        },
        # -------------------------------------------------------------
        # BEAT 8: FINAL CTA (40-45s)
        # -------------------------------------------------------------
        {
            "beat_id": 8,
            "scene_id": "beat_08",
            "name": "Final Call To Action",
            "start_time": 40.0,
            "end_time": 45.0,
            "duration": 5.0,
            "prompt_data": {
                "subject": "Minimalist, monumental brand identity composition on premium Archival Tan paper canvas (#C9BB9C) with refined double hairline border",
                "environment": "Locked archival stage with subtle organic fiber grain and soft matte finish",
                "time_of_day": "Locked documentary stage",
                "lighting": "Warm, even editorial light casting subtle depth across the paper surface",
                "material": "Aged archival paper (#C9BB9C), high-contrast ink black lettering (#1A1A1A), crisp Hot Red accent underline (#D62E1F)",
                "camera": "Extremely slow 1% push-in drift, holding rock-steady to maximize reading comprehension",
                "lens_feel": "85mm classic portrait lens, flat planar perspective, zero distortion",
                "depth": "Deliberately serene, uncluttered stage allowing the brand statement to command total visual authority",
                "foreground": "CROWDWISDOM TRADING / SEE THE SIGNAL INSIDE THE NOISE. / crowdwisdomtrading.com",
                "midground": "Hot Red underline swipe and rounded paper button container",
                "background": "Archival tan paper fiber texture with antique framing rule",
                "motion": "Subtle 1% camera push, stable text lockup, final frame breathes peacefully",
                "atmosphere": "Definitive authority, quiet confidence, indelible closing impression",
                "editorial_style": "Classic high-end editorial book typography and timeless institutional identity",
                "color": "Archival Tan (#C9BB9C), Ink Black (#1A1A1A), Hot Red (#D62E1F)",
                "transition_intent": "Holds steadily through second 45.0 before smooth fade to black",
            },
            "post_typography": "CROWDWISDOM TRADING / SEE THE SIGNAL INSIDE THE NOISE. / crowdwisdomtrading.com",
            "sound_design": "Warm final chord resolves into gentle room tone, concluding with a solid definitive bass tone",
            "narration": "See the signal inside the noise. Visit crowdwisdomtrading.com.",
        },
    ]
