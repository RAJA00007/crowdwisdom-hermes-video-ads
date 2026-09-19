"""Phase 9 Editorial Motion Compositor — Official Company Art-Direction Engine.

Implements the authentic Vox-style documentary paper diorama visual system:
Reference: assets/style_reference/company_art_direction.png

Visual Construction Logic:
- Palette: Archival Tan (#C9BB9C), Ink Black (#1A1A1A), Halftone Gray (#8C8C8C), Hot Red (#D62E1F), Mustard (#D9A441)
- Material: Halftone texture + rough off-white cut-paper keyline + offset Hot-Red stroke (+12px) + paper drop shadows
- Surface: Aged archival paper, antique nautical map overlay, fiber grain, matte finish
- Depth Planes: 3-plane physical paper diorama (Background: map/newspaper, Midground: halftone cutouts, Foreground: stat cards/pins/underlines)
- Typography: Impact condensed bold uppercase, Consolas monospace typewriter annotations, giant stat heroes
- Reusable Motion Primitives: PAPER_POP, TICK_UP, UNDERLINE, ALERT_WASH (once in beat 6), THREAD_PULL, STAMP, COUNTER_SLAM

Zero neon, zero glossy 3D, zero generic dashboards, zero AI-hallucinated text.
Compatible with Python 3.10.
"""

import json
import logging
import math
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

from tools.ffmpeg_tool import FFmpegTool

logger = logging.getLogger(__name__)

# Official Company Art-Direction Palette
COLOR_ARCHIVAL_TAN = (201, 187, 156)    # #C9BB9C aged archival paper
COLOR_INK_BLACK = (26, 26, 26)          # #1A1A1A high-contrast ink
COLOR_HALFTONE_GRAY = (140, 140, 140)   # #8C8C8C newspaper dot screen
COLOR_HOT_RED = (214, 46, 31)           # #D62E1F emphasis, strokes, arrows, underlines
COLOR_MUSTARD = (217, 164, 65)          # #D9A441 secondary accent tags (sparing)
COLOR_PAPER_WHITE = (248, 246, 240)     # Cut paper keyline border
COLOR_CARD_BG = (242, 238, 228)         # Clean paper card fill


