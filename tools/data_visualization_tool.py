"""Editorial Data Visualization & Motion Graphics Tool for CrowdWisdom Video Ads.

Adheres strictly to modern visual journalism / editorial documentary design principles:
- Restrained 2D editorial animations (warm off-white, charcoal, muted red, subtle gold accent).
- Clean typography and grid-aligned editorial layouts.
- Data introduced strictly as narrative evidence (1,482,930 inputs, 68.4% accuracy, 14.6h lead time).
- No neon effects, no 3D particle explosions, no cheesy fintech dashboards.

Compatible with Python 3.10.
"""

import json
import logging
import math
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from tools.ffmpeg_tool import FFmpegTool

logger = logging.getLogger(__name__)

# Editorial Visual Journalism Color Palette
BG_DARK = (11, 15, 20)           # Deep charcoal / near black
CARD_BG = (22, 28, 38)           # Slate charcoal card
WARM_WHITE = (247, 250, 252)     # Off-white primary text
MUTED_GRAY = (148, 163, 184)     # Secondary slate label
MUTED_RED = (229, 62, 62)        # Warning / baseline / noise
ACCENT_GOLD = (214, 158, 46)     # CrowdWisdom consensus / conviction
CYAN_ACCENT = (49, 151, 149)     # Verified lead time
DIVIDER_LINE = (45, 55, 72)      # Subtle editorial rule


