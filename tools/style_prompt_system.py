"""tools/style_prompt_system.py

Official Company-Provided Prompt System for CrowdWisdomTrading Video Ads.
Translates the company-provided textual production specification into a reusable
prompt generation engine.

Exact Company-Provided Style Blocks:
- Flat Parallax
- Deep Diorama
- Locked Stage
- Shot Construction Rules (BACKGROUND, MG, FG, CAMERA, SETTLE)
- Camera Move Library
- Escalation Devices
- Audio Construction Rules (sound design only, no music, no narration)
- Avoid Rules (Flat Parallax / Locked Stage vs Deep Diorama)
- Sequencing Rules

DO NOT rewrite or summarize the company-provided style blocks.
"""

from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# OFFICIAL COMPANY-PROVIDED PROMPT BLOCKS (VERBATIM)
# ============================================================

COMPANY_STYLE_BLOCK_A_FLAT_PARALLAX = (
    "Use the attached style sheet as the strict visual system — match its aged-newsprint "
    "collage surface, desaturated archival palette with one hot accent, condensed headline caps "
    "with giant stat numbers, halftone black-and-white cutout people with rough white keylines and "
    "offset accent strokes, and its print-grain finish. Do NOT copy the sheet's layout; it defines "
    "the language, not the composition. Layers sit at distinct depths like a paper diorama — true "
    "parallax, never glossy 3D. Backgrounds are muted archival fields, varying per clip within this "
    "palette. ALERT WASH means the whole frame floods toward the hot accent tone. Motion: spring "
    "pop-ups with overshoot, staggered entrances, ticking counters, underline swipes; one slow camera "
    "move per clip. Audio: sound design only — paper pops, thwips, stamps, ticks, low newsroom hum. "
    "No music. No voice-over."
)

COMPANY_STYLE_BLOCK_B_DEEP_DIORAMA = (
    "Use the attached style sheet for materials only — aged-print collage textures, halftone "
    "black-and-white cutout people with rough keylines and offset accent strokes, giant stat "
    "numbers, print grain. Do NOT copy the sheet's layout or its flatness: every clip is a deep 3D "
    "paper diorama — cutouts are physical layers separated in real space, strong shallow depth of "
    "field, foreground elements crossing close to the lens. The camera is an actor: it flies between "
    "layers, orbits, dives, whips, racks focus — one committed cinematic move per clip. Backgrounds "
    "change per clip, always within the sheet's palette. ALERT WASH means the entire frame floods to "
    "the hot accent tone in one beat. Motion: springs with overshoot, staggered entrances, ticking "
    "counters. Audio: sound design only — paper pops, whooshes, stamps, ticks. No music. No voice-over."
)

COMPANY_STYLE_BLOCK_C_LOCKED_STAGE = (
    "Documentary cutout-collage stage: a locked, muted archival map/texture background that never "
    "changes. Midground: black-and-white halftone cutouts with a rough white keyline and an offset "
    "red marker stroke behind each. Foreground: structures, props, and big stat numbers in full "
    "color. Condensed bold headline caps; numbers rendered huge, as characters. Desaturated "
    "palette plus one hot red accent, secondary mustard. Spring pop-ups with slight overshoot, "
    "staggered entrances, counters ticking up, red underline swipes. Camera: subtle slow drift "
    "only, never cuts."
)

COMPANY_AVOID_FLAT_PARALLAX_LOCKED_STAGE = (
    "AVOID: no glossy CG 3D, no lens flares, no camera cuts within the clip, no full-color "
    "midground portraits (people stay halftone black-and-white), no warped or gibberish text, "
    "no invented logos, no watermarks, no simultaneous entrances, no music, no soundtrack, "
    "no voice-over, no narration, no lyrics"
)

COMPANY_AVOID_DEEP_DIORAMA = (
    "AVOID: no flat single-plane composition, no static locked-off camera, no glossy plastic CG "
    "(depth stays papercraft), no full-color midground portraits (people stay halftone black-and-white), "
    "no warped or gibberish text, no invented logos, no watermarks, no music, no soundtrack, "
    "no voice-over, no narration, no lyrics"
)

COMPANY_AVOID_TECH_ADDENDUM = "no UI or glass elements"

ALLOWED_CAMERA_MOVES = [
    "push-in",
    "slow drift lateral",
    "dive through a layer",
    "orbit quarter turn",
    "whip ×2–3, each landing hard",
    "fast lateral track then hard stop with overshoot",
    "climb alongside a rising element",
    "fly low between columns",
    "ride a path like a rail",
    "macro slide along an object, rack focus tip→subject",
]

CAMERA_SOUND_MAPPINGS = {
    "dive through a layer": ["submerge whoosh", "deep pressure hum"],
    "whip ×2–3, each landing hard": ["three whip whooshes", "pops landing each hit"],
    "fast lateral track then hard stop with overshoot": ["track rumble", "stall click", "drain hiss"],
    "push-in": ["subtle paper slide", "clock tick", "quiet room tone"],
    "slow drift lateral": ["quiet room tone", "paper rustle", "faint room tone"],
    "alert wash": ["rising air riser", "deep sub thud"],
    "loop": ["accelerating ticks", "whoosh per lap"],
    "tension": ["rubber creak", "room tone falling to near silence"],
}


