"""scripts/generate_overlays.py

Generates transparent 1080x1920 PNG overlays for each of the 8 beats
incorporating authentic company art-direction design language:
- Archival Tan cards with soft drop shadows
- Ink Black condensed typography (Impact / Arial Black)
- Hot Red signature underlines and warning brackets
- Monospace technical annotations (Consolas)
- Rough white keylines and crosshairs
- Verified numbers: 1,482,930 | 68.4% | 14.6 HOURS
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OVERLAY_DIR = Path("outputs/videos/overlays_p14")
OVERLAY_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920

# Colors
C_TAN = (201, 187, 156, 255)
C_CARD_BG = (242, 238, 228, 250)
C_INK = (26, 26, 26, 255)
C_RED = (214, 46, 31, 255)
C_MUSTARD = (217, 164, 65, 255)
C_WHITE = (248, 246, 240, 255)
C_HALFTONE = (140, 140, 140, 180)
C_DARK_SHADOW = (0, 0, 0, 90)


def get_font(size: int, font_type: str = "bold"):
    candidates = []
    if font_type == "headline":
        candidates = ["impact.ttf", "arialbd.ttf", "segoeuib.ttf"]
    elif font_type == "mono":
        candidates = ["consola.ttf", "cour.ttf", "segoeui.ttf"]
    elif font_type == "bold":
        candidates = ["arialbd.ttf", "segoeuib.ttf"]
    else:
        candidates = ["arial.ttf", "segoeui.ttf"]

    for name in candidates:
        p = Path(f"C:/Windows/Fonts/{name}")
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def draw_keyline_frame(draw: ImageDraw.ImageDraw, margin: int = 40):
    """Draw thin rough white keyline frame with corner crosshairs."""
    # Outer frame
    draw.rectangle([margin, margin, W - margin, H - margin], outline=C_WHITE, width=2)
    # Corner crosshairs
    ch = 18
    corners = [
        (margin, margin),
        (W - margin, margin),
        (margin, H - margin),
        (W - margin, H - margin)
    ]
    for cx, cy in corners:
        draw.line([(cx - ch, cy), (cx + ch, cy)], fill=C_RED, width=3)
        draw.line([(cx, cy - ch), (cx, cy + ch)], fill=C_RED, width=3)


def draw_card(img: Image.Image, box: tuple, bg_color=C_CARD_BG, outline=C_TAN, shadow: bool = True):
    """Draw paper card with drop shadow."""
    x1, y1, x2, y2 = box
    if shadow:
        shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow_layer)
        s_draw.rectangle([x1 + 8, y1 + 10, x2 + 8, y2 + 10], fill=(0, 0, 0, 80))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(8))
        img.alpha_composite(shadow_layer)

    draw = ImageDraw.Draw(img)
    draw.rectangle(box, fill=bg_color, outline=outline, width=3)
    return draw


def generate_beat_01():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_keyline_frame(draw)

    # Top time badge
    badge_box = (80, 100, 360, 170)
    draw_card(img, badge_box, bg_color=C_CARD_BG, outline=C_RED)
    d = ImageDraw.Draw(img)
    f_badge = get_font(34, "headline")
    d.ellipse([105, 125, 125, 145], fill=C_RED)
    d.text((140, 118), "2:17 AM", fill=C_INK, font=f_badge)

    # Monospace meta
    f_mono = get_font(20, "mono")
    d.text((80, 190), "SESSION: GLOBAL FX / ASIA OPEN  •  02:17:04 EST", fill=C_WHITE, font=f_mono)

    # Lower hero card
    card_box = (70, H - 480, W - 70, H - 240)
    draw_card(img, card_box, bg_color=C_CARD_BG, outline=C_TAN)
    d = ImageDraw.Draw(img)

    f_head = get_font(52, "headline")
    f_sub = get_font(24, "mono")
    d.text((105, H - 440), "THE MARKET NEVER SLEEPS.", fill=C_INK, font=f_head)
    # Red accent rule
    d.rectangle([105, H - 370, 480, H - 364], fill=C_RED)
    d.text((105, H - 340), "WHILE TRADERS REST, GLOBAL CAPITAL IS MOVING.", fill=C_INK, font=f_sub)
    d.text((105, H - 300), "STATUS: UNFILTERED DATA INCOMING", fill=C_RED, font=f_mono)

    out_path = OVERLAY_DIR / "overlay_beat_01.png"
    img.save(out_path)
    print(f"Generated {out_path.name}")


def generate_beat_02():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_keyline_frame(draw)

    # Warning headline banner
    banner_box = (70, 120, W - 70, 240)
    draw_card(img, banner_box, bg_color=C_RED, outline=C_WHITE)
    d = ImageDraw.Draw(img)
    f_head = get_font(50, "headline")
    d.text((100, 150), "TOO MUCH INFORMATION.", fill=C_WHITE, font=f_head)

    # Monospace tag
    f_mono = get_font(22, "mono")
    d.text((75, 260), "INGESTION RATE: 14,800 HEADLINES / MINUTE", fill=C_MUSTARD, font=f_mono)

    # Screen center warning brackets
    cx, cy = W // 2, H // 2 - 40
    bw, bh = 420, 240
    d.line([(cx - bw//2, cy - bh//2), (cx - bw//2 + 50, cy - bh//2)], fill=C_RED, width=4)
    d.line([(cx - bw//2, cy - bh//2), (cx - bw//2, cy - bh//2 + 50)], fill=C_RED, width=4)
    d.line([(cx + bw//2, cy + bh//2), (cx + bw//2 - 50, cy + bh//2)], fill=C_RED, width=4)
    d.line([(cx + bw//2, cy + bh//2), (cx + bw//2, cy + bh//2 - 50)], fill=C_RED, width=4)

    # Center label inside brackets
    f_alert = get_font(32, "headline")
    d.text((cx - 160, cy - 20), "ALERT: NOISE SATURATION", fill=C_WHITE, font=f_alert)

    # Bottom ticker tape
    draw.rectangle([0, H - 180, W, H - 90], fill=(15, 15, 15, 230))
    draw.line([(0, H - 180), (W, H - 180)], fill=C_RED, width=3)
    f_tick = get_font(22, "mono")
    d.text((30, H - 150), "SPY -1.4% ▼  |  BTC +4.8% ▲  |  FED POLICY LEAK  |  VIX +18% ▲  |  TECH MISS", fill=C_WHITE, font=f_tick)

    out_path = OVERLAY_DIR / "overlay_beat_02.png"
    img.save(out_path)
    print(f"Generated {out_path.name}")


def generate_beat_03():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_keyline_frame(draw)

    # Center realization card
    card_box = (70, H // 2 - 160, W - 70, H // 2 + 140)
    draw_card(img, card_box, bg_color=C_CARD_BG, outline=C_TAN)
    d = ImageDraw.Draw(img)

    f_head = get_font(56, "headline")
    f_sub = get_font(22, "mono")

    d.text((105, H // 2 - 120), "NOT ENOUGH SIGNAL.", fill=C_INK, font=f_head)

    # Signature Hot Red hand-drawn style underline under "SIGNAL."
    d.line([(105, H // 2 - 45), (600, H // 2 - 45)], fill=C_RED, width=7)
    d.line([(110, H // 2 - 40), (590, H // 2 - 40)], fill=C_RED, width=4)

    d.text((105, H // 2 - 10), "SIGNALS ARE BURIED INSIDE THE NOISE.", fill=C_INK, font=f_sub)
    d.text((105, H // 2 + 35), "TRUE INFORMATION EFFICIENCY: < 0.2%", fill=C_RED, font=f_sub)

    # Top indicator
    f_mono = get_font(20, "mono")
    d.text((80, 120), "DATA STATUS: STATIC OVERWHELM", fill=C_WHITE, font=f_mono)

    out_path = OVERLAY_DIR / "overlay_beat_03.png"
    img.save(out_path)
    print(f"Generated {out_path.name}")


def generate_beat_04():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_keyline_frame(draw)

    # Top category badge
    top_badge = (70, 100, W - 70, 170)
    draw_card(img, top_badge, bg_color=C_RED, outline=C_WHITE)
    d = ImageDraw.Draw(img)
    f_b = get_font(24, "bold")
    d.text((100, 122), "CROWD WISDOM COLLECTIVE INTELLIGENCE", fill=C_WHITE, font=f_b)

    # Giant Stat Hero Card
    card_box = (60, H // 2 - 220, W - 60, H // 2 + 180)
    draw_card(img, card_box, bg_color=C_CARD_BG, outline=C_TAN)
    d = ImageDraw.Draw(img)

    f_giant = get_font(92, "headline")
    f_sub = get_font(34, "headline")
    f_mono = get_font(22, "mono")

    # The verified number: 1,482,930
    d.text((95, H // 2 - 190), "1,482,930", fill=C_INK, font=f_giant)

    # Pill badge for TRADER INPUTS
    d.rectangle([95, H // 2 - 80, 390, H // 2 - 25], fill=C_RED)
    d.text((115, H // 2 - 75), "TRADER INPUTS", fill=C_WHITE, font=f_sub)

    d.rectangle([95, H // 2 + 5, W - 95, H // 2 + 8], fill=C_TAN)
    d.text((95, H // 2 + 25), "UNIFIED REAL-TIME MARKET CONVERGENCE", fill=C_INK, font=f_sub)
    d.text((95, H // 2 + 80), "SOURCE: VERIFIED CROWDWISDOM GLOBAL NETWORK", fill=C_HALFTONE, font=f_mono)

    out_path = OVERLAY_DIR / "overlay_beat_04.png"
    img.save(out_path)
    print(f"Generated {out_path.name}")


def generate_beat_05():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_keyline_frame(draw)

    # Top Stamp
    stamp_box = (70, 100, 520, 160)
    draw_card(img, stamp_box, bg_color=C_CARD_BG, outline=C_RED)
    d = ImageDraw.Draw(img)
    f_stamp = get_font(24, "mono")
    d.text((95, 120), "VERIFIED PERFORMANCE DATA", fill=C_RED, font=f_stamp)

    # Card 1: 68.4% Directional Accuracy
    card1_box = (60, H // 2 - 280, W - 60, H // 2 - 40)
    draw_card(img, card1_box, bg_color=C_CARD_BG, outline=C_TAN)
    d = ImageDraw.Draw(img)

    f_giant = get_font(88, "headline")
    f_label = get_font(32, "headline")
    f_mono = get_font(22, "mono")

    d.text((95, H // 2 - 260), "68.4%", fill=C_INK, font=f_giant)
    d.rectangle([95, H // 2 - 160, 480, H // 2 - 110], fill=C_RED)
    d.text((115, H // 2 - 155), "DIRECTIONAL ACCURACY", fill=C_WHITE, font=f_label)
    d.text((95, H // 2 - 95), "SYSTEMATIC OUTPERFORMANCE VS BASELINE", fill=C_HALFTONE, font=f_mono)

    # Card 2: 14.6 HOURS Early Warning Lead
    card2_box = (60, H // 2 + 20, W - 60, H // 2 + 260)
    draw_card(img, card2_box, bg_color=C_CARD_BG, outline=C_TAN)
    d = ImageDraw.Draw(img)

    d.text((95, H // 2 + 40), "14.6 HOURS", fill=C_INK, font=f_giant)
    d.rectangle([95, H // 2 + 140, 480, H // 2 + 190], fill=C_MUSTARD)
    d.text((115, H // 2 + 145), "EARLY WARNING LEAD", fill=C_INK, font=f_label)
    d.text((95, H // 2 + 205), "PREDICTIVE SENTIMENT PRECEDES PRICE MOVE", fill=C_HALFTONE, font=f_mono)

    out_path = OVERLAY_DIR / "overlay_beat_05.png"
    img.save(out_path)
    print(f"Generated {out_path.name}")


def generate_beat_06():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_keyline_frame(draw)

    # Center Payoff Card
    card_box = (60, H // 2 - 200, W - 60, H // 2 + 150)
    draw_card(img, card_box, bg_color=C_CARD_BG, outline=C_RED)
    d = ImageDraw.Draw(img)

    f_head = get_font(48, "headline")
    f_badge = get_font(28, "headline")
    f_body = get_font(24, "mono")

    d.text((95, H // 2 - 160), "NOISE → SIGNAL → ACTION", fill=C_INK, font=f_head)
    d.rectangle([95, H // 2 - 90, 440, H // 2 - 40], fill=C_RED)
    d.text((115, H // 2 - 85), "EXECUTION ADVANTAGE", fill=C_WHITE, font=f_badge)

    d.rectangle([95, H // 2 - 15, W - 95, H // 2 - 12], fill=C_TAN)
    d.text((95, H // 2 + 10), "ACT BEFORE THE BREAKOUT BECOMES OBVIOUS.", fill=C_INK, font=f_body)
    d.text((95, H // 2 + 50), "SIGNAL CONVICTION: CONFIRMED", fill=C_RED, font=f_body)

    out_path = OVERLAY_DIR / "overlay_beat_06.png"
    img.save(out_path)
    print(f"Generated {out_path.name}")


def generate_beat_07():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_keyline_frame(draw)

    # Top Platform Header
    top_box = (60, 100, W - 60, 200)
    draw_card(img, top_box, bg_color=C_CARD_BG, outline=C_TAN)
    d = ImageDraw.Draw(img)
    f_head = get_font(42, "headline")
    d.text((90, 130), "CROWDWISDOM INTELLIGENCE PLATFORM", fill=C_INK, font=f_head)

    # Center Polar Radar Display
    cx, cy = W // 2, H // 2 - 30
    radius = 260
    # Radar concentric circles
    for r in [60, 120, 180, 240]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=C_HALFTONE, width=2)
    # Cross axes
    draw.line([(cx - radius - 20, cy), (cx + radius + 20, cy)], fill=C_TAN, width=2)
    draw.line([(cx, cy - radius - 20), (cx, cy + radius + 20)], fill=C_TAN, width=2)
    # Target blips
    blips = [(cx + 90, cy - 80), (cx - 120, cy + 50), (cx + 140, cy + 90)]
    for bx, by in blips:
        draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=C_RED, outline=C_WHITE, width=2)
        draw.line([(bx, by), (bx + 35, by - 25)], fill=C_RED, width=2)
        draw.rectangle([bx + 35, by - 35, bx + 110, by - 15], fill=C_CARD_BG)
        d.text((bx + 40, by - 32), "+ALPHA", fill=C_RED, font=get_font(16, "mono"))

    # Lower Product Badge
    bot_box = (70, H - 420, W - 70, H - 240)
    draw_card(img, bot_box, bg_color=C_CARD_BG, outline=C_RED)
    d = ImageDraw.Draw(img)
    f_bot = get_font(36, "headline")
    f_mono = get_font(22, "mono")
    d.text((100, H - 390), "REAL-TIME ALPHA SIGNALS", fill=C_INK, font=f_bot)
    d.rectangle([100, H - 335, 420, H - 330], fill=C_RED)
    d.text((100, H - 310), "CROSS-ASSET SENTIMENT INTELLIGENCE", fill=C_HALFTONE, font=f_mono)

    out_path = OVERLAY_DIR / "overlay_beat_07.png"
    img.save(out_path)
    print(f"Generated {out_path.name}")


def generate_beat_08():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_keyline_frame(draw)

    # Master CTA Card in center
    card_box = (60, H // 2 - 240, W - 60, H // 2 + 220)
    draw_card(img, card_box, bg_color=C_CARD_BG, outline=C_TAN)
    d = ImageDraw.Draw(img)

    f_brand = get_font(56, "headline")
    f_tag = get_font(32, "headline")
    f_domain = get_font(38, "headline")
    f_copy = get_font(18, "mono")

    # Brand Title
    d.text((105, H // 2 - 200), "CROWDWISDOM TRADING", fill=C_INK, font=f_brand)
    # Red accent line
    d.rectangle([105, H // 2 - 125, W - 105, H // 2 - 120], fill=C_RED)

    # Tagline
    d.text((105, H // 2 - 95), "SEE THE SIGNAL INSIDE THE NOISE.", fill=C_INK, font=f_tag)

    # Domain button
    btn_box = (105, H // 2 - 20, W - 105, H // 2 + 70)
    d.rectangle(btn_box, fill=C_RED)
    d.text((160, H // 2 + 3), "crowdwisdomtrading.com", fill=C_WHITE, font=f_domain)

    # Editorial note
    d.text((105, H // 2 + 105), "REQUEST ALPHA ACCESS  •  VERIFIED TRADER INTELLIGENCE", fill=C_HALFTONE, font=f_copy)

    out_path = OVERLAY_DIR / "overlay_beat_08.png"
    img.save(out_path)
    print(f"Generated {out_path.name}")


def main():
    generate_beat_01()
    generate_beat_02()
    generate_beat_03()
    generate_beat_04()
    generate_beat_05()
    generate_beat_06()
    generate_beat_07()
    generate_beat_08()
    print("All 8 beat overlays generated successfully.")


if __name__ == "__main__":
    main()