class DataVisualizationTool:
    """Renders 1080x1920 editorial documentary motion graphics and data evidence."""

    def __init__(self, ffmpeg_tool: Optional[FFmpegTool] = None):
        self.ffmpeg = ffmpeg_tool or FFmpegTool()

    def _get_font(self, size: int, bold: bool = False) -> ImageFont.ImageFont:
        """Load clean editorial sans-serif font (Segoe UI or Arial) with fallback."""
        candidates = ["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
        for font_name in candidates:
            win_path = Path(f"C:/Windows/Fonts/{font_name}")
            if win_path.exists():
                try:
                    return ImageFont.truetype(str(win_path), size)
                except Exception:
                    pass
        return ImageFont.load_default()

    def render_noise_to_signal_animation(
        self,
        output_path: Path,
        duration: float = 8.0,
        fps: int = 30,
        width: int = 1080,
        height: int = 1920,
    ) -> Path:
        """Scene 4: Thousands of chaotic trader signals aligning into a directional conviction vector,

        culminating in the verified figure: 1,482,930 trader inputs.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_scene4_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)
        import random
        rng = random.Random(2026)

        # 300 editorial signal vectors
        signals = []
        for i in range(300):
            signals.append({
                "x": rng.uniform(120, width - 120),
                "y": rng.uniform(400, 1150),
                "random_angle": rng.uniform(-math.pi, math.pi),
                "target_angle": -math.pi / 4.0,  # Upward-right bullish consensus (45 deg)
                "length": rng.uniform(18, 38),
                "speed": rng.uniform(0.7, 1.3),
            })

        font_counter = self._get_font(72, bold=True)
        font_label = self._get_font(32, bold=True)
        font_sub = self._get_font(26, bold=False)
        font_meta = self._get_font(20, bold=False)

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)  # 0.0 to 1.0
            frame_img = Image.new("RGB", (width, height), BG_DARK)
            draw = ImageDraw.Draw(frame_img)

            # 1. Subtle Editorial Grid
            for gy in range(200, 1700, 120):
                draw.line([(80, gy), (width - 80, gy)], fill=(18, 24, 32), width=1)
            for gx in range(120, width, 160):
                draw.line([(gx, 200), (gx, 1600)], fill=(18, 24, 32), width=1)

            # 2. Header metadata
            draw.text((80, 140), "EDITORIAL INVESTIGATION // CROWD SENTIMENT", fill=MUTED_GRAY, font=font_meta)
            draw.line([(80, 175), (width - 80, 175)], fill=DIVIDER_LINE, width=2)
            draw.text((80, 210), "FROM DISPERSED NOISE TO COLLECTIVE SIGNAL", fill=WARM_WHITE, font=font_label)

            # 3. Animate signal vectors:
            # First 35%: chaotic, random Brownian motion
            # 35% - 75%: gradual alignment to target angle and gold color
            # 75% - 100%: fully aligned directional vector stream
            alignment_progress = max(0.0, min(1.0, (t - 0.30) / 0.35))

            for s in signals:
                cur_angle = s["random_angle"] * (1.0 - alignment_progress) + s["target_angle"] * alignment_progress
                # Color transition from chaotic muted red/gray to confident gold
                if alignment_progress > 0.4:
                    prog = (alignment_progress - 0.4) / 0.6
                    r = int(MUTED_GRAY[0] * (1 - prog) + ACCENT_GOLD[0] * prog)
                    g = int(MUTED_GRAY[1] * (1 - prog) + ACCENT_GOLD[1] * prog)
                    b = int(MUTED_GRAY[2] * (1 - prog) + ACCENT_GOLD[2] * prog)
                    vec_color = (r, g, b)
                else:
                    vec_color = MUTED_RED if s["x"] % 3 == 0 else MUTED_GRAY

                # Subtle drift
                drift = math.sin(t * 10 * s["speed"] + s["x"]) * 3
                x1 = s["x"] + drift
                y1 = s["y"] + drift
                x2 = x1 + math.cos(cur_angle) * s["length"]
                y2 = y1 + math.sin(cur_angle) * s["length"]

                draw.line([(x1, y1), (x2, y2)], fill=vec_color, width=2)
                # Arrowhead tip
                draw.ellipse([x2 - 2, y2 - 2, x2 + 2, y2 + 2], fill=vec_color)

            # 4. Editorial Evidence Card (bottom half)
            card_top = 1250
            draw.rectangle([80, card_top, width - 80, card_top + 340], fill=CARD_BG, outline=DIVIDER_LINE, width=2)

            # Animate input counter starting at 50% through duration
            counter_prog = max(0.0, min(1.0, (t - 0.45) / 0.40))
            # Smooth ease-out
            eased_counter = 1.0 - math.pow(1.0 - counter_prog, 3)
            current_inputs = int(eased_counter * 1482930)

            # Formatted number: 1,482,930
            counter_str = f"{current_inputs:,}"
            draw.text((120, card_top + 40), "PROPRIETARY BENCHMARK DATASET", fill=MUTED_GRAY, font=font_meta)
            draw.text((120, card_top + 80), counter_str, fill=ACCENT_GOLD if counter_prog >= 0.95 else WARM_WHITE, font=font_counter)
            draw.text((120, card_top + 180), "TRADER INPUTS AGGREGATED IN REAL-TIME", fill=WARM_WHITE, font=font_label)
            draw.text((120, card_top + 235), "Noise filtered via Bayesian consensus weighting across 10 asset classes.", fill=MUTED_GRAY, font=font_sub)

            # Save frame
            frame_path = temp_dir / f"frame_{frame_idx:04d}.png"
            frame_img.save(frame_path, "PNG")

        # Encode frames with FFmpeg
        cmd = [
            self.ffmpeg.ffmpeg_path,
            "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        # Cleanup frames
        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Noise-to-Signal editorial animation rendered: %s", output_path)
        return output_path

    def render_editorial_proprietary_data_card(
        self,
        output_path: Path,
        duration: float = 7.0,
        fps: int = 30,
        width: int = 1080,
        height: int = 1920,
    ) -> Path:
        """Scene 5: Editorial data visualization showing verified project data:

        - 68.4% directional accuracy benchmark (vs 41.2% retail baseline)
        - 14.6-hour early warning lead-time waveform timeline
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_dir = output_path.parent / "temp_scene5_frames"
        temp_dir.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration * fps)

        font_large = self._get_font(84, bold=True)
        font_title = self._get_font(38, bold=True)
        font_body = self._get_font(26, bold=False)
        font_meta = self._get_font(20, bold=False)

        for frame_idx in range(total_frames):
            t = frame_idx / float(total_frames)
            frame_img = Image.new("RGB", (width, height), BG_DARK)
            draw = ImageDraw.Draw(frame_img)

            # Header
            draw.text((80, 140), "CROWDWISDOM TRADING // VERIFIED BENCHMARK", fill=MUTED_GRAY, font=font_meta)
            draw.line([(80, 175), (width - 80, 175)], fill=DIVIDER_LINE, width=2)
            draw.text((80, 210), "PROPRIETARY PERFORMANCE METRICS", fill=WARM_WHITE, font=font_title)

            # Progress eases
            ease_accuracy = max(0.0, min(1.0, t / 0.35))
            ease_timeline = max(0.0, min(1.0, (t - 0.35) / 0.45))

            # --- CARD 1: 68.4% Directional Accuracy ---
            c1_top = 300
            c1_h = 580
            draw.rectangle([80, c1_top, width - 80, c1_top + c1_h], fill=CARD_BG, outline=DIVIDER_LINE, width=2)
            draw.text((120, c1_top + 40), "METRIC 01: PREDICTIVE CONVICTION", fill=MUTED_GRAY, font=font_meta)

            disp_acc = f"{68.4 * ease_accuracy:.1f}%"
            draw.text((120, c1_top + 80), disp_acc, fill=ACCENT_GOLD, font=font_large)
            draw.text((120, c1_top + 190), "DIRECTIONAL ACCURACY", fill=WARM_WHITE, font=font_title)
            draw.text((120, c1_top + 245), "Statistically validated across multi-year trading log benchmarks.", fill=MUTED_GRAY, font=font_body)

            # Comparative Bar Chart
            bar_y = c1_top + 330
            # Retail baseline
            draw.text((120, bar_y), "Retail Baseline (41.2%)", fill=MUTED_GRAY, font=font_meta)
            draw.rectangle([120, bar_y + 30, 120 + int(41.2 * 8 * ease_accuracy), bar_y + 55], fill=MUTED_RED)
            # CrowdWisdom
            draw.text((120, bar_y + 80), "CrowdWisdom Consensus (68.4%)", fill=WARM_WHITE, font=font_meta)
            draw.rectangle([120, bar_y + 110, 120 + int(68.4 * 8 * ease_accuracy), bar_y + 135], fill=ACCENT_GOLD)

            # --- CARD 2: 14.6-Hour Early Warning Waveform ---
            c2_top = 940
            c2_h = 680
            draw.rectangle([80, c2_top, width - 80, c2_top + c2_h], fill=CARD_BG, outline=DIVIDER_LINE, width=2)
            draw.text((120, c2_top + 40), "METRIC 02: TEMPORAL ADVANTAGE", fill=MUTED_GRAY, font=font_meta)

            disp_lead = f"{14.6 * ease_timeline:.1f} HOURS"
            draw.text((120, c2_top + 80), disp_lead, fill=CYAN_ACCENT, font=font_large)
            draw.text((120, c2_top + 190), "SENTIMENT EARLY-WARNING LEAD TIME", fill=WARM_WHITE, font=font_title)
            draw.text((120, c2_top + 245), "Crowd conviction crystallizes hours before market price inflection.", fill=MUTED_GRAY, font=font_body)

            # Timeline Waveform visualization
            wave_y = c2_top + 460
            draw.line([(120, wave_y), (width - 120, wave_y)], fill=DIVIDER_LINE, width=2)

            # Waveform points
            steps = 80
            pts_sentiment = []
            pts_price = []
            for s in range(steps):
                wx = 120 + s * ((width - 240) / float(steps))
                prog_x = s / float(steps)

                # Sentiment wave (peaks early at prog_x = 0.35)
                amp1 = math.exp(-math.pow((prog_x - 0.35) / 0.18, 2)) * 90 * ease_timeline
                sy = wave_y - amp1
                pts_sentiment.append((wx, sy))

                # Price action wave (inflects late at prog_x = 0.70 - exactly 14.6h later)
                amp2 = math.exp(-math.pow((prog_x - 0.70) / 0.18, 2)) * 75 * ease_timeline
                py = wave_y - amp2
                pts_price.append((wx, py))

            if len(pts_sentiment) > 1:
                draw.line(pts_sentiment, fill=CYAN_ACCENT, width=4)
                draw.line(pts_price, fill=MUTED_GRAY, width=2)

            # Lead Marker
            lead_x1 = 120 + int(0.35 * (width - 240))
            lead_x2 = 120 + int(0.70 * (width - 240))
            draw.line([(lead_x1, wave_y - 110), (lead_x2, wave_y - 110)], fill=ACCENT_GOLD, width=3)
            draw.line([(lead_x1, wave_y - 120), (lead_x1, wave_y - 100)], fill=ACCENT_GOLD, width=3)
            draw.line([(lead_x2, wave_y - 120), (lead_x2, wave_y - 100)], fill=ACCENT_GOLD, width=3)
            draw.text((lead_x1 + 45, wave_y - 150), "+14.6h EARLY LEAD", fill=ACCENT_GOLD, font=font_meta)

            # Labels for waveforms
            draw.text((120, c2_top + 575), "- Crowd Sentiment Lead", fill=CYAN_ACCENT, font=font_meta)
            draw.text((width / 2 + 30, c2_top + 575), "- Subsequent Market Price Move", fill=MUTED_GRAY, font=font_meta)

            # Save frame
            frame_path = temp_dir / f"frame_{frame_idx:04d}.png"
            frame_img.save(frame_path, "PNG")

        # Encode frames
        cmd = [
            self.ffmpeg.ffmpeg_path,
            "-y",
            "-framerate", str(fps),
            "-i", str(temp_dir / "frame_%04d.png"),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

        for f in temp_dir.glob("*.png"):
            f.unlink(missing_ok=True)
        temp_dir.rmdir()

        logger.info("Editorial proprietary data card rendered: %s", output_path)
        return output_path

    def render_minimal_brand_cta(
        self,
        output_path: Path,
        duration: float = 4.0,
        fps: int = 30,
        width: int = 1080,
        height: int = 1920,
    ) -> Path:
        """Scene 8: Minimal editorial brand CTA card."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_img_path = output_path.parent / "cta_temp_card.png"

        img = Image.new("RGB", (width, height), BG_DARK)
        draw = ImageDraw.Draw(img)

        font_brand = self._get_font(52, bold=True)
        font_tagline = self._get_font(34, bold=False)
        font_url = self._get_font(30, bold=True)
        font_meta = self._get_font(20, bold=False)

        # Subtle fine linen border
        draw.rectangle([80, 80, width - 80, height - 80], outline=DIVIDER_LINE, width=2)

        cy = height / 2 - 80
        draw.text((width / 2 - 240, cy - 80), "CROWDWISDOM TRADING", fill=WARM_WHITE, font=font_brand)
        # Gold accent line
        draw.line([(width / 2 - 120, cy - 10), (width / 2 + 120, cy - 10)], fill=ACCENT_GOLD, width=3)
        draw.text((width / 2 - 235, cy + 30), "\"See the signal inside the noise.\"", fill=MUTED_GRAY, font=font_tagline)

        # Action URL
        draw.rectangle([width / 2 - 220, cy + 140, width / 2 + 220, cy + 220], fill=CARD_BG, outline=ACCENT_GOLD, width=2)
        draw.text((width / 2 - 170, cy + 162), "crowdwisdomtrading.com", fill=ACCENT_GOLD, font=font_url)

        draw.text((width / 2 - 160, height - 160), "INSTITUTIONAL INSIGHT // RETAIL CLARITY", fill=DIVIDER_LINE, font=font_meta)

        img.save(temp_img_path, "PNG")

        # Create motion clip (gentle breathing)
        self.ffmpeg.create_cinematic_motion_clip(
            image_path=temp_img_path,
            output_path=output_path,
            duration=duration,
            motion="subtle_drift",
            width=width,
            height=height,
            fps=fps,
        )

        temp_img_path.unlink(missing_ok=True)
        return output_path
