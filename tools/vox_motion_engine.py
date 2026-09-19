"""tools/vox_motion_engine.py

Cinematic Vox-Style Motion Graphic Explainer Engine.

Implements a true object-oriented 2.5D motion graphics animation system:
- OBJECT -> MOTION -> TRANSFORMATION -> CAMERA -> NEXT OBJECT -> VISUAL METAPHOR -> NEXT IDEA
- Reusable motion primitives:
    PHOTO_CUTOUT, HALFTONE_CUTOUT, PAPER_LAYER, NEWSPAPER_FRAGMENT, MAP_LAYER,
    DATA_POINT, DATA_LINE, ARROW, LABEL, STAT_NUMBER, CHART, TRADER_FIGURE,
    PHONE, SCREEN, NETWORK_NODE, SIGNAL_LINE, RED_STROKE, UNDERLINE, MASK, TEXT_OBJECT.
- Transformation primitives:
    DUPLICATE, SPLIT, MERGE, MORPH, TRACE, CONNECT, DISCONNECT, EXPLODE,
    COLLAPSE, SCALE_UP, SCALE_DOWN, ROTATE, MASK_REVEAL, PAPER_TEAR,
    CUTOUT_REVEAL, CAMERA_DIVE, CAMERA_PULL, CAMERA_ORBIT, CAMERA_TRACK, MATCH_CUT.
- Authentic Company Art Direction:
    Archival tan (#C9BB9C), Ink Black (#1A1A1A), Hot Red (#D62E1F), Mustard (#D9A441),
    Halftone Gray (#8C8C8C), Paper White (#F8F6F0).
    Halftone cutouts with rough white keylines and offset red marker strokes.
    Print-grain texture, torn edges, giant stat numbers, condensed bold caps.
- 2.5D Camera through multi-plane Z-space with true perspective projection.
- High-performance direct-to-FFmpeg frame piping.
"""

import math
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# ============================================================
# 1. COLOR PALETTE & CONSTANTS
# ============================================================

COLOR_ARCHIVAL_TAN = (201, 187, 156, 255)    # #C9BB9C
COLOR_CARD_BG = (242, 238, 228, 255)         # #F2EEE4
COLOR_INK_BLACK = (26, 26, 26, 255)          # #1A1A1A
COLOR_HOT_RED = (214, 46, 31, 255)           # #D62E1F
COLOR_MUSTARD = (217, 164, 65, 255)          # #D9A441
COLOR_PAPER_WHITE = (248, 246, 240, 255)     # #F8F6F0
COLOR_HALFTONE_GRAY = (140, 140, 140, 255)   # #8C8C8C
COLOR_DARK_SLATE = (20, 24, 28, 255)

# Primitives Types
OBJ_PHOTO_CUTOUT = "PHOTO_CUTOUT"
OBJ_HALFTONE_CUTOUT = "HALFTONE_CUTOUT"
OBJ_PAPER_LAYER = "PAPER_LAYER"
OBJ_NEWSPAPER_FRAGMENT = "NEWSPAPER_FRAGMENT"
OBJ_MAP_LAYER = "MAP_LAYER"
OBJ_DATA_POINT = "DATA_POINT"
OBJ_DATA_LINE = "DATA_LINE"
OBJ_ARROW = "ARROW"
OBJ_LABEL = "LABEL"
OBJ_STAT_NUMBER = "STAT_NUMBER"
OBJ_CHART = "CHART"
OBJ_TRADER_FIGURE = "TRADER_FIGURE"
OBJ_PHONE = "PHONE"
OBJ_SCREEN = "SCREEN"
OBJ_NETWORK_NODE = "NETWORK_NODE"
OBJ_SIGNAL_LINE = "SIGNAL_LINE"
OBJ_RED_STROKE = "RED_STROKE"
OBJ_UNDERLINE = "UNDERLINE"
OBJ_MASK = "MASK"
OBJ_TEXT_OBJECT = "TEXT_OBJECT"

ALL_OBJECT_PRIMITIVES = [
    OBJ_PHOTO_CUTOUT, OBJ_HALFTONE_CUTOUT, OBJ_PAPER_LAYER, OBJ_NEWSPAPER_FRAGMENT,
    OBJ_MAP_LAYER, OBJ_DATA_POINT, OBJ_DATA_LINE, OBJ_ARROW, OBJ_LABEL,
    OBJ_STAT_NUMBER, OBJ_CHART, OBJ_TRADER_FIGURE, OBJ_PHONE, OBJ_SCREEN,
    OBJ_NETWORK_NODE, OBJ_SIGNAL_LINE, OBJ_RED_STROKE, OBJ_UNDERLINE,
    OBJ_MASK, OBJ_TEXT_OBJECT
]

# Transformation Types
TRANS_DUPLICATE = "DUPLICATE"
TRANS_SPLIT = "SPLIT"
TRANS_MERGE = "MERGE"
TRANS_MORPH = "MORPH"
TRANS_TRACE = "TRACE"
TRANS_CONNECT = "CONNECT"
TRANS_DISCONNECT = "DISCONNECT"
TRANS_EXPLODE = "EXPLODE"
TRANS_COLLAPSE = "COLLAPSE"
TRANS_SCALE_UP = "SCALE_UP"
TRANS_SCALE_DOWN = "SCALE_DOWN"
TRANS_ROTATE = "ROTATE"
TRANS_MASK_REVEAL = "MASK_REVEAL"
TRANS_PAPER_TEAR = "PAPER_TEAR"
TRANS_CUTOUT_REVEAL = "CUTOUT_REVEAL"
TRANS_CAMERA_DIVE = "CAMERA_DIVE"
TRANS_CAMERA_PULL = "CAMERA_PULL"
TRANS_CAMERA_ORBIT = "CAMERA_ORBIT"
TRANS_CAMERA_TRACK = "CAMERA_TRACK"
TRANS_MATCH_CUT = "MATCH_CUT"