# ============================================================
# API FUNCTIONS
# ============================================================

def get_flat_parallax_style() -> str:
    """Return verbatim Company Style Block A — Flat Parallax."""
    return COMPANY_STYLE_BLOCK_A_FLAT_PARALLAX


def get_deep_diorama_style() -> str:
    """Return verbatim Company Style Block B — Deep Diorama."""
    return COMPANY_STYLE_BLOCK_B_DEEP_DIORAMA


def get_locked_stage_style() -> str:
    """Return verbatim Company Style Block C — Locked Stage."""
    return COMPANY_STYLE_BLOCK_C_LOCKED_STAGE


def build_shot_prompt(
    background: str,
    mg: str,
    fg: str,
    camera: str,
    settle: str,
    depth_description: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> str:
    """Construct a company-compliant SHOT block.

    Must contain:
    BACKGROUND: Sets depth field
    MG: Defines subject cutouts
    FG: Defines data element
    CAMERA: ONE committed camera move
    SETTLE: Defines final frame

    Every text element explicitly tagged: (headline), (label), (counter), (giant number).
    Every prompt must explicitly describe depth.
    """
    lines = []

    # Depth annotation
    if depth_description:
        lines.append(f"DEPTH: {depth_description.strip()}")

    # Tags annotation if provided separately
    if tags:
        tag_lines = [f"{k}: {v}" for k, v in tags.items()]
        lines.append("ELEMENT TAGS: " + "; ".join(tag_lines))

    lines.append(f"BACKGROUND: {background.strip()}")
    lines.append(f"MG: {mg.strip()}")
    lines.append(f"FG: {fg.strip()}")
    lines.append(f"CAMERA: {camera.strip()} (ONE committed camera move)")
    lines.append(f"SETTLE: {settle.strip()}")

    return "\n".join(lines)


def build_audio_prompt(
    camera_move: Optional[str] = None,
    sounds: Optional[List[str]] = None,
) -> str:
    """Construct a company-compliant AUDIO block.

    Rule:
    AUDIO:
    [2–3 sounds, comma separated] — sound design only, no music, no narration.
    Sound must mirror the camera movement.
    """
    if sounds and len(sounds) > 0:
        sound_list = sounds[:3]
    elif camera_move and camera_move.lower() in CAMERA_SOUND_MAPPINGS:
        sound_list = CAMERA_SOUND_MAPPINGS[camera_move.lower()]
    else:
        sound_list = ["paper pops", "subtle click", "tactile thwip"]

    sound_str = ", ".join(sound_list)
    return f"AUDIO:\n[{sound_str}] — sound design only, no music, no narration."


def build_avoid_prompt(
    style_type: str,
    has_tech_or_ui: bool = False,
) -> str:
    """Construct a company-compliant AVOID block based on style block selection."""
    style_norm = style_type.lower().replace("-", "_").replace(" ", "_")
    if "deep" in style_norm:
        base_avoid = COMPANY_AVOID_DEEP_DIORAMA
    else:
        base_avoid = COMPANY_AVOID_FLAT_PARALLAX_LOCKED_STAGE

    if has_tech_or_ui:
        return f"{base_avoid}, {COMPANY_AVOID_TECH_ADDENDUM}"
    return base_avoid


def build_complete_generation_prompt(
    style_type: str,
    shot_params: Dict[str, Any],
    sounds: Optional[List[str]] = None,
    has_tech_or_ui: bool = False,
) -> str:
    """Assemble the 4-part authoritative generation prompt:

    STYLE BLOCK
    +
    SHOT
    +
    AUDIO
    +
    AVOID

    Does NOT collapse these into one generic paragraph.
    """
    style_norm = style_type.lower().replace("-", "_").replace(" ", "_")
    if "deep" in style_norm:
        style_block = get_deep_diorama_style()
    elif "locked" in style_norm:
        style_block = get_locked_stage_style()
    else:
        style_block = get_flat_parallax_style()

    shot_block = build_shot_prompt(
        background=shot_params.get("background", ""),
        mg=shot_params.get("mg", ""),
        fg=shot_params.get("fg", ""),
        camera=shot_params.get("camera", "slow drift lateral"),
        settle=shot_params.get("settle", ""),
        depth_description=shot_params.get("depth_description", "at three different physical depths"),
        tags=shot_params.get("tags", None),
    )

    audio_block = build_audio_prompt(
        camera_move=shot_params.get("camera", ""),
        sounds=sounds,
    )

    avoid_block = build_avoid_prompt(
        style_type=style_type,
        has_tech_or_ui=has_tech_or_ui,
    )

    sections = [
        "============================================================",
        "STYLE BLOCK",
        "============================================================",
        style_block,
        "",
        "============================================================",
        "SHOT",
        "============================================================",
        shot_block,
        "",
        "============================================================",
        "AUDIO",
        "============================================================",
        audio_block,
        "",
        "============================================================",
        "AVOID",
        "============================================================",
        avoid_block,
    ]

    return "\n".join(sections)


def validate_camera_move(camera_str: str) -> Tuple[bool, str]:
    """Validate that camera move specifies exactly ONE committed camera move."""
    cam_lower = camera_str.lower()
    
    # Check contradictory multi-moves
    contradictions = [
        ("push-in", "pull back"),
        ("push in", "pull back"),
        ("push-in", "orbit"),
        ("push in", "orbit"),
        ("orbit", "whip"),
        ("dive", "whip"),
        ("fast lateral", "orbit"),
    ]
    for m1, m2 in contradictions:
        if m1 in cam_lower and m2 in cam_lower:
            return False, f"Contradictory multiple camera moves detected: '{m1}' and '{m2}'"

    # Check multiple clauses separated by 'then' or commas
    then_count = cam_lower.count(" then ") + cam_lower.count(", then ")
    if then_count > 1 and "hard stop" not in cam_lower:
        return False, f"Too many chained camera movements ({then_count} 'then' transitions). ONE camera move per clip allowed."

    return True, "Valid single camera move"


def build_scene_prompt(
    style_mode: str,
    background: str,
    mg: str,
    fg: str,
    camera_move: str,
    settle: str,
    audio: Optional[str] = None,
    avoid: Optional[str] = None,
    depth_description: Optional[str] = None,
    has_tech_or_ui: bool = False,
    sounds: Optional[List[str]] = None,
) -> str:
    """Build the official 4-part scene prompt using exact company specifications:

    STYLE BLOCK + SHOT + AUDIO + AVOID

    Enforces:
    - Verbatim company style blocks (Style A Flat Parallax, Style B Deep Diorama, Style C Locked Stage)
    - SHOT containing Background, MG, FG, Camera, Settle
    - Explicit depth relationships across 3 planes
    - Exactly ONE committed camera move
    - Sound design only (no music/narration in visual prompt)
    - Targeted AVOID block
    """
    valid_cam, msg = validate_camera_move(camera_move)
    if not valid_cam:
        raise ValueError(f"Invalid camera move for scene: {msg}")

    # 1. Style Block
    style_norm = style_mode.lower().replace("-", "_").replace(" ", "_")
    if "deep" in style_norm:
        style_text = get_deep_diorama_style()
    elif "locked" in style_norm:
        style_text = get_locked_stage_style()
    else:
        style_text = get_flat_parallax_style()

    # 2. Shot Block
    shot_text = build_shot_prompt(
        background=background,
        mg=mg,
        fg=fg,
        camera=camera_move,
        settle=settle,
        depth_description=depth_description or "at three distinct physical depths",
    )

    # 3. Audio Block
    if audio and "AUDIO:" in audio:
        audio_text = audio.strip()
    else:
        audio_text = build_audio_prompt(camera_move=camera_move, sounds=sounds)

    # 4. Avoid Block
    if avoid and "AVOID:" in avoid:
        avoid_text = avoid.strip()
    else:
        avoid_text = build_avoid_prompt(style_type=style_mode, has_tech_or_ui=has_tech_or_ui)

    prompt_parts = [
        "============================================================",
        "STYLE BLOCK",
        "============================================================",
        style_text,
        "",
        "============================================================",
        "SHOT",
        "============================================================",
        shot_text,
        "",
        "============================================================",
        "AUDIO",
        "============================================================",
        audio_text,
        "",
        "============================================================",
        "AVOID",
        "============================================================",
        avoid_text,
    ]
    return "\n".join(prompt_parts)



class StylePromptSystem:
    """Reusable Object-Oriented wrapper for the Company Style Prompt System."""

    def __init__(self):
        self.style_a = COMPANY_STYLE_BLOCK_A_FLAT_PARALLAX
        self.style_b = COMPANY_STYLE_BLOCK_B_DEEP_DIORAMA
        self.style_c = COMPANY_STYLE_BLOCK_C_LOCKED_STAGE
        self.allowed_camera_moves = ALLOWED_CAMERA_MOVES

    def get_style(self, style_name: str) -> str:
        name = style_name.lower().replace("-", "_").replace(" ", "_")
        if "deep" in name:
            return get_deep_diorama_style()
        elif "locked" in name:
            return get_locked_stage_style()
        return get_flat_parallax_style()

    def build_prompt(
        self,
        style_type: str,
        shot_params: Dict[str, Any],
        sounds: Optional[List[str]] = None,
        has_tech_or_ui: bool = False,
    ) -> str:
        return build_complete_generation_prompt(
            style_type=style_type,
            shot_params=shot_params,
            sounds=sounds,
            has_tech_or_ui=has_tech_or_ui,
        )
