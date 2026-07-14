"""
Ultra-Modern V100 Visual Compositor (1080x1350).
Synthesizes cutting-edge 2026/2027 design aesthetics:
- Radial Neon Mesh Glow Backgrounds (`#00E5CC` & `#FF4B4B` ambient light blobs)
- Multi-Layered Frosted Glassmorphism Cards (`backdrop-filter`, inner highlights, drop shadows)
- Mac OS Code Terminal Windows (`[🔴] [🟡] [🟢]` traffic light header dots)
- Glowing Pill Eyebrow Badges & Widescreen Split Comparison Matrices
- High-Fidelity Dual Export: Standalone HTML (`slide_01.html`) + Razor-Sharp Vector PNG (`slide_01.png`)
"""
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
from .topic_dna import get_topic_dna
from .svg_flow_engine import SVGFlowEngine


class NextGenRenderer:
    """
    V100 Ultra-Modern Renderer producing dual HTML + PNG slide suites.
    """

    ARCHETYPES = {
        "cyber_dark": {"background": "#090A0F", "primary": "#00E5CC", "accent": "#FF4B4B", "text": "#FFFFFF", "subtext": "#B0B0B0", "card_bg": "rgba(18, 20, 30, 0.85)"},
        "minimalist_white": {"background": "#FAFAFA", "primary": "#2563EB", "accent": "#DC2626", "text": "#18181B", "subtext": "#52525B", "card_bg": "rgba(244, 244, 246, 0.9)"},
        "monokai_code": {"background": "#141416", "primary": "#A6E22E", "accent": "#F92672", "text": "#F8F8F2", "subtext": "#94949C", "card_bg": "rgba(32, 34, 42, 0.85)"},
        "brutalist_swiss": {"background": "#FACC15", "primary": "#000000", "accent": "#DC2626", "text": "#000000", "subtext": "#27272A", "card_bg": "#FFFFFF"},
        "infrastructure_blue": {"background": "#080C14", "primary": "#38BDF8", "accent": "#F59E0B", "text": "#F9FAFB", "subtext": "#9CA3AF", "card_bg": "rgba(16, 24, 38, 0.85)"}
    }

    def __init__(self):
        self.has_convert = shutil.which("convert") is not None

    def _clean_txt(self, text: Any) -> str:
        if not text:
            return ""
        cleaned = re.sub(r'<[^>]+>', '', str(text))
        cleaned = cleaned.replace('"', "'").replace('`', "'").replace('$', "").strip()
        return cleaned

    def _get_palette(self, topic_dna: Dict[str, Any], archetype_override: str = "") -> Dict[str, str]:
        if archetype_override and archetype_override in self.ARCHETYPES:
            return self.ARCHETYPES[archetype_override]
        cat = topic_dna.get("category", "ai_engineering")
        if cat == "infrastructure":
            return self.ARCHETYPES["infrastructure_blue"]
        elif cat == "software_engineering":
            return self.ARCHETYPES["monokai_code"]
        return self.ARCHETYPES["cyber_dark"]

    def render(self, slides: List[Dict[str, Any]], topic: str, output_dir: Path,
               topic_dna: Optional[Dict[str, Any]] = None, archetype: str = "") -> List[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        if topic_dna is None:
            topic_dna = get_topic_dna(topic)

        colors = self._get_palette(topic_dna, archetype)
        total_slides = len(slides)
        rendered_paths = []
        png_paths = []

        png_dir = output_dir / "png"
        if self.has_convert:
            png_dir.mkdir(parents=True, exist_ok=True)

        for idx, slide in enumerate(slides, 1):
            file_path = output_dir / f"slide_{idx:02d}.html"
            html_content = self._render_slide_html(slide, idx, total_slides, colors)
            file_path.write_text(html_content, encoding="utf-8")
            rendered_paths.append(file_path)

            if self.has_convert:
                png_path = output_dir / f"slide_{idx:02d}.png"
                self._render_slide_png(slide, idx, total_slides, colors, png_path)
                if png_path.exists():
                    png_paths.append(png_path)
                    try:
                        shutil.copy2(png_path, png_dir / f"slide_{idx:02d}.png")
                    except Exception:
                        pass

        package_file = output_dir / "carousel_data.json"
        package_data = {
            "topic": topic,
            "version": "v100.0_ultra_modern_masterpiece",
            "topic_dna": topic_dna,
            "archetype_used": archetype or topic_dna.get("category", "cyber_dark"),
            "slides": slides,
            "slide_files": [p.name for p in rendered_paths],
            "png_files": [p.name for p in png_paths]
        }
        package_file.write_text(json.dumps(package_data, indent=2, ensure_ascii=False), encoding="utf-8")

        return rendered_paths

    def _render_slide_html(self, slide: Dict[str, Any], slide_num: int, total_slides: int, colors: Dict[str, str]) -> str:
        layout = slide.get("layout", "concept_deepdive").lower()
        headline = slide.get("headline", "") or (slide.get("headline_top", "") + " " + slide.get("headline_accent", "")).strip() or slide.get("eyebrow", "")
        eyebrow = slide.get("eyebrow", "")
        subtitle = slide.get("subtitle", "")
        main_stat = slide.get("main_stat", slide.get("stat_value", ""))
        stat_label = slide.get("stat_label", "")
        left_col = slide.get("left_col", "")
        right_col = slide.get("right_col", "")

        bg_color = colors["background"]
        primary_color = colors["primary"]
        accent_color = colors["accent"]
        text_color = colors["text"]
        subtext_color = colors["subtext"]
        card_bg = colors.get("card_bg", "rgba(18, 20, 30, 0.85)")

        hl_len = len(headline)
        hl_size = "68px" if hl_len < 40 else "54px" if hl_len < 65 else "44px"

        mac_header = f"""
    <div class="mac-dots">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
    </div>"""

        if layout == "hero" or slide_num == 1:
            eyebrow_pill = f"<div style='display:inline-block; background: rgba(0,229,204,0.08); border: 1px solid rgba(0,229,204,0.3); padding: 10px 28px; border-radius: 30px; color: {primary_color}; font-size: 20px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 35px; box-shadow: 0 0 20px rgba(0,229,204,0.15);'>✦ {eyebrow} ✦</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_pill}
  <div style='color: {text_color}; font-size: {hl_size}; font-weight: 900; line-height: 1.15; margin-bottom: 40px; max-width: 940px; text-shadow: 0 0 40px rgba(255,255,255,0.1);'>{headline}</div>
  <div style='color: {subtext_color}; font-size: 34px; font-weight: 500; line-height: 1.5; max-width: 880px;'>{subtitle}</div>
"""
        elif layout == "stat_highlight" or main_stat:
            inner_html = f"""
  <div style='color: {accent_color}; font-size: 40px; font-weight: 800; line-height: 1.2; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 2px;'>{headline}</div>
  <div style='font-size: 165px; font-weight: 900; color: {primary_color}; line-height: 1; margin-bottom: 30px; text-shadow: 0 0 60px rgba(0,229,204,0.3);'>{main_stat}</div>
  <div class="mac-card" style="max-width: 880px;">
    {mac_header}
    <div style='color: {text_color}; font-size: 30px; font-weight: 500; line-height: 1.5;'>{stat_label or subtitle}</div>
  </div>
"""
        elif layout == "comparative_text" or (left_col and right_col):
            inner_html = f"""
  <div style='color: {text_color}; font-size: 46px; font-weight: 800; line-height: 1.2; margin-bottom: 35px;'>{headline}</div>
  <div style='display: flex; gap: 35px; width: 100%; max-width: 960px; text-align: left;'>
    <div class="mac-card" style="flex: 1; padding: 26px;">
      <div class="card-strip" style="background: {accent_color};"></div>
      {mac_header}
      <div style='color: {accent_color}; font-size: 22px; font-weight: 800; margin-bottom: 14px; letter-spacing: 1px;'>❌ AMATEUR / LEGACY</div>
      <div style='color: {text_color}; font-size: 24px; line-height: 1.6; white-space: pre-line;'>{left_col}</div>
    </div>
    <div class="mac-card" style="flex: 1; padding: 26px;">
      <div class="card-strip" style="background: {primary_color};"></div>
      {mac_header}
      <div style='color: {primary_color}; font-size: 22px; font-weight: 800; margin-bottom: 14px; letter-spacing: 1px;'>⚡ PRO / MODERN</div>
      <div style='color: {text_color}; font-size: 24px; line-height: 1.6; white-space: pre-line;'>{right_col}</div>
    </div>
  </div>
"""
        elif layout in ["outro", "cta_classic"] or slide_num == total_slides:
            cta_text = slide.get("cta_text", "Follow @AIWITHSUFIYAN")
            cta_highlight = slide.get("cta_highlight", slide.get("subtitle", "Save this post for your next architecture review."))
            items = slide.get("items", [])
            items_html = ""
            if isinstance(items, list):
                for item in items:
                    txt = item.get("text", str(item)) if isinstance(item, dict) else str(item)
                    items_html += f"<div style='color: {text_color}; font-size: 28px; margin-bottom: 16px; font-weight: 600;'>👉 {txt}</div>"
            eyebrow_pill = f"<div style='display:inline-block; background: rgba(255,75,75,0.08); border: 1px solid rgba(255,75,75,0.3); padding: 8px 24px; border-radius: 30px; color: {accent_color}; font-size: 18px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 25px;'>✦ {eyebrow} ✦</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_pill}
  <div style='color: {primary_color}; font-size: 58px; font-weight: 900; line-height: 1.2; margin-bottom: 25px; max-width: 880px;'>{headline or 'Ready to Level Up?'}</div>
  <div class="mac-card" style="max-width: 860px; margin-bottom: 35px;">
    {mac_header}
    {items_html}
    <div style='color: {subtext_color}; font-size: 26px; font-weight: 500; line-height: 1.5; margin-top: 15px;'>{cta_highlight}</div>
  </div>
  <div style='background: {primary_color}; color: {bg_color}; font-size: 28px; font-weight: 800; padding: 22px 55px; border-radius: 40px; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 0 30px rgba(0,229,204,0.4);'>{cta_text}</div>
"""
        else:
            boxes_html = ""
            for b_idx in [1, 2, 3]:
                title = slide.get(f"box{b_idx}_title", "")
                body = slide.get(f"box{b_idx}_body", "")
                if title or body:
                    bc = primary_color if b_idx==1 else accent_color if b_idx==2 else primary_color
                    boxes_html += f"""
    <div class="mac-card" style="margin-bottom: 20px; padding: 24px 30px;">
      <div class="card-strip" style="background: {bc};"></div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        {mac_header}
        <div style='color: {bc}; font-size: 24px; font-weight: 800; letter-spacing: 0.5px;'>{title}</div>
      </div>
      <div style='color: {subtext_color}; font-size: 23px; line-height: 1.5;'>{body}</div>
    </div>"""
            eyebrow_pill = f"<div style='display:inline-block; background: rgba(0,229,204,0.08); border: 1px solid rgba(0,229,204,0.3); padding: 8px 24px; border-radius: 30px; color: {accent_color}; font-size: 18px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 25px;'>✦ {eyebrow} ✦</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_pill}
  <div style='color: {text_color}; font-size: 46px; font-weight: 800; line-height: 1.2; margin-bottom: 30px; max-width: 900px;'>{headline}</div>
  <div style='width: 100%; display: flex; flex-direction: column; align-items: center;'>{boxes_html}</div>
"""

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1350px; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; background: {bg_color}; }}
.slide {{ width: 1080px; height: 1350px; position: relative; display: flex; flex-direction: column; background: {bg_color}; color: {text_color}; justify-content: center; align-items: center; text-align: center; padding: 90px; overflow: hidden; }}
.glow-blob-1 {{ position: absolute; top: -120px; left: -120px; width: 480px; height: 480px; background: rgba(0, 229, 204, 0.18); filter: blur(95px); border-radius: 50%; pointer-events: none; z-index: 1; }}
.glow-blob-2 {{ position: absolute; bottom: -140px; right: -140px; width: 520px; height: 520px; background: rgba(255, 75, 75, 0.16); filter: blur(105px); border-radius: 50%; pointer-events: none; z-index: 1; }}
.content {{ position: relative; z-index: 2; width: 100%; display: flex; flex-direction: column; align-items: center; }}
.mac-card {{ background: {card_bg}; border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 20px 50px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.18); border-radius: 18px; position: relative; overflow: hidden; backdrop-filter: blur(24px); }}
.mac-dots {{ display: flex; gap: 8px; align-items: center; }}
.dot {{ width: 12px; height: 12px; border-radius: 50%; }}
.dot-red {{ background: #FF5F56; }}
.dot-yellow {{ background: #FFBD2E; }}
.dot-green {{ background: #27C93F; }}
.card-strip {{ position: absolute; left: 0; top: 0; bottom: 0; width: 6px; }}
.footer {{ position: absolute; bottom: 40px; left: 60px; right: 60px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255, 255, 255, 0.12); padding-top: 22px; z-index: 2; }}
.brand {{ font-size: 16px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; color: {text_color}; opacity: 0.65; }}
.slide_num {{ font-size: 16px; font-weight: 800; color: {primary_color}; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); padding: 6px 18px; border-radius: 8px; }}
</style>
</head>
<body>
<div class="slide">
  <div class="glow-blob-1"></div>
  <div class="glow-blob-2"></div>
  <div class="content">
{inner_html}
  </div>
  <div class="footer">
    <div class="brand">✦ AIWITHSUFIYAN — ARCHITECTURE BLUEPRINT</div>
    <div class="slide_num">{slide_num:02d} / {total_slides:02d}</div>
  </div>
</div>
</body>
</html>"""

    def _render_slide_png(self, slide: Dict[str, Any], slide_num: int, total_slides: int, colors: Dict[str, str], output_png: Path):
        layout = slide.get("layout", "concept_deepdive").lower()
        headline = self._clean_txt(slide.get("headline", "") or (slide.get("headline_top", "") + " " + slide.get("headline_accent", "")).strip() or slide.get("eyebrow", ""))
        eyebrow = self._clean_txt(slide.get("eyebrow", ""))
        subtitle = self._clean_txt(slide.get("subtitle", ""))
        main_stat = self._clean_txt(slide.get("main_stat", slide.get("stat_value", "")))
        stat_label = self._clean_txt(slide.get("stat_label", ""))
        left_col = self._clean_txt(slide.get("left_col", ""))
        right_col = self._clean_txt(slide.get("right_col", ""))

        bg_color = colors["background"]
        primary_color = colors["primary"]
        accent_color = colors["accent"]
        text_color = colors["text"]
        subtext_color = colors["subtext"]

        # Base canvas + Radial Neon Glow Blobs
        cmd = [
            "convert", "-size", "1080x1350", f"xc:{bg_color}",
            "(", "-size", "500x500", "xc:none", "-fill", "rgba(0,229,204,0.24)", "-draw", "circle 250,250 250,50", "-blur", "0x85", ")",
            "-gravity", "northwest", "-geometry", "-100-100", "-composite",
            "(", "-size", "600x600", "xc:none", "-fill", "rgba(255,75,75,0.22)", "-draw", "circle 300,300 300,50", "-blur", "0x95", ")",
            "-gravity", "southeast", "-geometry", "-150-150", "-composite"
        ]

        if layout == "hero" or slide_num == 1:
            if eyebrow:
                cmd += [
                    "-fill", "rgba(0,229,204,0.06)", "-stroke", "rgba(0,229,204,0.35)", "-strokewidth", "2", "-draw", "roundrectangle 310,120 770,175 28,28",
                    "(", "-size", "440x40", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:✦ {eyebrow} ✦", ")",
                    "-gravity", "north", "-geometry", "+0+128", "-composite"
                ]
            if headline:
                cmd += [
                    "(", "-size", "940x260", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", text_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+260", "-composite"
                ]
            if subtitle:
                cmd += [
                    "(", "-size", "880x300", "-background", "none", "-font", "DejaVu-Sans", "-fill", subtext_color, "-gravity", "center", f"caption:{subtitle}", ")",
                    "-gravity", "north", "-geometry", "+0+560", "-composite"
                ]
        elif layout == "stat_highlight" or main_stat:
            if headline:
                cmd += [
                    "(", "-size", "900x100", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", accent_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+160", "-composite"
                ]
            if main_stat:
                cmd += [
                    "(", "-size", "900x240", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{main_stat}", ")",
                    "-gravity", "north", "-geometry", "+0+320", "-composite"
                ]
            if stat_label or subtitle:
                cmd += [
                    "-fill", "rgba(0,0,0,0.6)", "-draw", "roundrectangle 82,606 998,906 24,24",
                    "-fill", "#12141E", "-stroke", "rgba(255,255,255,0.12)", "-strokewidth", "2", "-draw", "roundrectangle 80,600 1000,900 24,24",
                    "-fill", "none", "-stroke", "rgba(255,255,255,0.2)", "-strokewidth", "1", "-draw", "line 104,602 976,602",
                    "-fill", "#FF5F56", "-draw", "circle 122,628 126,628",
                    "-fill", "#FFBD2E", "-draw", "circle 142,628 146,628",
                    "-fill", "#27C93F", "-draw", "circle 162,628 166,628",
                    "(", "-size", "860x220", "-background", "none", "-font", "DejaVu-Sans", "-fill", text_color, "-gravity", "center", f"caption:{stat_label or subtitle}", ")",
                    "-gravity", "north", "-geometry", "+0+655", "-composite"
                ]
        elif layout == "comparative_text" or (left_col and right_col):
            if headline:
                cmd += [
                    "(", "-size", "900x100", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", text_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+110", "-composite"
                ]
            cmd += [
                "-fill", "rgba(0,0,0,0.6)", "-draw", "roundrectangle 62,246 508,1106 24,24",
                "-fill", "#141118", "-stroke", "rgba(255,75,75,0.3)", "-strokewidth", "2", "-draw", "roundrectangle 60,240 510,1100 24,24",
                "-fill", "none", "-stroke", "rgba(255,255,255,0.15)", "-strokewidth", "1", "-draw", "line 84,242 486,242",
                "-fill", accent_color, "-stroke", "none", "-draw", "roundrectangle 60,240 74,1100 24,24", "-draw", "rectangle 66,240 74,1100",
                "-fill", "#FF5F56", "-draw", "circle 102,268 106,268",
                "-fill", "#FFBD2E", "-draw", "circle 122,268 126,268",
                "-fill", "#27C93F", "-draw", "circle 142,268 146,268",
                "(", "-size", "340x40", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", accent_color, "-gravity", "west", "caption:❌ AMATEUR / LEGACY", ")",
                "-gravity", "northwest", "-geometry", "+85+250", "-composite",
                "(", "-size", "390x750", "-background", "none", "-font", "DejaVu-Sans", "-fill", "#C4C4CC", "-gravity", "northwest", f"caption:{left_col}", ")",
                "-gravity", "northwest", "-geometry", "+85+320", "-composite",
                "-fill", "rgba(0,0,0,0.6)", "-draw", "roundrectangle 552,246 998,1106 24,24",
                "-fill", "#101720", "-stroke", "rgba(0,229,204,0.3)", "-strokewidth", "2", "-draw", "roundrectangle 550,240 1000,1100 24,24",
                "-fill", "none", "-stroke", "rgba(255,255,255,0.15)", "-strokewidth", "1", "-draw", "line 574,242 976,242",
                "-fill", primary_color, "-stroke", "none", "-draw", "roundrectangle 550,240 564,1100 24,24", "-draw", "rectangle 556,240 564,1100",
                "-fill", "#FF5F56", "-draw", "circle 592,268 596,268",
                "-fill", "#FFBD2E", "-draw", "circle 612,268 616,268",
                "-fill", "#27C93F", "-draw", "circle 632,268 636,268",
                "(", "-size", "340x40", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "west", "caption:⚡ PRO / MODERN", ")",
                "-gravity", "northwest", "-geometry", "+575+250", "-composite",
                "(", "-size", "390x750", "-background", "none", "-font", "DejaVu-Sans", "-fill", text_color, "-gravity", "northwest", f"caption:{right_col}", ")",
                "-gravity", "northwest", "-geometry", "+575+320", "-composite"
            ]
        elif layout in ["outro", "cta_classic"] or slide_num == total_slides:
            cta_text = self._clean_txt(slide.get("cta_text", "Follow @AIWITHSUFIYAN"))
            cta_highlight = self._clean_txt(slide.get("cta_highlight", slide.get("subtitle", "Save this post for your next architecture review.")))
            items = slide.get("items", [])
            if eyebrow:
                cmd += [
                    "-fill", "rgba(255,75,75,0.08)", "-stroke", "rgba(255,75,75,0.35)", "-strokewidth", "2", "-draw", "roundrectangle 330,120 750,170 28,28",
                    "(", "-size", "400x40", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", accent_color, "-gravity", "center", f"caption:✦ {eyebrow} ✦", ")",
                    "-gravity", "north", "-geometry", "+0+125", "-composite"
                ]
            if headline or "Ready to Level Up?":
                cmd += [
                    "(", "-size", "920x130", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{headline or 'Ready to Level Up?'}", ")",
                    "-gravity", "north", "-geometry", "+0+190", "-composite"
                ]
            # Mac Card for takeaways
            cmd += [
                "-fill", "rgba(0,0,0,0.6)", "-draw", "roundrectangle 102,346 978,746 24,24",
                "-fill", "#12141E", "-stroke", "rgba(255,255,255,0.12)", "-strokewidth", "2", "-draw", "roundrectangle 100,340 980,740 24,24",
                "-fill", "none", "-stroke", "rgba(255,255,255,0.2)", "-strokewidth", "1", "-draw", "line 124,342 956,342",
                "-fill", "#FF5F56", "-draw", "circle 142,368 146,368",
                "-fill", "#FFBD2E", "-draw", "circle 162,368 166,368",
                "-fill", "#27C93F", "-draw", "circle 182,368 186,368"
            ]
            if items and isinstance(items, list) and len(items) > 0:
                txt0 = self._clean_txt(items[0].get("text", str(items[0])) if isinstance(items[0], dict) else str(items[0]))
                cmd += [
                    "(", "-size", "820x100", "-background", "none", "-font", "DejaVu-Sans", "-fill", text_color, "-gravity", "center", f"caption:👉 {txt0}", ")",
                    "-gravity", "north", "-geometry", "+0+410", "-composite"
                ]
            cmd += [
                "(", "-size", "820x160", "-background", "none", "-font", "DejaVu-Sans", "-fill", subtext_color, "-gravity", "center", f"caption:{cta_highlight}", ")",
                "-gravity", "north", "-geometry", "+0+540", "-composite",
                "-fill", primary_color, "-draw", "roundrectangle 240,820 840,930 55,55",
                "(", "-size", "560x80", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", "#090A0F", "-gravity", "center", f"caption:{cta_text}", ")",
                "-gravity", "north", "-geometry", "+0+835", "-composite"
            ]
        elif layout in ["concept_deepdive", "process_detail"] or slide.get("box1_title"):
            if eyebrow:
                cmd += [
                    "-fill", "rgba(0,229,204,0.08)", "-stroke", "rgba(0,229,204,0.35)", "-strokewidth", "2", "-draw", "roundrectangle 330,70 750,115 24,24",
                    "(", "-size", "400x36", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", accent_color, "-gravity", "center", f"caption:✦ {eyebrow} ✦", ")",
                    "-gravity", "north", "-geometry", "+0+75", "-composite"
                ]
            if headline:
                cmd += [
                    "(", "-size", "920x90", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", text_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+130", "-composite"
                ]
            y_offsets = [(240, 520, 268, 330), (550, 830, 578, 640), (860, 1140, 888, 950)]
            box_colors = [primary_color, accent_color, primary_color]
            for b_idx in [1, 2, 3]:
                title = self._clean_txt(slide.get(f"box{b_idx}_title", ""))
                body = self._clean_txt(slide.get(f"box{b_idx}_body", ""))
                if title or body:
                    y1, y2, yt, yb = y_offsets[b_idx-1]
                    bc = box_colors[b_idx-1]
                    cmd += [
                        "-fill", "rgba(0,0,0,0.6)", "-draw", f"roundrectangle 82,{y1+6} 998,{y2+6} 24,24",
                        "-fill", "#12141E", "-stroke", "rgba(255,255,255,0.12)", "-strokewidth", "2", "-draw", f"roundrectangle 80,{y1} 1000,{y2} 24,24",
                        "-fill", "none", "-stroke", "rgba(255,255,255,0.2)", "-strokewidth", "1", "-draw", f"line 104,{y1+2} 976,{y1+2}",
                        "-fill", bc, "-stroke", "none", "-draw", f"roundrectangle 80,{y1} 94,{y2} 24,24", "-draw", f"rectangle 86,{y1} 94,{y2}",
                        "-fill", "#FF5F56", "-draw", f"circle 122,{y1+28} 126,{y1+28}",
                        "-fill", "#FFBD2E", "-draw", f"circle 142,{y1+28} 146,{y1+28}",
                        "-fill", "#27C93F", "-draw", f"circle 162,{y1+28} 166,{y1+28}"
                    ]
                    if title:
                        cmd += [
                            "(", "-size", "750x38", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", bc, "-gravity", "west", f"caption:{title}", ")",
                            "-gravity", "north", "-geometry", f"+110+{yt}", "-composite"
                        ]
                    if body:
                        cmd += [
                            "(", "-size", "860x170", "-background", "none", "-font", "DejaVu-Sans", "-fill", subtext_color, "-gravity", "west", f"caption:{body}", ")",
                            "-gravity", "north", "-geometry", f"+20+{yb}", "-composite"
                        ]
        else:
            if headline:
                cmd += [
                    "(", "-size", "900x160", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+250", "-composite"
                ]
            if subtitle:
                cmd += [
                    "-fill", "#12141E", "-stroke", "rgba(255,255,255,0.12)", "-strokewidth", "2", "-draw", "roundrectangle 80,450 1000,950 24,24",
                    "(", "-size", "860x460", "-background", "none", "-font", "DejaVu-Sans", "-fill", text_color, "-gravity", "center", f"caption:{subtitle}", ")",
                    "-gravity", "north", "-geometry", "+0+470", "-composite"
                ]

        # Widescreen footer line + brand + slide pill
        cmd += [
            "-stroke", "rgba(255,255,255,0.12)", "-strokewidth", "1", "-draw", "line 60,1250 1020,1250",
            "-font", "DejaVu-Sans-Bold", "-fill", "#FFFFFF99", "-pointsize", "19", "-gravity", "southwest", "-annotate", "+60+45", "✦ AIWITHSUFIYAN — ARCHITECTURE BLUEPRINT",
            "-fill", "rgba(255,255,255,0.06)", "-stroke", "rgba(255,255,255,0.2)", "-strokewidth", "1", "-draw", "roundrectangle 850,1268 1020,1312 12,12",
            "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-pointsize", "18", "-gravity", "southeast", "-annotate", "+82+45", f"{slide_num:02d} / {total_slides:02d}",
            str(output_png)
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            pass