class EditorialCompositor:
    """Production compositor implementing the company paper-diorama documentary explainer system."""

    def __init__(self, ffmpeg_tool: Optional[FFmpegTool] = None):
        self.ffmpeg = ffmpeg_tool or FFmpegTool()
        self.assets_dir = Path("data/assets")
        self.style_ref_dir = Path("assets/style_reference")

        # Load extracted stage map texture if available
        self.map_texture_path = self.assets_dir / "cinematic" / "stage_map_texture.png"
        self._cached_bg: Optional[Image.Image] = None

    def _get_font(self, size: int, style: str = "headline") -> ImageFont.ImageFont:
        """Load authentic typography: Impact for headlines, Consolas for annotations, Arial for body."""
        candidates = []
        if style == "headline":
            candidates = ["impact.ttf", "arialbd.ttf", "segoeuib.ttf"]
        elif style == "mono":
            candidates = ["consola.ttf", "cour.ttf", "segoeui.ttf"]
        elif style == "bold":
            candidates = ["arialbd.ttf", "segoeuib.ttf"]
        else:
            candidates = ["arial.ttf", "segoeui.ttf"]

        for font_name in candidates:
            win_path = Path(f"C:/Windows/Fonts/{font_name}")
            if win_path.exists():
                try:
                    return ImageFont.truetype(str(win_path), size)
                except Exception:
                    pass
        return ImageFont.load_default()

    def create_archival_paper_canvas(self, width: int = 1080, height: int = 1920, with_map: bool = True) -> Image.Image:
        """Generate archival tan (#C9BB9C) paper canvas with authentic fiber grain and antique map overlay."""
        # 1. Base tan fill
        canvas = Image.new("RGB", (width, height), COLOR_ARCHIVAL_TAN)

        # 2. Add subtle antique map linework if stage map exists
        if with_map and self.map_texture_path.exists():
            try:
                map_img = Image.open(self.map_texture_path).convert("RGBA")
                mw, mh = map_img.size
                # Scale map to span canvas width
                scaled_h = int(mh * (width / float(mw)))
                map_scaled = map_img.resize((width, max(scaled_h, 300)), Image.Resampling.LANCZOS)
                # Tile / paste map with subtle opacity
                map_alpha = map_scaled.split()[-1].point(lambda p: int(p * 0.35))
                canvas.paste(map_scaled.convert("RGB"), (0, height - scaled_h - 100), map_alpha)
                # Paste top flipped map faintly
                canvas.paste(map_scaled.convert("RGB"), (0, 60), map_alpha)
            except Exception as e:
                logger.warning("Could not overlay stage map: %s", e)

        # 3. Add paper fiber noise
        rng = np.random.RandomState(42)
        noise = rng.normal(0, 5, (height, width, 3)).astype(np.int16)
        base_arr = np.array(canvas, dtype=np.int16)
        noisy_arr = np.clip(base_arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(noisy_arr, mode="RGB")

    def make_halftone(self, img_gray: Image.Image, step: int = 7) -> Image.Image:
        """Convert grayscale image to high-contrast newsprint halftone dot screen."""
        gw, gh = img_gray.size
        dots = Image.new("L", (gw, gh), 255)
        d = ImageDraw.Draw(dots)
        arr = np.array(img_gray)
        for y in range(0, gh, step):
            for x in range(0, gw, step):
                val = np.mean(arr[y:min(y + step, gh), x:min(x + step, gw)])
                r = ((255 - val) / 255.0) * (step * 0.72)
                if r > 0.4:
                    cx, cy = x + step // 2, y + step // 2
                    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=0)
        return dots

    def create_halftone_cutout(
        self,
        img_path: Path,
        target_size: Tuple[int, int] = (500, 680),
        crop_box: Optional[Tuple[int, int, int, int]] = None,
        border_radius: int = 40,
    ) -> Image.Image:
        """Create paper diorama cutout: Halftone + Rough White Keyline + Offset Hot Red Stroke + Drop Shadow."""
        tw, th = target_size
        img = Image.open(img_path).convert("RGB")
        w, h = img.size

        if crop_box:
            img = img.crop(crop_box)
        else:
            # Default center upper crop
            img = img.crop((w // 5, h // 8, 4 * w // 5, 7 * h // 8))

        img_scaled = img.resize((tw, th), Image.Resampling.LANCZOS)
        gray = ImageOps.autocontrast(img_scaled.convert("L"))
        halftone_dots = self.make_halftone(gray, step=7)

        # Build padded canvas to hold border and offset strokes
        pad = 60
        CW, CH = tw + pad * 2, th + pad * 2
        ox, oy = pad, pad

        # Silhouette mask
        mask = Image.new("L", (CW, CH), 0)
        d_m = ImageDraw.Draw(mask)
        d_m.rounded_rectangle([ox, oy, ox + tw, oy + th], radius=border_radius, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(6))
        mask = mask.point(lambda p: 255 if p > 120 else 0)

        # 1. White border mask (rough paper keyline)
        white_mask = mask.filter(ImageFilter.MaxFilter(21))

        # 2. Hot Red offset mask (offset +14px, +14px)
        red_mask = Image.new("L", (CW, CH), 0)
        red_mask.paste(white_mask, (14, 14))

        # 3. Soft paper drop shadow mask (offset +24px, +24px)
        shadow_mask = Image.new("L", (CW, CH), 0)
        shadow_mask.paste(white_mask, (24, 24))
        shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(14))

        cutout = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))

        # Layer 1: Drop Shadow
        shadow_col = Image.new("RGBA", (CW, CH), (20, 20, 20, 85))
        cutout.paste(shadow_col, (0, 0), shadow_mask)

        # Layer 2: Offset Hot Red Stroke
        red_col = Image.new("RGBA", (CW, CH), (*COLOR_HOT_RED, 255))
        cutout.paste(red_col, (0, 0), red_mask)

        # Layer 3: Rough White Cut-Paper Keyline
        white_col = Image.new("RGBA", (CW, CH), (*COLOR_PAPER_WHITE, 255))
        cutout.paste(white_col, (0, 0), white_mask)

        # Layer 4: Halftone Figure
        ht_color = Image.new("RGBA", (tw, th), (*COLOR_INK_BLACK, 255))
        ht_paper = Image.new("RGBA", (tw, th), (*COLOR_PAPER_WHITE, 255))
        ht_paper.paste(ht_color, (0, 0), ImageOps.invert(halftone_dots))
        sub_mask = mask.crop((ox, oy, ox + tw, oy + th))
        cutout.paste(ht_paper, (ox, oy), sub_mask)

        return cutout

    def render_red_stat_card(self, number_text: str, label_text: str, width: int = 420, height: int = 240) -> Image.Image:
        """Render iconic $123 style red stat hero card with white paper border and drop shadow."""
        pad = 40
        CW, CH = width + pad * 2, height + pad * 2
        ox, oy = pad, pad

        card_mask = Image.new("L", (CW, CH), 0)
        d_m = ImageDraw.Draw(card_mask)
        d_m.rounded_rectangle([ox, oy, ox + width, oy + height], radius=24, fill=255)
        white_border_mask = card_mask.filter(ImageFilter.MaxFilter(11))

        # Shadow
        shadow_mask = Image.new("L", (CW, CH), 0)
        shadow_mask.paste(white_border_mask, (14, 14))
        shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(10))

        card_img = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        shadow_col = Image.new("RGBA", (CW, CH), (20, 20, 20, 80))
        card_img.paste(shadow_col, (0, 0), shadow_mask)

        # White border
        white_col = Image.new("RGBA", (CW, CH), (*COLOR_PAPER_WHITE, 255))
        card_img.paste(white_col, (0, 0), white_border_mask)

        # Red fill
        red_card = Image.new("RGBA", (width, height), (*COLOR_HOT_RED, 255))
        draw = ImageDraw.Draw(red_card)

        # Numbers and label in pure white
        font_num = self._get_font(92, style="headline")
        font_lbl = self._get_font(24, style="mono")

        # Center number
        draw.text((width // 2, height // 2 - 24), number_text, fill=COLOR_PAPER_WHITE, font=font_num, anchor="mm")
        draw.text((width // 2, height // 2 + 55), label_text.upper(), fill=COLOR_PAPER_WHITE, font=font_lbl, anchor="mm")

        sub_mask = card_mask.crop((ox, oy, ox + width, oy + height))
        card_img.paste(red_card, (ox, oy), sub_mask)
        return card_img

    def render_annotation_tag(self, text: str, bg_color: Tuple[int, int, int] = COLOR_MUSTARD) -> Image.Image:
        """Render Fig. 3 - Trade Route style paper tape annotation tag."""
        font = self._get_font(24, style="mono")
        padding_x, padding_y = 20, 10
        # Calculate size
        temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        tw = (bbox[2] - bbox[0]) + padding_x * 2
        th = (bbox[3] - bbox[1]) + padding_y * 2

        tag = Image.new("RGBA", (tw + 20, th + 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(tag)
        # Drop shadow
        draw.rectangle([14, 14, tw + 14, th + 14], fill=(20, 20, 20, 50))
        # Mustard or white tape
        draw.rectangle([10, 10, tw + 10, th + 10], fill=(*bg_color, 255), outline=COLOR_INK_BLACK, width=1)
        # Typewriter text in ink black
        draw.text((10 + padding_x, 10 + padding_y), text, fill=COLOR_INK_BLACK, font=font)
        return tag

    def render_red_underline(self, draw: ImageDraw.Draw, x1: float, y: float, x2: float, progress: float = 1.0, width: int = 8):
        """Draw tactile Hot Red marker underline with tapered start/end."""
        cur_x2 = x1 + (x2 - x1) * min(1.0, max(0.0, progress))
        if cur_x2 > x1 + 2:
            draw.line([(x1, y), (cur_x2, y)], fill=COLOR_HOT_RED, width=width)
            # Subtle overshoot marker dot
            draw.ellipse([cur_x2 - width // 2, y - width // 2, cur_x2 + width // 2, y + width // 2], fill=COLOR_HOT_RED)

    def render_red_pin(self, draw: ImageDraw.Draw, cx: float, cy: float, scale: float = 1.0):
        """Draw iconic red map pin with drop shadow (from Component Zoo)."""
        r = 16 * scale
        # Shadow
        draw.ellipse([cx - r + 6, cy - r + 8, cx + r + 6, cy + r + 8], fill=(20, 20, 20, 60))
        # Red Pin Head
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=COLOR_HOT_RED, outline=COLOR_PAPER_WHITE, width=int(3 * scale))
        # White inner core
        draw.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45], fill=COLOR_PAPER_WHITE)
        # Pin needle
        draw.polygon([(cx - 3, cy + r - 2), (cx + 3, cy + r - 2), (cx, cy + r + 18 * scale)], fill=COLOR_INK_BLACK)

    def render_red_arrow(self, draw: ImageDraw.Draw, start_pt: Tuple[float, float], end_pt: Tuple[float, float], progress: float = 1.0, width: int = 5):
        """Draw Hot Red directional arrow from start_pt toward end_pt."""
        x1, y1 = start_pt
        x2, y2 = end_pt
        prog = min(1.0, max(0.0, progress))
        cur_x = x1 + (x2 - x1) * prog
        cur_y = y1 + (y2 - y1) * prog
        if prog > 0.05:
            draw.line([(x1, y1), (cur_x, cur_y)], fill=COLOR_HOT_RED, width=width)
            # Arrowhead
            angle = math.atan2(y2 - y1, x2 - x1)
            arrow_len = 18
            arrow_angle = math.pi / 6.0
            p1 = (cur_x - arrow_len * math.cos(angle - arrow_angle), cur_y - arrow_len * math.sin(angle - arrow_angle))
            p2 = (cur_x - arrow_len * math.cos(angle + arrow_angle), cur_y - arrow_len * math.sin(angle + arrow_angle))
            draw.polygon([(cur_x, cur_y), p1, p2], fill=COLOR_HOT_RED)

    # -------------------------------------------------------------------------
    # OFFICIAL COMPANY MOTION PRIMITIVES (STEP 8)
    # -------------------------------------------------------------------------

    def alert_wash(self, frame: Image.Image, progress: float, max_tint: float = 0.85) -> Image.Image:
        """ALERT_WASH: Entire frame floods toward Hot Red accent tone (#D62E1F) and settles back."""
        # Progress 0.0 -> 0.5 floods to red, 0.5 -> 1.0 recovers to tan
        if progress <= 0.0 or progress >= 1.0:
            return frame
        flood = math.sin(progress * math.pi) * max_tint
        red_wash = Image.new("RGB", frame.size, COLOR_HOT_RED)
        return Image.blend(frame, red_wash, flood)

    def tick_up(self, start_val: float, target_val: float, progress: float, is_int: bool = False, format_str: str = "{:.1f}") -> str:
        """TICK_UP: Ticking counter updating to factual target value with slight spring settle."""
        prog = min(1.0, max(0.0, progress))
        # Logarithmic ease-out toward verified number
        eased = 1.0 - math.pow(1.0 - prog, 3)
        val = start_val + (target_val - start_val) * eased
        if is_int:
            return f"{int(round(val)):,}"
        return format_str.format(val)

    def tear(self, frame: Image.Image, tear_y: int, progress: float, width: int = 1080) -> Image.Image:
        """TEAR: Creates a physical jagged cut-paper tear edge splitting or revealing paper depth."""
        prog = min(1.0, max(0.0, progress))
        if prog <= 0.0:
            return frame
        torn = frame.copy()
        draw = ImageDraw.Draw(torn)
        # Generate jagged tear line
        points = []
        rng = np.random.RandomState(42)
        step = 30
        for x in range(0, width + step, step):
            offset = rng.randint(-8, 8)
            points.append((x, tear_y + offset))
        points.extend([(width, tear_y + 80), (0, tear_y + 80)])
        draw.polygon(points, fill=COLOR_CARD_BG)
        # White paper fiber fray border along the tear
        for i in range(len(points) - 3):
            draw.line([points[i], points[i+1]], fill=COLOR_PAPER_WHITE, width=4)
        return torn

    def stamp(self, base_img: Image.Image, stamp_img: Image.Image, pos: Tuple[int, int], progress: float) -> Image.Image:
        """STAMP: Tactile physical stamp slamming down onto paper with slight scale overshoot."""
        prog = min(1.0, max(0.0, progress))
        if prog <= 0.0:
            return base_img
        out = base_img.copy()
        if prog < 1.0:
            # Slam from 1.35x down to 1.0x
            scale = 1.0 + (1.0 - prog) * 0.35
            sw = max(1, int(stamp_img.width * scale))
            sh = max(1, int(stamp_img.height * scale))
            resized = stamp_img.resize((sw, sh), Image.Resampling.BILINEAR)
            ox = pos[0] - (sw - stamp_img.width) // 2
            oy = pos[1] - (sh - stamp_img.height) // 2
            out.paste(resized, (ox, oy), resized)
        else:
            out.paste(stamp_img, pos, stamp_img)
        return out

    def thread_pull(self, draw: ImageDraw.Draw, pt_a: Tuple[float, float], pt_b: Tuple[float, float], progress: float, color: Tuple[int, int, int] = COLOR_HOT_RED, width: int = 4):
        """THREAD_PULL: Taut connector string line extending between nodes with tactile snap."""
        prog = min(1.0, max(0.0, progress))
        if prog <= 0.0:
            return
        x1, y1 = pt_a
        x2, y2 = pt_b
        cur_x = x1 + (x2 - x1) * prog
        cur_y = y1 + (y2 - y1) * prog
        draw.line([(x1, y1), (cur_x, cur_y)], fill=color, width=width)
        # Knot/anchor points
        draw.ellipse([x1 - 5, y1 - 5, x1 + 5, y1 + 5], fill=COLOR_INK_BLACK)
        if prog > 0.95:
            draw.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=COLOR_INK_BLACK)

    def underline(self, draw: ImageDraw.Draw, x1: float, y: float, x2: float, progress: float = 1.0, width: int = 8, color: Tuple[int, int, int] = COLOR_HOT_RED):
        """UNDERLINE: Tactile Hot Red marker swipe with tapered start and overshoot dot."""
        self.render_red_underline(draw, x1, y, x2, progress=progress, width=width)

    def counter_slam(self, base_img: Image.Image, number_img: Image.Image, center_pos: Tuple[int, int], progress: float) -> Image.Image:
        """COUNTER_SLAM: Number flies toward the lens and snaps into razor focus with drop shadow."""
        prog = min(1.0, max(0.0, progress))
        out = base_img.copy()
        if prog <= 0.0:
            return out
        # Scale from 2.0x down to 1.0x
        scale = 1.0 + math.pow(1.0 - prog, 2) * 1.0
        sw = max(1, int(number_img.width * scale))
        sh = max(1, int(number_img.height * scale))
        resized = number_img.resize((sw, sh), Image.Resampling.BILINEAR)
        cx, cy = center_pos
        ox = cx - sw // 2
        oy = cy - sh // 2
        out.paste(resized, (ox, oy), resized)
        return out

    def paper_pop(self, base_img: Image.Image, element_img: Image.Image, target_pos: Tuple[int, int], progress: float) -> Image.Image:
        """PAPER_POP: Spring pop-up with overshoot rising from below lower paper layer."""
        prog = min(1.0, max(0.0, progress))
        if prog <= 0.0:
            return base_img
        out = base_img.copy()
        # Spring overshoot curve
        spring = math.sin(prog * math.pi * 0.75) * 1.06 if prog < 1.0 else 1.0
        offset_y = int((1.0 - spring) * 80)
        out.paste(element_img, (target_pos[0], target_pos[1] + offset_y), element_img)
        return out

    def paper_slide(self, base_img: Image.Image, element_img: Image.Image, start_pos: Tuple[int, int], end_pos: Tuple[int, int], progress: float) -> Image.Image:
        """PAPER_SLIDE: Card sliding smoothly across paper stage with friction deceleration."""
        prog = min(1.0, max(0.0, progress))
        if prog <= 0.0:
            return base_img
        out = base_img.copy()
        eased = 1.0 - math.pow(1.0 - prog, 3)
        cur_x = int(start_pos[0] + (end_pos[0] - start_pos[0]) * eased)
        cur_y = int(start_pos[1] + (end_pos[1] - start_pos[1]) * eased)
        out.paste(element_img, (cur_x, cur_y), element_img)
        return out

    def cutout_pop(self, base_img: Image.Image, cutout_img: Image.Image, target_pos: Tuple[int, int], progress: float) -> Image.Image:
        """CUTOUT_POP: Halftone figure cutout popping up with white border and offset red stroke."""
        return self.paper_pop(base_img, cutout_img, target_pos, progress)

    def photo_card_enter(self, base_img: Image.Image, card_img: Image.Image, final_pos: Tuple[int, int], progress: float, angle_deg: float = -2.5) -> Image.Image:
        """PHOTO_CARD_ENTER: Staggered archival photo card sliding and rotating with paper drop shadow."""
        prog = min(1.0, max(0.0, progress))
        if prog <= 0.0:
            return base_img
        out = base_img.copy()
        rotated = card_img.rotate(angle_deg * prog, resample=Image.Resampling.BICUBIC, expand=True)
        eased = 1.0 - math.pow(1.0 - prog, 2)
        cur_y = int(final_pos[1] + (1.0 - eased) * 120)
        out.paste(rotated, (final_pos[0], cur_y), rotated)
        return out

    def annotation_draw(self, draw: ImageDraw.Draw, text: str, pos: Tuple[int, int], font: ImageFont.ImageFont, progress: float, with_underline: bool = True):
        """ANNOTATION_DRAW: Typewriter text reveal with accompanying hot-red underline swipe."""
        prog = min(1.0, max(0.0, progress))
        if prog <= 0.0:
            return
        num_chars = int(len(text) * prog)
        visible_text = text[:num_chars]
        draw.text(pos, visible_text, fill=COLOR_INK_BLACK, font=font)
        if with_underline and prog > 0.4:
            bbox = draw.textbbox(pos, visible_text, font=font)
            line_prog = min(1.0, (prog - 0.4) / 0.6)
            self.underline(draw, pos[0], bbox[3] + 4, bbox[2], progress=line_prog, width=4)

    # Uppercase aliases matching official prompt naming
    ALERT_WASH = alert_wash
    TICK_UP = tick_up
    TEAR = tear
    STAMP = stamp
    THREAD_PULL = thread_pull
    UNDERLINE = underline
    COUNTER_SLAM = counter_slam
    PAPER_POP = paper_pop
    PAPER_SLIDE = paper_slide
    CUTOUT_POP = cutout_pop
    PHOTO_CARD_ENTER = photo_card_enter
    ANNOTATION_DRAW = annotation_draw

    # -------------------------------------------------------------------------
    # BEAT RENDERING METHODS (8 BEATS)
    # -------------------------------------------------------------------------

    def render_beat1_hook(self, output_path: Path, duration: float = 4.0, fps: int = 30) -> Path:
        """Beat 1: The Hook (0-4s)
        Aged map background + Halftone trader cutout (trader_char_01) with white keyline & offset Hot Red stroke
        + Giant printed 2:17 AM + Phone paper card. Slow push-in through paper layers.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_beat1_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        width, height = 1080, 1920

        # Pre-generate elements
        bg_master = self.create_archival_paper_canvas(width, height, with_map=True)
        trader_img_path = self.assets_dir / "cinematic" / "scene_01_trader_217am.jpg"
        cutout = self.create_halftone_cutout(trader_img_path, target_size=(560, 740), border_radius=50)
        stat_card = self.render_red_stat_card("2:17 AM", "ALONE AT THE TERMINAL", width=480, height=220)
        annotation = self.render_annotation_tag("Fig. 1 - Late-Night Retail Dilemma", bg_color=COLOR_MUSTARD)

        font_label = self._get_font(28, style="mono")

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)  # 0.0 to 1.0
            # Physical camera move: Slow 3% push-in through layers
            zoom = 1.0 + 0.035 * t

            frame = bg_master.copy()
            draw = ImageDraw.Draw(frame)

            # Midground: Cutout figure springs up with slight overshoot (PAPER_POP)
            pop_progress = min(1.0, t / 0.35)
            # Spring overshoot function
            spring_y = math.sin(pop_progress * math.pi * 0.75) * 1.05 if pop_progress < 1.0 else 1.0
            cutout_y = int(450 - (spring_y * 100))
            cutout_x = 240

            frame.paste(cutout, (cutout_x, cutout_y), cutout)

            # Foreground: Giant 2:17 AM Stat Card (snaps in from bottom with drop shadow)
            card_enter = min(1.0, max(0.0, (t - 0.15) / 0.30))
            card_y = int(1220 - card_enter * 120)
            card_x = (width - stat_card.width) // 2
            frame.paste(stat_card, (card_x, card_y), stat_card)

            # Foreground: Annotation tag
            frame.paste(annotation, (100, 1460), annotation)

            # Red underline swipe beneath annotation
            underline_prog = min(1.0, max(0.0, (t - 0.40) / 0.30))
            self.render_red_underline(draw, 100, 1540, 560, progress=underline_prog, width=6)

            # Small phone indicator card
            draw.rectangle([width - 320, 1460, width - 100, 1520], fill=COLOR_PAPER_WHITE, outline=COLOR_INK_BLACK, width=2)
            draw.text((width - 300, 1478), "NOTIFICATION: SELL", fill=COLOR_HOT_RED, font=font_label)

            # Apply slow camera drift
            if zoom != 1.0:
                crop_w = int(width / zoom)
                crop_h = int(height / zoom)
                x0 = (width - crop_w) // 2
                y0 = (height - crop_h) // 2
                frame = frame.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((width, height), Image.Resampling.BILINEAR)

            frame.save(temp_dir / f"frame_{frame_idx:04d}.png", "PNG")

        cmd = [
            self.ffmpeg.ffmpeg_path, "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Beat 1 paper diorama hook rendered: %s", output_path)
        return output_path

    def render_beat2_montage(self, output_path: Path, duration: float = 5.0, fps: int = 30) -> Path:
        """Beat 2: Information Overload (4-9s)
        Stacked newspaper columns, faded financial charts, multiple halftone trader/screen cutouts,
        archival photo cards, ticker strips, red arrows, red underlines. Fast lateral track across paper layers.
        Zero random readable text! All headlines rendered deterministically.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_beat2_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        width, height = 1080, 1920

        bg_master = self.create_archival_paper_canvas(width + 600, height, with_map=True)
        font_h1 = self._get_font(52, style="headline")
        font_mono = self._get_font(26, style="mono")
        font_stat = self._get_font(36, style="headline")

        # Create paper cards for collage (NO unsupported statistics)
        photo_card1 = self.render_annotation_tag("BREAKING: FED RATE REVERSAL", bg_color=COLOR_PAPER_WHITE)
        photo_card2 = self.render_annotation_tag("ANALYST CONSENSUS: SPLIT", bg_color=COLOR_MUSTARD)
        stat_card = self.render_red_stat_card("ALERT", "MARKET NOISE", width=400, height=180)

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)

            # Lateral camera tracking move: Pan from left to right (offset 0 to 450px)
            pan_x = int(t * 380)
            frame = bg_master.crop((pan_x, 0, pan_x + width, height))
            draw = ImageDraw.Draw(frame)

            # Draw background newspaper columns (simulated clean editorial columns)
            col_w = 260
            for col_i in range(4):
                cx = 60 + col_i * (col_w + 30) - (pan_x % 80)
                draw.rectangle([cx, 160, cx + col_w, 1720], fill=(238, 230, 212), outline=(180, 168, 140), width=1)
                # Simulated neat typographic rule lines
                for ly in range(220, 1680, 36):
                    draw.line([(cx + 15, ly), (cx + col_w - 15, ly)], fill=(160, 150, 130), width=2)

            # Header label
            draw.text((90, 120), "INFORMATION OVERLOAD // ARCHIVAL MEDIA FEED", fill=COLOR_INK_BLACK, font=font_mono)
            self.render_red_underline(draw, 90, 160, 780, progress=1.0, width=4)

            # Staggered entrance 1: Newspaper photo card (t > 0.1)
            e1 = min(1.0, max(0.0, (t - 0.08) / 0.25))
            if e1 > 0:
                y1 = int(320 - e1 * 40)
                frame.paste(photo_card1, (120, y1), photo_card1)
                self.render_red_pin(draw, 140, y1 + 10, scale=1.0)

            # Staggered entrance 2: Giant Stat card (t > 0.25)
            e2 = min(1.0, max(0.0, (t - 0.22) / 0.25))
            if e2 > 0:
                y2 = int(580 - e2 * 50)
                frame.paste(stat_card, (width - 480, y2), stat_card)
                # Draw red arrow pointing to stat
                self.render_red_arrow(draw, (width - 560, y2 + 80), (width - 490, y2 + 80), progress=e2, width=6)

            # Staggered entrance 3: Ticker strips
            e3 = min(1.0, max(0.0, (t - 0.40) / 0.25))
            if e3 > 0:
                y3 = int(980 - e3 * 40)
                draw.rectangle([80, y3, width - 80, y3 + 80], fill=COLOR_INK_BLACK, outline=COLOR_HOT_RED, width=2)
                draw.text((110, y3 + 24), "TICKER: SPY -1.4% // QQQ -2.1% // VIX +18.4% // BREADTH 28%", fill=COLOR_PAPER_WHITE, font=font_mono)

            # Staggered entrance 4: Second card (t > 0.60)
            e4 = min(1.0, max(0.0, (t - 0.55) / 0.25))
            if e4 > 0:
                y4 = int(1240 - e4 * 40)
                frame.paste(photo_card2, (120, y4), photo_card2)
                self.render_red_underline(draw, 120, y4 + 65, 520, progress=e4, width=5)

            # Bottom warning callout
            draw.rectangle([80, 1460, width - 80, 1600], fill=COLOR_PAPER_WHITE, outline=COLOR_INK_BLACK, width=2)
            draw.text((120, 1500), "EVERYONE SEES THE NOISE. NO ONE SEES THE MOVE.", fill=COLOR_HOT_RED, font=font_h1)

            frame.save(temp_dir / f"frame_{frame_idx:04d}.png", "PNG")

        cmd = [
            self.ffmpeg.ffmpeg_path, "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Beat 2 paper diorama montage rendered: %s", output_path)
        return output_path

    def render_beat3_problem_typography(self, output_path: Path, duration: float = 4.0, fps: int = 30) -> Path:
        """Beat 3: The Problem (9-13s)
        Abrupt freeze. Reduce complexity. Plain archival tan background (#C9BB9C).
        Giant condensed bold typography in Ink Black:
        0-2s: TOO MUCH INFORMATION.
        2-4s: NOT ENOUGH SIGNAL. with Hot Red underline beneath SIGNAL.
        Very subtle camera drift (2%). Near silence.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_beat3_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        width, height = 1080, 1920

        bg_master = self.create_archival_paper_canvas(width, height, with_map=False)
        font_h1 = self._get_font(78, style="headline")
        font_mono = self._get_font(26, style="mono")

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)
            zoom = 1.0 + 0.02 * t

            frame = bg_master.copy()
            draw = ImageDraw.Draw(frame)

            # Header metadata tag
            draw.text((90, 180), "THE CORE PROBLEM // INFORMATION EFFICIENCY", fill=COLOR_HALFTONE_GRAY, font=font_mono)
            draw.line([(90, 220), (width - 90, 220)], fill=(180, 168, 140), width=2)

            cy = height // 2 - 120

            # Part 1 (0 to 0.48): TOO MUCH INFORMATION.
            if t < 0.48:
                draw.text((90, cy - 80), "TOO MUCH", fill=COLOR_INK_BLACK, font=font_h1)
                draw.text((90, cy + 20), "INFORMATION.", fill=COLOR_INK_BLACK, font=font_h1)
                # Gray secondary line
                draw.line([(90, cy + 130), (520, cy + 130)], fill=COLOR_HALFTONE_GRAY, width=4)

            # Part 2 (0.48 to 1.0): NOT ENOUGH SIGNAL.
            else:
                draw.text((90, cy - 80), "NOT ENOUGH", fill=COLOR_INK_BLACK, font=font_h1)
                draw.text((90, cy + 20), "SIGNAL.", fill=COLOR_HOT_RED, font=font_h1)

                # Hot Red underline swipe beneath SIGNAL (UNDERLINE primitive)
                underline_prog = min(1.0, (t - 0.48) / 0.22)
                self.render_red_underline(draw, 90, cy + 130, 420, progress=underline_prog, width=10)

                # Monospace subtitle
                draw.text((90, cy + 180), "THE NOISE IS LOUD. THE MOVE IS SILENT.", fill=COLOR_INK_BLACK, font=font_mono)

            # Clean paper frame border
            draw.rectangle([50, 50, width - 50, height - 50], outline=(170, 156, 128), width=3)

            # Apply slow camera drift
            if zoom != 1.0:
                crop_w = int(width / zoom)
                crop_h = int(height / zoom)
                x0 = (width - crop_w) // 2
                y0 = (height - crop_h) // 2
                frame = frame.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((width, height), Image.Resampling.BILINEAR)

            frame.save(temp_dir / f"frame_{frame_idx:04d}.png", "PNG")

        cmd = [
            self.ffmpeg.ffmpeg_path, "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Beat 3 kinetic typography rendered: %s", output_path)
        return output_path

    def render_beat4_crowd_signal(self, output_path: Path, duration: float = 6.0, fps: int = 30) -> Path:
        """Beat 4: The Crowd: Chaos to Conviction (13-19s)
        Faded map/ledger background + small halftone trader cutouts, sentiment marks, pins.
        THREAD_PULL red connector lines linking them into directional consensus.
        Final foreground statistic: 1,482,930 TRADER INPUTS.
        CRITICAL: Never display fake/intermediate factual numbers! Animate graphical density, not the number.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_beat4_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        width, height = 1080, 1920

        bg_master = self.create_archival_paper_canvas(width, height, with_map=True)
        stat_card = self.render_red_stat_card("1,482,930", "VERIFIED TRADER INPUTS", width=520, height=240)
        font_mono = self._get_font(26, style="mono")
        font_h1 = self._get_font(42, style="headline")

        # Generate 45 small crowd node coordinates
        rng = np.random.RandomState(1337)
        nodes = []
        for _ in range(45):
            nodes.append({
                "x": rng.uniform(120, width - 120),
                "y": rng.uniform(320, 1180),
                "dx": rng.uniform(-20, 20),
                "dy": rng.uniform(-20, 20),
            })

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)
            zoom = 1.0 + 0.04 * t

            frame = bg_master.copy()
            draw = ImageDraw.Draw(frame)

            # Header
            draw.text((90, 140), "COLLECTIVE CONVICTION ENGINE // CROWD INTELLIGENCE", fill=COLOR_INK_BLACK, font=font_mono)
            self.render_red_underline(draw, 90, 175, 780, progress=1.0, width=3)
            draw.text((90, 210), "THE POWER OF AGGREGATE SENTIMENT", fill=COLOR_INK_BLACK, font=font_h1)

            # THREAD_PULL: Progressively connect nodes with red threads as t advances
            thread_prog = min(1.0, max(0.0, (t - 0.15) / 0.45))

            # Draw nodes (small paper halftone pins)
            for i, n in enumerate(nodes):
                nx = n["x"] + math.sin(t * 2 + i) * 4
                ny = n["y"] + math.cos(t * 2 + i) * 4
                self.render_red_pin(draw, nx, ny, scale=0.6)

            # Draw red thread connections
            if thread_prog > 0:
                active_links = int(thread_prog * (len(nodes) - 1))
                for i in range(active_links):
                    p1 = (nodes[i]["x"], nodes[i]["y"])
                    p2 = (nodes[(i * 7) % len(nodes)]["x"], nodes[(i * 7) % len(nodes)]["y"])
                    draw.line([p1, p2], fill=COLOR_HOT_RED, width=2)

            # Foreground: Final Verified Stat Card (snaps in after t > 0.50)
            if t > 0.45:
                card_enter = min(1.0, (t - 0.45) / 0.20)
                card_y = int(1240 - card_enter * 100)
                card_x = (width - stat_card.width) // 2
                frame.paste(stat_card, (card_x, card_y), stat_card)

                # Label tag
                tag = self.render_annotation_tag("Fig. 2 - Aggregated Conviction Threshold", bg_color=COLOR_MUSTARD)
                frame.paste(tag, (120, 1480), tag)

            # Apply slow camera drift
            if zoom != 1.0:
                crop_w = int(width / zoom)
                crop_h = int(height / zoom)
                x0 = (width - crop_w) // 2
                y0 = (height - crop_h) // 2
                frame = frame.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((width, height), Image.Resampling.BILINEAR)

            frame.save(temp_dir / f"frame_{frame_idx:04d}.png", "PNG")

        cmd = [
            self.ffmpeg.ffmpeg_path, "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Beat 4 crowd consensus rendered: %s", output_path)
        return output_path

    def render_beat5_data_proof(self, output_path: Path, duration: float = 8.0, fps: int = 30) -> Path:
        """Beat 5: The Proof: One Fact at a Time (19-27s)
        Two separate editorial moments on archival paper cards:
        Moment A (0-4s): 68.4% DIRECTIONAL ACCURACY (TICK_UP) on printed directional chart with retail comparison.
        Moment B (4-8s): 14.6 HOURS EARLY-WARNING LEAD with red arrow moving ahead of timeline.
        No neon, no glass, no dashboard.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_beat5_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        width, height = 1080, 1920

        bg_master = self.create_archival_paper_canvas(width, height, with_map=False)
        font_large = self._get_font(110, style="headline")
        font_h1 = self._get_font(44, style="headline")
        font_mono = self._get_font(24, style="mono")
        font_body = self._get_font(28, style="bold")

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)

            frame = bg_master.copy()
            draw = ImageDraw.Draw(frame)

            draw.text((90, 140), "CROWDWISDOM // BENCHMARK VERIFICATION", fill=COLOR_HALFTONE_GRAY, font=font_mono)
            draw.line([(90, 175), (width - 90, 175)], fill=(180, 168, 140), width=2)

            cy = height // 2 - 80

            # MOMENT A: 68.4% Directional Accuracy (0.0 to 0.48)
            if t < 0.48:
                draw.text((90, 210), "EVIDENCE 01: PREDICTIVE CONVICTION", fill=COLOR_INK_BLACK, font=font_h1)

                # Physical paper card
                card_x1, card_y1 = 90, cy - 200
                card_x2, card_y2 = width - 90, cy + 340
                # Drop shadow
                draw.rounded_rectangle([card_x1 + 14, card_y1 + 14, card_x2 + 14, card_y2 + 14], radius=20, fill=(20, 20, 20, 60))
                # White paper card
                draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=20, fill=COLOR_CARD_BG, outline=COLOR_INK_BLACK, width=2)

                # TICK_UP: Animate into final verified value with slight spring overshoot
                ease_1 = min(1.0, t / 0.28)
                val_display = f"{68.4 * ease_1:.1f}%"
                draw.text((150, cy - 140), val_display, fill=COLOR_HOT_RED, font=font_large)
                draw.text((150, cy), "DIRECTIONAL ACCURACY", fill=COLOR_INK_BLACK, font=font_h1)
                draw.text((150, cy + 60), "Validated against multi-year trading benchmark.", fill=COLOR_HALFTONE_GRAY, font=font_body)

                # Comparative clean printed bars
                bar_y = cy + 130
                draw.text((150, bar_y), "Retail Baseline (41.2%)", fill=COLOR_HALFTONE_GRAY, font=font_mono)
                draw.rectangle([150, bar_y + 30, 150 + int(41.2 * 8 * ease_1), bar_y + 55], fill=COLOR_HALFTONE_GRAY)

                draw.text((150, bar_y + 75), "CrowdWisdom Consensus (68.4%)", fill=COLOR_INK_BLACK, font=font_mono)
                draw.rectangle([150, bar_y + 105, 150 + int(68.4 * 8 * ease_1), bar_y + 130], fill=COLOR_HOT_RED)

                tag = self.render_annotation_tag("Fig. 3 - Directional Accuracy Metric", bg_color=COLOR_MUSTARD)
                frame.paste(tag, (120, cy + 380), tag)

            # MOMENT B: 14.6 Hours Early-Warning Lead (0.48 to 1.0)
            else:
                draw.text((90, 210), "EVIDENCE 02: TEMPORAL ADVANTAGE", fill=COLOR_INK_BLACK, font=font_h1)

                card_x1, card_y1 = 90, cy - 200
                card_x2, card_y2 = width - 90, cy + 340
                draw.rounded_rectangle([card_x1 + 14, card_y1 + 14, card_x2 + 14, card_y2 + 14], radius=20, fill=(20, 20, 20, 60))
                draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=20, fill=COLOR_CARD_BG, outline=COLOR_INK_BLACK, width=2)

                ease_2 = min(1.0, (t - 0.48) / 0.28)
                disp_lead = f"{14.6 * ease_2:.1f} HOURS"
                draw.text((150, cy - 140), disp_lead, fill=COLOR_HOT_RED, font=font_large)
                draw.text((150, cy), "EARLY-WARNING LEAD TIME", fill=COLOR_INK_BLACK, font=font_h1)
                draw.text((150, cy + 60), "Sentiment signals precede price moves by over half a day.", fill=COLOR_HALFTONE_GRAY, font=font_body)

                # Printed Timeline with red arrow moving ahead
                line_y = cy + 180
                draw.line([(150, line_y), (width - 150, line_y)], fill=COLOR_INK_BLACK, width=3)
                # Ticks on timeline
                for tx in range(150, width - 150, 110):
                    draw.line([(tx, line_y - 8), (tx, line_y + 8)], fill=COLOR_INK_BLACK, width=2)

                # Red arrow moving ahead of timeline
                arrow_x = 150 + int((width - 340) * ease_2)
                self.render_red_arrow(draw, (arrow_x - 80, line_y - 45), (arrow_x, line_y - 45), progress=1.0, width=6)
                draw.text((arrow_x - 120, line_y - 95), "LEAD VECTOR", fill=COLOR_HOT_RED, font=font_mono)

                tag = self.render_annotation_tag("Fig. 4 - Average Sentiment Inflection Lead", bg_color=COLOR_MUSTARD)
                frame.paste(tag, (120, cy + 380), tag)

            frame.save(temp_dir / f"frame_{frame_idx:04d}.png", "PNG")

        cmd = [
            self.ffmpeg.ffmpeg_path, "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Beat 5 data proof rendered: %s", output_path)
        return output_path

    def render_beat6_signal_resolve(self, output_path: Path, duration: float = 7.0, fps: int = 30) -> Path:
        """Beat 6: The Signal: Order from Chaos (27-34s)
        Return to the EXACT SAME retail trader cutout (trader_char_01), now in calm posture.
        Paper trading screen + clean Hot Red directional signal line as the path forward.
        ALERT_WASH: Brief Hot Red flood occurs strictly ONCE here, then returns to archival tan.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_beat6_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        width, height = 1080, 1920

        bg_master = self.create_archival_paper_canvas(width, height, with_map=True)
        trader_img_path = self.assets_dir / "cinematic" / "scene_06_trader_calm.jpg"
        cutout = self.create_halftone_cutout(trader_img_path, target_size=(540, 720), border_radius=40)

        font_h1 = self._get_font(46, style="headline")
        font_mono = self._get_font(26, style="mono")

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)

            frame = bg_master.copy()
            draw = ImageDraw.Draw(frame)

            # Header
            draw.text((90, 140), "NARRATIVE RESOLUTION // THE CLARITY OF CONVICTION", fill=COLOR_INK_BLACK, font=font_mono)
            draw.line([(90, 175), (width - 90, 175)], fill=(180, 168, 140), width=2)

            # Place halftone trader cutout
            frame.paste(cutout, (270, 360), cutout)

            # Paper trading card with clean Hot Red directional signal line
            card_y = 1180
            draw.rounded_rectangle([90 + 10, card_y + 10, width - 90 + 10, card_y + 360 + 10], radius=20, fill=(20, 20, 20, 50))
            draw.rounded_rectangle([90, card_y, width - 90, card_y + 360], radius=20, fill=COLOR_CARD_BG, outline=COLOR_INK_BLACK, width=2)

            draw.text((130, card_y + 40), "CROWD SENTIMENT SIGNAL PATH", fill=COLOR_INK_BLACK, font=font_h1)

            # Draw clean Hot Red directional signal line
            line_prog = min(1.0, t / 0.60)
            pts = [(130, card_y + 260), (320, card_y + 240), (540, card_y + 160), (740, card_y + 190), (900, card_y + 110)]
            active_pts = pts[:max(2, int(line_prog * len(pts)) + 1)]
            draw.line(active_pts, fill=COLOR_HOT_RED, width=6)
            if len(active_pts) > 1:
                end_p = active_pts[-1]
                self.render_red_pin(draw, end_p[0], end_p[1], scale=0.8)

            tag = self.render_annotation_tag("Fig. 5 - Predictive Path Verified", bg_color=COLOR_MUSTARD)
            frame.paste(tag, (130, card_y + 290), tag)

            # ALERT_WASH: Brief Hot Red flood between t=0.22 and t=0.32 (used strictly ONCE)
            if 0.22 <= t <= 0.32:
                wash_factor = math.sin((t - 0.22) / 0.10 * math.pi) * 0.40
                red_overlay = Image.new("RGB", (width, height), COLOR_HOT_RED)
                frame = Image.blend(frame, red_overlay, wash_factor)

            frame.save(temp_dir / f"frame_{frame_idx:04d}.png", "PNG")

        cmd = [
            self.ffmpeg.ffmpeg_path, "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Beat 6 signal resolve rendered: %s", output_path)
        return output_path

    def render_beat7_product_radar(self, output_path: Path, duration: float = 6.0, fps: int = 30) -> Path:
        """Beat 7: Product: Sentiment Radar Feature (34-40s)
        Real CrowdWisdom product capture mounted inside a paper card frame with subtle drop shadow.
        Hot Red underline, annotation card labeled CROWD CONVICTION. Slow quarter orbit.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_beat7_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        width, height = 1080, 1920

        bg_master = self.create_archival_paper_canvas(width, height, with_map=True)
        prod_img_path = self.assets_dir / "cinematic" / "scene_07_product_radar.jpg"
        prod_raw = Image.open(prod_img_path).convert("RGB")
        pw, ph = 840, 960
        prod_scaled = prod_raw.resize((pw, ph), Image.Resampling.LANCZOS)

        font_h1 = self._get_font(44, style="headline")
        font_mono = self._get_font(26, style="mono")

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)
            zoom = 1.0 + 0.03 * t

            frame = bg_master.copy()
            draw = ImageDraw.Draw(frame)

            draw.text((90, 140), "PROPRIETARY PLATFORM // EARLY-WARNING SENTIMENT RADAR", fill=COLOR_INK_BLACK, font=font_mono)
            draw.line([(90, 175), (width - 90, 175)], fill=(180, 168, 140), width=2)
            draw.text((90, 210), "REAL-TIME CONSENSUS TRACKING", fill=COLOR_INK_BLACK, font=font_h1)

            # Paper frame holding product capture
            card_x = (width - pw) // 2
            card_y = 300

            # Drop shadow
            draw.rounded_rectangle([card_x + 16, card_y + 16, card_x + pw + 16, card_y + ph + 16], radius=24, fill=(20, 20, 20, 75))
            # White paper mount
            draw.rounded_rectangle([card_x - 12, card_y - 12, card_x + pw + 12, card_y + ph + 12], radius=24, fill=COLOR_PAPER_WHITE, outline=COLOR_INK_BLACK, width=2)

            frame.paste(prod_scaled, (card_x, card_y))

            # Mustard tag labeled CROWD CONVICTION
            tag = self.render_annotation_tag("CROWD CONVICTION // MULTI-ASSET RADAR", bg_color=COLOR_MUSTARD)
            frame.paste(tag, (card_x + 30, card_y + ph + 40), tag)
            self.render_red_underline(draw, card_x + 30, card_y + ph + 105, card_x + 620, progress=1.0, width=6)

            if zoom != 1.0:
                crop_w = int(width / zoom)
                crop_h = int(height / zoom)
                x0 = (width - crop_w) // 2
                y0 = (height - crop_h) // 2
                frame = frame.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((width, height), Image.Resampling.BILINEAR)

            frame.save(temp_dir / f"frame_{frame_idx:04d}.png", "PNG")

        cmd = [
            self.ffmpeg.ffmpeg_path, "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Beat 7 product radar rendered: %s", output_path)
        return output_path

    def render_beat8_minimal_cta(self, output_path: Path, duration: float = 5.0, fps: int = 30) -> Path:
        """Beat 8: CTA: See the Signal (40-45s)
        Clean archival paper stage (#C9BB9C). No particles, no dashboard.
        Bold ink black lockup:
        CROWDWISDOM TRADING
        SEE THE SIGNAL INSIDE THE NOISE.
        crowdwisdomtrading.com
        Hot Red underline. Very slow 2% camera drift.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_beat8_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        width, height = 1080, 1920

        bg_master = self.create_archival_paper_canvas(width, height, with_map=False)
        font_brand = self._get_font(64, style="headline")
        font_tagline = self._get_font(42, style="headline")
        font_url = self._get_font(34, style="mono")
        font_meta = self._get_font(22, style="mono")

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)
            zoom = 1.0 + 0.02 * t

            frame = bg_master.copy()
            draw = ImageDraw.Draw(frame)

            # Elegant paper border frame
            draw.rectangle([70, 70, width - 70, height - 70], outline=COLOR_INK_BLACK, width=2)
            draw.rectangle([80, 80, width - 80, height - 80], outline=(180, 168, 140), width=1)

            cy = height // 2 - 60

            # CROWDWISDOM TRADING
            draw.text((width // 2, cy - 140), "CROWDWISDOM TRADING", fill=COLOR_INK_BLACK, font=font_brand, anchor="mm")

            # Tagline
            draw.text((width // 2, cy - 30), "SEE THE SIGNAL", fill=COLOR_INK_BLACK, font=font_tagline, anchor="mm")
            draw.text((width // 2, cy + 30), "INSIDE THE NOISE.", fill=COLOR_INK_BLACK, font=font_tagline, anchor="mm")

            # Hot Red underline swipe beneath tagline
            underline_prog = min(1.0, t / 0.40)
            self.render_red_underline(draw, width // 2 - 240, cy + 75, width // 2 + 240, progress=underline_prog, width=6)

            # URL in rounded paper button
            btn_w, btn_h = 560, 80
            btn_x1 = width // 2 - btn_w // 2
            btn_y1 = cy + 140
            # Button drop shadow
            draw.rounded_rectangle([btn_x1 + 6, btn_y1 + 6, btn_x1 + btn_w + 6, btn_y1 + btn_h + 6], radius=16, fill=(20, 20, 20, 40))
            # Button fill
            draw.rounded_rectangle([btn_x1, btn_y1, btn_x1 + btn_w, btn_y1 + btn_h], radius=16, fill=COLOR_PAPER_WHITE, outline=COLOR_INK_BLACK, width=2)
            draw.text((width // 2, btn_y1 + btn_h // 2), "crowdwisdomtrading.com", fill=COLOR_HOT_RED, font=font_url, anchor="mm")

            # Bottom institutional notice
            draw.text((width // 2, height - 160), "INSTITUTIONAL INSIGHT // RETAIL CLARITY", fill=COLOR_HALFTONE_GRAY, font=font_meta, anchor="mm")

            if zoom != 1.0:
                crop_w = int(width / zoom)
                crop_h = int(height / zoom)
                x0 = (width - crop_w) // 2
                y0 = (height - crop_h) // 2
                frame = frame.crop((x0, y0, x0 + crop_w, y0 + crop_h)).resize((width, height), Image.Resampling.BILINEAR)

            frame.save(temp_dir / f"frame_{frame_idx:04d}.png", "PNG")

        cmd = [
            self.ffmpeg.ffmpeg_path, "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Beat 8 CTA rendered: %s", output_path)
        return output_path

    # -------------------------------------------------------------------------
    # DISPATCHER
    # -------------------------------------------------------------------------

    def render_beat(self, beat_id: int, output_path: Path, duration: Optional[float] = None, fps: int = 30) -> Path:
        """Dispatcher to render any Phase 9 beat by its ID."""
        default_durations = {
            1: 4.0,
            2: 5.0,
            3: 4.0,
            4: 6.0,
            5: 8.0,
            6: 7.0,
            7: 6.0,
            8: 5.0,
        }
        dur = duration or default_durations.get(beat_id, 4.0)

        dispatch_table = {
            1: self.render_beat1_hook,
            2: self.render_beat2_montage,
            3: self.render_beat3_problem_typography,
            4: self.render_beat4_crowd_signal,
            5: self.render_beat5_data_proof,
            6: self.render_beat6_signal_resolve,
            7: self.render_beat7_product_radar,
            8: self.render_beat8_minimal_cta,
        }
        fn = dispatch_table.get(beat_id)
        if not fn:
            raise ValueError(f"Unknown beat ID: {beat_id}. Expected 1-8.")
        return fn(output_path=output_path, duration=dur, fps=fps)

    def render_all_beats(self, output_dir: Path, storyboard: Optional[Dict[str, Any]] = None, fps: int = 30) -> List[Path]:
        """Render all 8 Phase 9 beats to separate MP4 files."""
        output_dir.mkdir(parents=True, exist_ok=True)
        beats = []
        if storyboard:
            beats = storyboard.get("beats", storyboard.get("scenes", []))

        beat_clips: List[Path] = []
        for b_id in range(1, 9):
            dur = None
            if beats and len(beats) >= b_id:
                dur = float(beats[b_id - 1].get("duration", 4.0))
            clip_path = output_dir / f"scene_{b_id:02d}.mp4"
            self.render_beat(beat_id=b_id, output_path=clip_path, duration=dur, fps=fps)
            beat_clips.append(clip_path)

        return beat_clips