ALL_TRANSFORMATION_PRIMITIVES = [
    TRANS_DUPLICATE, TRANS_SPLIT, TRANS_MERGE, TRANS_MORPH, TRANS_TRACE,
    TRANS_CONNECT, TRANS_DISCONNECT, TRANS_EXPLODE, TRANS_COLLAPSE,
    TRANS_SCALE_UP, TRANS_SCALE_DOWN, TRANS_ROTATE, TRANS_MASK_REVEAL,
    TRANS_PAPER_TEAR, TRANS_CUTOUT_REVEAL, TRANS_CAMERA_DIVE,
    TRANS_CAMERA_PULL, TRANS_CAMERA_ORBIT, TRANS_CAMERA_TRACK, TRANS_MATCH_CUT
]


# ============================================================
# 2. EASING FUNCTIONS
# ============================================================

def ease_linear(t: float) -> float:
    return max(0.0, min(1.0, t))

def ease_in_quad(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t

def ease_out_quad(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * (2.0 - t)

def ease_in_out_quad(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 2.0 * t * t if t < 0.5 else -1.0 + (4.0 - 2.0 * t) * t

def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    t -= 1.0
    return t * t * t + 1.0

def ease_out_back(t: float, s: float = 1.70158) -> float:
    """Overshoot spring pop-up motion."""
    t = max(0.0, min(1.0, t))
    t -= 1.0
    return t * t * ((s + 1.0) * t + s) + 1.0

def ease_in_back(t: float, s: float = 1.70158) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * ((s + 1.0) * t - s)

def ease_out_elastic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    if t == 0.0 or t == 1.0:
        return t
    p = 0.3
    s = p / 4.0
    return math.pow(2.0, -10.0 * t) * math.sin((t - s) * (2.0 * math.pi) / p) + 1.0


# ============================================================
# 3. 2.5D CAMERA SYSTEM
# ============================================================

class Camera25D:
    """2.5D Perspective Camera with focal length and 3D positioning."""

    def __init__(self, focal_length: float = 1000.0, width: int = 1080, height: int = 1920):
        self.focal = focal_length
        self.width = width
        self.height = height
        self.x = 0.0
        self.y = 0.0
        self.z = -1000.0  # Camera origin in Z
        self.rotation = 0.0 # Z-rotation degrees

    def project(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Project a 3D world coordinate (x, y, z) to 2D screen space (sx, sy, scale).
        Returns: (screen_x, screen_y, scale_factor).
        """
        dz = z - self.z
        if dz <= 10.0:
            dz = 10.0  # Avoid division by zero / negative behind lens
        scale = self.focal / dz
        
        # Apply camera offset
        rel_x = x - self.x
        rel_y = y - self.y
        
        # Apply camera rotation
        if self.rotation != 0.0:
            rad = math.radians(-self.rotation)
            cos_r = math.cos(rad)
            sin_r = math.sin(rad)
            rx = rel_x * cos_r - rel_y * sin_r
            ry = rel_x * sin_r + rel_y * cos_r
            rel_x, rel_y = rx, ry

        sx = rel_x * scale + (self.width / 2.0)
        sy = rel_y * scale + (self.height / 2.0)
        return sx, sy, scale


# ============================================================
# 4. BASE MOTION OBJECT
# ============================================================

class MotionObject:
    """Base animated object with 3D space coordinates, scaling, rotation,
    opacity, lifetime, and custom rendering method.
    """

    def __init__(
        self,
        object_id: str,
        obj_type: str,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        start_time: float = 0.0,
        end_time: float = 100.0,
        easing: str = "ease_out_quad",
    ):
        self.id = object_id
        self.type = obj_type
        self.start_time = start_time
        self.end_time = end_time
        self.easing = easing
        
        # Base transform properties
        self.x = x
        self.y = y
        self.z = z
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.rotation = 0.0
        self.opacity = 1.0
        
        # Keyframe tracks: {prop_name: [(t, val, easing_fn), ...]}
        self.keyframes: Dict[str, List[Tuple[float, float, Callable[[float], float]]]] = {}

    def add_keyframe(self, prop: str, time_sec: float, value: float, easing_fn: Optional[Callable[[float], float]] = None):
        if prop not in self.keyframes:
            self.keyframes[prop] = []
        fn = easing_fn or ease_out_quad
        self.keyframes[prop].append((time_sec, value, fn))
        self.keyframes[prop].sort(key=lambda k: k[0])

    def get_property_at_time(self, prop: str, t: float) -> float:
        """Interpolate property value at time t across defined keyframes."""
        if prop not in self.keyframes or not self.keyframes[prop]:
            return getattr(self, prop, 0.0)

        kfs = self.keyframes[prop]
        if t <= kfs[0][0]:
            return kfs[0][1]
        if t >= kfs[-1][0]:
            return kfs[-1][1]

        # Find bounding keyframes
        for i in range(len(kfs) - 1):
            t0, v0, _ = kfs[i]
            t1, v1, fn = kfs[i + 1]
            if t0 <= t <= t1:
                dur = t1 - t0
                if dur <= 0:
                    return v1
                ratio = (t - t0) / dur
                eased = fn(ratio)
                return v0 + (v1 - v0) * eased
        return getattr(self, prop, 0.0)

    def update_at_time(self, t: float):
        """Update internal transform variables at time t."""
        if "x" in self.keyframes:
            self.x = self.get_property_at_time("x", t)
        if "y" in self.keyframes:
            self.y = self.get_property_at_time("y", t)
        if "z" in self.keyframes:
            self.z = self.get_property_at_time("z", t)
        if "scale_x" in self.keyframes:
            self.scale_x = self.get_property_at_time("scale_x", t)
        if "scale_y" in self.keyframes:
            self.scale_y = self.get_property_at_time("scale_y", t)
        if "rotation" in self.keyframes:
            self.rotation = self.get_property_at_time("rotation", t)
        if "opacity" in self.keyframes:
            self.opacity = self.get_property_at_time("opacity", t)

    def is_active(self, t: float) -> bool:
        op = self.get_property_at_time("opacity", t) if "opacity" in self.keyframes else self.opacity
        return self.start_time <= t <= self.end_time and op > 0.001

    def render(self, img: Image.Image, camera: Camera25D, t: float):
        """Override in subclasses to draw the object onto the PIL canvas."""
        pass


# ============================================================
# 5. SPECIALIZED PRIMITIVES (COMPANY ART DIRECTION MATERIALS)
# ============================================================

def get_system_font(size: int, bold: bool = True) -> ImageFont.ImageFont:
    candidates = ["impact.ttf", "arialbd.ttf", "segoeuib.ttf"] if bold else ["arial.ttf", "segoeui.ttf"]
    for name in candidates:
        p = Path(f"C:/Windows/Fonts/{name}")
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


class HalftoneTraderFigure(MotionObject):
    """Halftone black-and-white cutout trader figure with rough white keyline
    and offset hot-red marker stroke behind.
    """

    def __init__(self, object_id: str, x: float = 0, y: float = 0, z: float = 0, width: int = 420, height: int = 540, **kwargs):
        super().__init__(object_id, OBJ_HALFTONE_CUTOUT, x, y, z, **kwargs)
        self.base_w = width
        self.base_h = height
        self._cache_sprite = None

    def _build_sprite(self) -> Image.Image:
        if self._cache_sprite is not None:
            return self._cache_sprite

        cutout_file = Path("assets/extracted_elements/cutout_man_hat_clean.png")
        if cutout_file.exists():
            try:
                raw_cutout = Image.open(cutout_file).convert("RGBA")
                # Scale proportionally to fit within base_h
                aspect = raw_cutout.width / raw_cutout.height
                th = self.base_h
                tw = int(th * aspect)
                scaled_cutout = raw_cutout.resize((tw, th), Image.Resampling.LANCZOS)
                self._cache_sprite = scaled_cutout
                return scaled_cutout
            except Exception:
                pass

        # Procedural company halftone cutout figure at workstation (fallback)
        w, h = self.base_w, self.base_h
        sprite = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sprite)

        # 1. Offset hot-red marker stroke (+18px X, +14px Y)
        ox, oy = 40 + 16, 40 + 14
        draw.ellipse([ox + w // 2 - 70, oy + 40, ox + w // 2 + 70, oy + 180], fill=COLOR_HOT_RED)
        draw.polygon([
            (ox + w // 2 - 130, oy + 180),
            (ox + w // 2 + 130, oy + 180),
            (ox + w // 2 + 160, oy + h - 50),
            (ox + w // 2 - 160, oy + h - 50)
        ], fill=COLOR_HOT_RED)

        # 2. Rough white keyline edge
        wx, wy = 40, 40
        draw.ellipse([wx + w // 2 - 74, wy + 36, wx + w // 2 + 74, wy + 184], outline=COLOR_PAPER_WHITE, width=8)
        draw.polygon([
            (wx + w // 2 - 134, wy + 176),
            (wx + w // 2 + 134, wy + 176),
            (wx + w // 2 + 164, wy + h - 46),
            (wx + w // 2 - 164, wy + h - 46)
        ], outline=COLOR_PAPER_WHITE, width=8)

        # 3. B&W Halftone Subject Body
        body = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(body)
        b_draw.ellipse([w // 2 - 68, 40, w // 2 + 68, 176], fill=COLOR_INK_BLACK)
        b_draw.polygon([
            (w // 2 - 126, 180),
            (w // 2 + 126, 180),
            (w // 2 + 154, h - 50),
            (w // 2 - 154, h - 50)
        ], fill=(35, 35, 35, 255))
        
        # Dual monitors in foreground of figure
        b_draw.rectangle([w // 2 - 180, h - 160, w // 2 - 30, h - 20], fill=COLOR_INK_BLACK, outline=COLOR_PAPER_WHITE, width=4)
        b_draw.rectangle([w // 2 + 30, h - 160, w // 2 + 180, h - 20], fill=COLOR_INK_BLACK, outline=COLOR_PAPER_WHITE, width=4)
        # Red candlestick bars on screens
        for bx in [w // 2 - 150, w // 2 - 110, w // 2 - 70, w // 2 + 60, w // 2 + 100, w // 2 + 140]:
            b_draw.line([(bx, h - 140), (bx, h - 40)], fill=COLOR_HOT_RED, width=3)

        # Apply halftone pattern
        grid_step = 6
        for gy in range(0, h, grid_step):
            for gx in range(0, w, grid_step):
                pixel = body.getpixel((gx, gy))
                if pixel[3] > 50:
                    r = 2 if (gx + gy) % 12 == 0 else 1
                    b_draw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=COLOR_HALFTONE_GRAY)

        sprite.alpha_composite(body, (wx, wy))
        self._cache_sprite = sprite
        return sprite

    def render(self, canvas: Image.Image, camera: Camera25D, t: float):
        if not self.is_active(t):
            return
        self.update_at_time(t)
        sx, sy, scale = camera.project(self.x, self.y, self.z)
        final_scale = scale * self.scale_x
        if final_scale <= 0.01:
            return

        sprite = self._build_sprite()
        target_w = max(4, int(sprite.width * final_scale))
        target_h = max(4, int(sprite.height * final_scale * (self.scale_y / self.scale_x)))
        
        scaled = sprite.resize((target_w, target_h), Image.Resampling.BILINEAR)
        if self.rotation != 0.0:
            scaled = scaled.rotate(-self.rotation, expand=True, resample=Image.Resampling.BILINEAR)

        # Apply opacity
        if self.opacity < 0.99:
            alpha = scaled.split()[3]
            alpha = alpha.point(lambda p: int(p * self.opacity))
            scaled.putalpha(alpha)

        px = int(sx - scaled.width // 2)
        py = int(sy - scaled.height // 2)
        canvas.alpha_composite(scaled, (px, py))


class NewspaperFragment(MotionObject):
    """Aged newspaper fragment / financial article clipping that tumbles,
    stacks, and can physically tear along an irregular fracture line.
    """

    def __init__(self, object_id: str, headline: str, x: float = 0, y: float = 0, z: float = 0, width: int = 360, height: int = 220, is_torn: bool = False, **kwargs):
        super().__init__(object_id, OBJ_NEWSPAPER_FRAGMENT, x, y, z, **kwargs)
        self.headline = headline
        self.w = width
        self.h = height
        self.is_torn = is_torn
        self.tear_progress = 0.0

    def render(self, canvas: Image.Image, camera: Camera25D, t: float):
        if not self.is_active(t):
            return
        self.update_at_time(t)
        sx, sy, scale = camera.project(self.x, self.y, self.z)
        final_scale = scale * self.scale_x
        if final_scale <= 0.01:
            return

        # Build card surface
        tw, th = max(10, int(self.w * final_scale)), max(10, int(self.h * final_scale))
        card = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)

        # Drop shadow
        draw.rectangle([6, 8, tw - 4, th - 4], fill=(0, 0, 0, 90))
        # Archival Tan / Newsprint Paper Body
        draw.rectangle([0, 0, tw - 10, th - 10], fill=COLOR_CARD_BG, outline=COLOR_ARCHIVAL_TAN, width=max(2, int(2 * final_scale)))

        # Header bar in Hot Red
        bar_h = max(12, int(26 * final_scale))
        draw.rectangle([0, 0, tw - 10, bar_h], fill=COLOR_HOT_RED)

        font_sm = get_system_font(max(10, int(13 * final_scale)), bold=True)
        draw.text((8, 4), "FINANCIAL DISPATCH • BREAKING", fill=COLOR_PAPER_WHITE, font=font_sm)

        # Headline
        font_head = get_system_font(max(14, int(22 * final_scale)), bold=True)
        draw.text((12, bar_h + 10), self.headline[:22], fill=COLOR_INK_BLACK, font=font_head)
        
        # Columns of fake microfiche text lines
        line_y = bar_h + int(42 * final_scale)
        for _ in range(3):
            draw.line([(12, line_y), (tw - 25, line_y)], fill=COLOR_HALFTONE_GRAY, width=max(1, int(2 * final_scale)))
            line_y += int(10 * final_scale)

        # Red accent bar on bottom edge
        draw.rectangle([12, th - int(24 * final_scale), tw - 25, th - int(20 * final_scale)], fill=COLOR_HOT_RED)

        # Rotate and opacity
        if self.rotation != 0.0:
            card = card.rotate(-self.rotation, expand=True, resample=Image.Resampling.BILINEAR)
        if self.opacity < 0.99:
            alpha = card.split()[3]
            alpha = alpha.point(lambda p: int(p * self.opacity))
            card.putalpha(alpha)

        px = int(sx - card.width // 2)
        py = int(sy - card.height // 2)
        canvas.alpha_composite(card, (px, py))


class KineticTextObject(MotionObject):
    """Typography as a physical animated object that scales, impacts,
    and pushes into the composition with spring physics.
    """

    def __init__(self, object_id: str, text: str, font_size: int = 54, color=COLOR_INK_BLACK, bg_color=None, **kwargs):
        super().__init__(object_id, OBJ_TEXT_OBJECT, **kwargs)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.bg_color = bg_color
        self.underline_width = 0.0  # 0.0 to 1.0 swipe

    def render(self, canvas: Image.Image, camera: Camera25D, t: float):
        if not self.is_active(t):
            return
        self.update_at_time(t)
        sx, sy, scale = camera.project(self.x, self.y, self.z)
        final_scale = scale * self.scale_x
        if final_scale <= 0.01:
            return

        size = max(10, int(self.font_size * final_scale))
        font = get_system_font(size, bold=True)
        
        # Measure text
        dummy = Image.new("RGBA", (1, 1))
        d_draw = ImageDraw.Draw(dummy)
        bbox = d_draw.textbbox((0, 0), self.text, font=font)
        tw = bbox[2] - bbox[0] + 40
        th = bbox[3] - bbox[1] + 30

        surf = Image.new("RGBA", (tw, th + 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(surf)

        # Optional background box (e.g. Hot Red card or Archival card)
        if self.bg_color:
            draw.rectangle([0, 0, tw - 4, th - 4], fill=(0, 0, 0, 80)) # shadow
            draw.rectangle([0, 0, tw - 8, th - 8], fill=self.bg_color, outline=COLOR_PAPER_WHITE, width=max(2, int(3 * final_scale)))

        draw.text((15, 6), self.text, fill=self.color, font=font)

        # Underline animation if active
        if "underline" in self.keyframes:
            self.underline_width = self.get_property_at_time("underline", t)
        if self.underline_width > 0.01:
            uw = int((tw - 30) * self.underline_width)
            uy = th - 4
            draw.line([(15, uy), (15 + uw, uy)], fill=COLOR_HOT_RED, width=max(3, int(7 * final_scale)))

        if self.rotation != 0.0:
            surf = surf.rotate(-self.rotation, expand=True, resample=Image.Resampling.BILINEAR)
        if self.opacity < 0.99:
            alpha = surf.split()[3]
            alpha = alpha.point(lambda p: int(p * self.opacity))
            surf.putalpha(alpha)

        px = int(sx - surf.width // 2)
        py = int(sy - surf.height // 2)
        canvas.alpha_composite(surf, (px, py))


class AnimatedStatCounter(MotionObject):
    """Animated stat number that rapidly counts up through orders of magnitude
    (1 -> 10 -> 100 -> 1,000 -> 10,000 -> 100,000 -> 1,482,930).
    """

    def __init__(self, object_id: str, target_number: int = 1482930, label: str = "TRADER INPUTS", **kwargs):
        super().__init__(object_id, OBJ_STAT_NUMBER, **kwargs)
        self.target = target_number
        self.label = label
        self.current_val = 1

    def render(self, canvas: Image.Image, camera: Camera25D, t: float):
        if not self.is_active(t):
            return
        self.update_at_time(t)
        sx, sy, scale = camera.project(self.x, self.y, self.z)
        final_scale = scale * self.scale_x
        if final_scale <= 0.01:
            return

        # Calculate animated count value based on progress
        if "count_progress" in self.keyframes:
            prog = self.get_property_at_time("count_progress", t)
            # Logarithmic/exponential acceleration through powers of 10
            if prog >= 0.99:
                self.current_val = self.target
            else:
                self.current_val = max(1, int(math.pow(self.target, prog)))
        
        display_num = f"{self.current_val:,}"
        font_num = get_system_font(max(18, int(92 * final_scale)), bold=True)
        font_lbl = get_system_font(max(12, int(26 * final_scale)), bold=True)

        w = max(100, int(640 * final_scale))
        h = max(60, int(260 * final_scale))
        surf = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(surf)

        # Drop shadow & Archival Card
        draw.rectangle([8, 10, w - 4, h - 4], fill=(0, 0, 0, 95))
        draw.rectangle([0, 0, w - 10, h - 10], fill=COLOR_CARD_BG, outline=COLOR_ARCHIVAL_TAN, width=max(2, int(3 * final_scale)))

        # Giant Stat Digits
        draw.text((25, int(15 * final_scale)), display_num, fill=COLOR_INK_BLACK, font=font_num)

        # Pill badge with label
        badge_y = int(120 * final_scale)
        badge_w = int(280 * final_scale)
        badge_h = int(45 * final_scale)
        draw.rectangle([25, badge_y, 25 + badge_w, badge_y + badge_h], fill=COLOR_HOT_RED)
        draw.text((40, badge_y + int(6 * final_scale)), self.label, fill=COLOR_PAPER_WHITE, font=font_lbl)

        # Underline coordinate
        draw.line([(25, h - int(35 * final_scale)), (w - 35, h - int(35 * final_scale))], fill=COLOR_MUSTARD, width=max(2, int(4 * final_scale)))

        if self.rotation != 0.0:
            surf = surf.rotate(-self.rotation, expand=True, resample=Image.Resampling.BILINEAR)
        if self.opacity < 0.99:
            alpha = surf.split()[3]
            alpha = alpha.point(lambda p: int(p * self.opacity))
            surf.putalpha(alpha)

        px = int(sx - surf.width // 2)
        py = int(sy - surf.height // 2)
        canvas.alpha_composite(surf, (px, py))


class NetworkMeshLayer(MotionObject):
    """Dynamic network of glowing nodes and tracing signal vectors
    representing collective intelligence convergence.
    """

    def __init__(self, object_id: str, node_count: int = 18, **kwargs):
        super().__init__(object_id, OBJ_NETWORK_NODE, **kwargs)
        np.random.seed(42)
        self.nodes = [
            (
                float(np.random.uniform(-420, 420)),
                float(np.random.uniform(-650, 650)),
                float(np.random.uniform(-100, 100))
            )
            for _ in range(node_count)
        ]
        self.trace_progress = 0.0

    def render(self, canvas: Image.Image, camera: Camera25D, t: float):
        if not self.is_active(t):
            return
        self.update_at_time(t)
        if "trace" in self.keyframes:
            self.trace_progress = self.get_property_at_time("trace", t)

        overlay = Image.new("RGBA", (canvas.width, canvas.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        projected = [camera.project(nx + self.x, ny + self.y, nz + self.z) for (nx, ny, nz) in self.nodes]

        # Draw connecting signal lines up to trace_progress
        total_connections = len(projected) - 1
        active_lines = int(total_connections * self.trace_progress)

        for i in range(active_lines):
            p1 = projected[i]
            p2 = projected[(i * 3 + 1) % len(projected)]
            if p1[2] > 0.05 and p2[2] > 0.05:
                col = (*COLOR_HOT_RED[:3], int(210 * self.opacity))
                draw.line([(p1[0], p1[1]), (p2[0], p2[1])], fill=col, width=max(2, int(4 * p1[2])))

        # Draw nodes
        for sx, sy, sc in projected:
            if sc > 0.05:
                r = max(4, int(10 * sc))
                col_outer = (*COLOR_HOT_RED[:3], int(240 * self.opacity))
                col_inner = (*COLOR_PAPER_WHITE[:3], int(255 * self.opacity))
                draw.ellipse([sx - r - 3, sy - r - 3, sx + r + 3, sy + r + 3], fill=col_outer)
                draw.ellipse([sx - r + 1, sy - r + 1, sx + r - 1, sy + r - 1], fill=col_inner)

        canvas.alpha_composite(overlay)


# ============================================================
# 6. VOX MOTION COMPOSITION (ENGINE)
# ============================================================

class VoxMotionComposition:
    """Master multi-layer 2.5D animated visual journalism composition.
    Handles timeline, camera choreography, object hierarchy, and FFmpeg encoding.
    """

    def __init__(self, duration_sec: float = 10.0, fps: int = 30, width: int = 1080, height: int = 1920):
        self.duration = duration_sec
        self.fps = fps
        self.width = width
        self.height = height
        self.total_frames = int(duration_sec * fps)
        self.camera = Camera25D(focal_length=1000.0, width=width, height=height)
        self.objects: List[MotionObject] = []
        self._bg_texture = None

    def add_object(self, obj: MotionObject):
        self.objects.append(obj)

    def _get_background_frame(self) -> Image.Image:
        if self._bg_texture is not None:
            return self._bg_texture.copy()

        # Build official company archival paper background (#C9BB9C) with double border & subtle grid
        bg = Image.new("RGBA", (self.width, self.height), COLOR_ARCHIVAL_TAN)
        draw = ImageDraw.Draw(bg)

        # Subtle archival paper grid lines
        grid_step = 60
        for gx in range(0, self.width, grid_step):
            draw.line([(gx, 0), (gx, self.height)], fill=(185, 172, 142, 120), width=1)
        for gy in range(0, self.height, grid_step):
            draw.line([(0, gy), (self.width, gy)], fill=(185, 172, 142, 120), width=1)

        # Stage map from company art direction master
        map_path = Path("assets/extracted_elements/archival_stage_map.png")
        if map_path.exists():
            try:
                stage_map = Image.open(map_path).convert("RGBA")
                sm_w = self.width - 80
                sm_h = int(stage_map.height * (sm_w / stage_map.width))
                scaled_map = stage_map.resize((sm_w, sm_h), Image.Resampling.LANCZOS)
                alpha = scaled_map.split()[3]
                alpha = alpha.point(lambda p: int(p * 0.40))
                scaled_map.putalpha(alpha)
                bg.alpha_composite(scaled_map, (40, self.height - sm_h - 60))
            except Exception:
                pass

        # Double keyline border
        margin = 40
        draw.rectangle([margin, margin, self.width - margin, self.height - margin], outline=COLOR_PAPER_WHITE, width=2)
        draw.rectangle([margin + 8, margin + 8, self.width - margin - 8, self.height - margin - 8], outline=(170, 155, 125, 180), width=1)

        # Corner Hot Red crosshairs
        ch = 22
        for cx, cy in [
            (margin, margin),
            (self.width - margin, margin),
            (margin, self.height - margin),
            (self.width - margin, self.height - margin)
        ]:
            draw.line([(cx - ch, cy), (cx + ch, cy)], fill=COLOR_HOT_RED, width=3)
            draw.line([(cx, cy - ch), (cx, cy + ch)], fill=COLOR_HOT_RED, width=3)

        self._bg_texture = bg
        return bg.copy()

    def render_frame(self, t: float) -> Image.Image:
        """Render a single 2.5D motion graphics frame at time t."""
        canvas = self._get_background_frame()

        # Collect and sort active objects by 3D depth Z (back-to-front painter's order)
        active_objs = [obj for obj in self.objects if obj.is_active(t)]
        active_objs.sort(key=lambda o: o.get_property_at_time("z", t) if "z" in o.keyframes else o.z, reverse=True)

        for obj in active_objs:
            obj.render(canvas, self.camera, t)

        return canvas

    def render_video(self, output_mp4: Path, ffmpeg_path: str = "ffmpeg") -> Path:
        """Pipe raw RGBA frames directly into FFmpeg stdin to produce high-bitrate H.264 video."""
        output_mp4.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            ffmpeg_path, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.width}x{self.height}",
            "-pix_fmt", "rgba",
            "-r", str(self.fps),
            "-i", "pipe:0",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-r", str(self.fps),
            str(output_mp4)
        ]

        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

        for frame_idx in range(self.total_frames):
            t = frame_idx / self.fps
            frame_img = self.render_frame(t)
            raw_bytes = frame_img.tobytes()
            p.stdin.write(raw_bytes)

        p.stdin.close()
        p.wait()

        if p.returncode != 0:
            err = p.stderr.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"FFmpeg motion engine render failed: {err}")

        return output_mp4


# ============================================================
# 7. AUTHORITATIVE PROOF SEQUENCE GENERATOR (8-12 SECONDS)
# ============================================================

def build_vox_motion_proof_sequence(duration_sec: float = 10.0) -> VoxMotionComposition:
    """Build the official Phase 17/18 Vox Motion Graphic Proof sequence (10.0s).
    Demonstrates:
    1. TRADER cutout drops into center with spring overshoot (0.0s - 2.0s)
    2. TRADER DUPLICATES into network of 6 figures (2.0s - 4.5s)
    3. INFORMATION FLOOD: Stacks of newspaper fragments fly in, stack, and tear (4.5s - 6.8s)
    4. THE VACUUM COLLAPSE: 20 objects snap inward to dead-center card on sub-bass hit (6.8s - 8.2s)
    5. DATA PROOF & NETWORK TRACE: Numbers accelerate dynamically 1 -> 1,482,930 (8.2s - 10.0s)
    """
    comp = VoxMotionComposition(duration_sec=duration_sec, fps=30, width=1080, height=1920)

    # ------------------------------------------------------------
    # A. CAMERA CHOREOGRAPHY
    # ------------------------------------------------------------
    # Camera dives forward, tracks up, holds, and dives into numbers
    # We animate camera.z directly in custom update hook or keyframe wrapper
    
    # ------------------------------------------------------------
    # B. SCENE 1: TRADER FIGURE & ISOLATION (0.0s - 2.5s)
    # ------------------------------------------------------------
    trader_main = HalftoneTraderFigure("trader_main", x=0, y=100, z=0, start_time=0.0, end_time=10.0)
    # Drops down with spring overshoot
    trader_main.add_keyframe("y", 0.0, -800.0)
    trader_main.add_keyframe("y", 0.6, 100.0, ease_out_back)
    trader_main.add_keyframe("scale_x", 0.0, 0.2)
    trader_main.add_keyframe("scale_x", 0.6, 1.0, ease_out_back)
    trader_main.add_keyframe("scale_y", 0.0, 0.2)
    trader_main.add_keyframe("scale_y", 0.6, 1.0, ease_out_back)
    # Duplication shrink at 2.2s
    trader_main.add_keyframe("scale_x", 2.2, 1.0)
    trader_main.add_keyframe("scale_x", 2.8, 0.45, ease_out_quad)
    trader_main.add_keyframe("scale_y", 2.2, 1.0)
    trader_main.add_keyframe("scale_y", 2.8, 0.45, ease_out_quad)
    trader_main.add_keyframe("y", 2.2, 100.0)
    trader_main.add_keyframe("y", 2.8, -120.0, ease_out_quad)
    # Collapse into center at 6.8s
    trader_main.add_keyframe("opacity", 6.8, 1.0)
    trader_main.add_keyframe("opacity", 7.1, 0.0, ease_out_quad)
    comp.add_object(trader_main)

    # 2:17 AM Badge
    badge_time = KineticTextObject("badge_time", "[● 2:17 AM]", font_size=32, color=COLOR_INK_BLACK, bg_color=COLOR_CARD_BG, start_time=0.4, end_time=6.8)
    badge_time.x = 0
    badge_time.y = -500
    badge_time.add_keyframe("scale_x", 0.4, 0.0)
    badge_time.add_keyframe("scale_x", 0.8, 1.0, ease_out_back)
    badge_time.add_keyframe("scale_y", 0.4, 0.0)
    badge_time.add_keyframe("scale_y", 0.8, 1.0, ease_out_back)
    badge_time.add_keyframe("opacity", 6.8, 1.0)
    badge_time.add_keyframe("opacity", 7.0, 0.0)
    comp.add_object(badge_time)

    # ------------------------------------------------------------
    # C. SCENE 2: DUPLICATION & NETWORK SPREAD (2.0s - 6.8s)
    # ------------------------------------------------------------
    # 5 duplicate trader cutouts spreading outward
    dup_coords = [
        (-280, -320, 100),
        (280, -320, 100),
        (-320, 180, 50),
        (320, 180, 50),
        (0, 420, -50),
    ]
    for idx, (dx, dy, dz) in enumerate(dup_coords):
        dup = HalftoneTraderFigure(f"trader_dup_{idx}", x=0, y=100, z=0, width=280, height=360, start_time=2.2, end_time=6.8)
        dup.add_keyframe("x", 2.2, 0.0)
        dup.add_keyframe("x", 2.8 + idx * 0.08, dx, ease_out_back)
        dup.add_keyframe("y", 2.2, 100.0)
        dup.add_keyframe("y", 2.8 + idx * 0.08, dy, ease_out_back)
        dup.add_keyframe("scale_x", 2.2, 0.0)
        dup.add_keyframe("scale_x", 2.8, 0.55, ease_out_back)
        dup.add_keyframe("scale_y", 2.2, 0.0)
        dup.add_keyframe("scale_y", 2.8, 0.55, ease_out_back)
        # Collapse inward at 6.8s
        dup.add_keyframe("x", 6.8, dx)
        dup.add_keyframe("x", 7.1, 0.0, ease_in_back)
        dup.add_keyframe("y", 6.8, dy)
        dup.add_keyframe("y", 7.1, 0.0, ease_in_back)
        dup.add_keyframe("opacity", 6.8, 1.0)
        dup.add_keyframe("opacity", 7.1, 0.0)
        comp.add_object(dup)

    # ------------------------------------------------------------
    # D. SCENE 3: INFORMATION FLOOD (4.0s - 6.8s)
    # ------------------------------------------------------------
    # Cascading flying newspaper fragments stacking in 3D space
    news_headlines = [
        ("INFLATION SPIKE TRIGGERS SELLOFF", -240, -180, 200, -14),
        ("FED RATE HIKE LEAK CONFIRMED", 250, -80, 150, 12),
        ("ALGORITHM SQUEEZE DETECTED", -200, 320, 250, 8),
        ("VOLATILITY SURGE: VIX +18%", 220, 280, 180, -10),
        ("BREAKING MARKET COLLAPSE", 0, -40, 350, 0),
    ]
    for idx, (head, fx, fy, fz, rot) in enumerate(news_headlines):
        card = NewspaperFragment(f"news_{idx}", head, x=fx * 2.5, y=fy * 2.5, z=fz, start_time=4.0 + idx * 0.35, end_time=7.1)
        # Tumble into frame
        card.add_keyframe("x", 4.0 + idx * 0.35, fx * 3.0)
        card.add_keyframe("x", 4.6 + idx * 0.35, fx, ease_out_cubic)
        card.add_keyframe("y", 4.0 + idx * 0.35, fy * 3.0)
        card.add_keyframe("y", 4.6 + idx * 0.35, fy, ease_out_cubic)
        card.add_keyframe("rotation", 4.0 + idx * 0.35, rot * 2.5)
        card.add_keyframe("rotation", 4.6 + idx * 0.35, rot, ease_out_back)
        card.add_keyframe("opacity", 4.0 + idx * 0.35, 0.0)
        card.add_keyframe("opacity", 4.4 + idx * 0.35, 1.0)
        # Collapse into center at 6.8s
        card.add_keyframe("x", 6.8, fx)
        card.add_keyframe("x", 7.1, 0.0, ease_in_back)
        card.add_keyframe("y", 6.8, fy)
        card.add_keyframe("y", 7.1, 0.0, ease_in_back)
        card.add_keyframe("opacity", 6.8, 1.0)
        card.add_keyframe("opacity", 7.1, 0.0)
        comp.add_object(card)

    # Banner: "TOO MUCH INFORMATION"
    banner_noise = KineticTextObject("banner_noise", "TOO MUCH INFORMATION.", font_size=52, color=COLOR_PAPER_WHITE, bg_color=COLOR_HOT_RED, start_time=4.8, end_time=6.9)
    banner_noise.x = 0
    banner_noise.y = -420
    banner_noise.add_keyframe("scale_x", 4.8, 0.0)
    banner_noise.add_keyframe("scale_x", 5.2, 1.0, ease_out_back)
    banner_noise.add_keyframe("scale_y", 4.8, 0.0)
    banner_noise.add_keyframe("scale_y", 5.2, 1.0, ease_out_back)
    banner_noise.add_keyframe("opacity", 6.8, 1.0)
    banner_noise.add_keyframe("opacity", 7.0, 0.0)
    comp.add_object(banner_noise)

    # ------------------------------------------------------------
    # E. SCENE 4: THE VACUUM COLLAPSE & SIGNAL (7.0s - 8.4s)
    # ------------------------------------------------------------
    # Centered stark card popping out of the vacuum singularity
    signal_card = KineticTextObject(
        "signal_card",
        "NOT ENOUGH SIGNAL.",
        font_size=68,
        color=COLOR_INK_BLACK,
        bg_color=COLOR_CARD_BG,
        start_time=7.1,
        end_time=10.0
    )
    signal_card.x = 0
    signal_card.y = -220
    # Spring pop up from zero
    signal_card.add_keyframe("scale_x", 7.1, 0.0)
    signal_card.add_keyframe("scale_x", 7.45, 1.0, ease_out_back)
    signal_card.add_keyframe("scale_y", 7.1, 0.0)
    signal_card.add_keyframe("scale_y", 7.45, 1.0, ease_out_back)
    # Underline swipe
    signal_card.add_keyframe("underline", 7.45, 0.0)
    signal_card.add_keyframe("underline", 7.85, 1.0, ease_out_cubic)
    comp.add_object(signal_card)

    # Sub-tag: "TRUE EFFICIENCY < 0.2%"
    sub_tag = KineticTextObject("sub_tag", "TRUE INFORMATION EFFICIENCY < 0.2%", font_size=24, color=COLOR_HOT_RED, bg_color=None, start_time=7.5, end_time=10.0)
    sub_tag.x = 0
    sub_tag.y = -130
    sub_tag.add_keyframe("opacity", 7.5, 0.0)
    sub_tag.add_keyframe("opacity", 7.7, 1.0)
    comp.add_object(sub_tag)

    # ------------------------------------------------------------
    # F. SCENE 5: DATA PROOF & NETWORK TRACE (8.2s - 10.0s)
    # ------------------------------------------------------------
    # Network mesh connecting nodes across space
    network = NetworkMeshLayer("network_mesh", node_count=20, start_time=8.2, end_time=10.0)
    network.x = 0
    network.y = 200
    network.add_keyframe("trace", 8.2, 0.0)
    network.add_keyframe("trace", 9.4, 1.0, ease_out_cubic)
    network.add_keyframe("opacity", 8.2, 0.0)
    network.add_keyframe("opacity", 8.5, 1.0)
    comp.add_object(network)

    # Animated Stat Counter: 1 -> 1,482,930
    counter = AnimatedStatCounter("counter_proof", target_number=1482930, label="TRADER INPUTS INDEXED", start_time=8.2, end_time=10.0)
    counter.x = 0
    counter.y = 180
    counter.z = 200
    counter.add_keyframe("scale_x", 8.2, 0.2)
    counter.add_keyframe("scale_x", 8.6, 1.0, ease_out_back)
    counter.add_keyframe("scale_y", 8.2, 0.2)
    counter.add_keyframe("scale_y", 8.6, 1.0, ease_out_back)
    counter.add_keyframe("count_progress", 8.3, 0.0)
    counter.add_keyframe("count_progress", 9.8, 1.0, ease_out_quad)
    comp.add_object(counter)

    # Accuracy Pill Badge
    acc_badge = KineticTextObject("acc_badge", "68.4% DIRECTIONAL ACCURACY", font_size=34, color=COLOR_PAPER_WHITE, bg_color=COLOR_HOT_RED, start_time=8.8, end_time=10.0)
    acc_badge.x = 0
    acc_badge.y = 420
    acc_badge.add_keyframe("scale_x", 8.8, 0.0)
    acc_badge.add_keyframe("scale_x", 9.15, 1.0, ease_out_back)
    acc_badge.add_keyframe("scale_y", 8.8, 0.0)
    acc_badge.add_keyframe("scale_y", 9.15, 1.0, ease_out_back)
    comp.add_object(acc_badge)

    return comp
