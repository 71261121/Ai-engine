"""
Next-Gen Visual Compositor (V100) for 1080x1350 Instagram/LinkedIn Carousels.
Supports 12 Tailwind-inspired design archetypes, dynamic SVG architecture diagrams,
auto-scaling typography, and crisp vector PNG slide generation.
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
    V100 Renderer synthesizing both responsive HTML slides and high-resolution PNG image slides
    across 12 modular visual archetypes.
    """

    ARCHETYPES = {
        "cyber_dark": {"background": "#0F0F13", "primary": "#00E5CC", "accent": "#FF4B4B", "text": "#FFFFFF", "subtext": "#B0B0B0", "card_bg": "rgba(255,255,255,0.03)"},
        "minimalist_white": {"background": "#FAFAFA", "primary": "#2563EB", "accent": "#DC2626", "text": "#18181B", "subtext": "#52525B", "card_bg": "#F4F4F5"},
        "monokai_code": {"background": "#1E1E1E", "primary": "#A6E22E", "accent": "#F92672", "text": "#F8F8F2", "subtext": "#75715E", "card_bg": "#272822"},
        "brutalist_swiss": {"background": "#FACC15", "primary": "#000000", "accent": "#DC2626", "text": "#000000", "subtext": "#27272A", "card_bg": "#FFFFFF"},
        "infrastructure_blue": {"background": "#0D1117", "primary": "#38BDF8", "accent": "#F59E0B", "text": "#F9FAFB", "subtext": "#9CA3AF", "card_bg": "rgba(255,255,255,0.04)"}
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
        """
        Render slides to HTML (`slide_01.html`) and PNG (`slide_01.png`) in output_dir.
        """
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

        # Save package manifest
        package_file = output_dir / "carousel_data.json"
        package_data = {
            "topic": topic,
            "version": "v100.0_masterpiece",
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
        card_bg = colors.get("card_bg", "rgba(255,255,255,0.03)")

        # Auto-scaling headline font size check
        hl_len = len(headline)
        hl_size = "68px" if hl_len < 40 else "54px" if hl_len < 65 else "44px"

        if layout == "hero" or slide_num == 1:
            eyebrow_tag = f"<div style='color: {accent_color}; font-size: 22px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 24px;'>{eyebrow}</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_tag}
  <div style='color: {primary_color}; font-size: {hl_size}; font-weight: 900; line-height: 1.15; margin-bottom: 40px; max-width: 940px;'>{headline}</div>
  <div style='color: {subtext_color}; font-size: 34px; font-weight: 500; line-height: 1.5; max-width: 880px;'>{subtitle}</div>
"""
        elif layout == "stat_highlight" or main_stat:
            inner_html = f"""
  <div style='color: {primary_color}; font-size: 44px; font-weight: 700; line-height: 1.2; margin-bottom: 30px;'>{headline}</div>
  <div style='font-size: 155px; font-weight: 900; color: {primary_color}; line-height: 1; margin-bottom: 25px;'>{main_stat}</div>
  <div style='color: {subtext_color}; font-size: 32px; font-weight: 400; line-height: 1.5; max-width: 860px;'>{stat_label or subtitle}</div>
"""
        elif layout == "comparative_text" or (left_col and right_col):
            svg_comp = SVGFlowEngine.generate_comparison_svg(left_col, right_col, primary_color, accent_color)
            inner_html = f"""
  <div style='color: {primary_color}; font-size: 46px; font-weight: 800; line-height: 1.2; margin-bottom: 35px;'>{headline}</div>
  {svg_comp}
  <div style='display: flex; gap: 35px; width: 100%; max-width: 940px; text-align: left;'>
    <div style='flex: 1; background: {card_bg}; border-left: 5px solid {accent_color}; padding: 28px; border-radius: 12px;'>
      <div style='color: {accent_color}; font-size: 24px; font-weight: 800; margin-bottom: 12px;'>AMATEUR / OLD</div>
      <div style='color: {text_color}; font-size: 25px; line-height: 1.5;'>{left_col}</div>
    </div>
    <div style='flex: 1; background: {card_bg}; border-left: 5px solid {primary_color}; padding: 28px; border-radius: 12px;'>
      <div style='color: {primary_color}; font-size: 24px; font-weight: 800; margin-bottom: 12px;'>PRO / NEW</div>
      <div style='color: {text_color}; font-size: 25px; line-height: 1.5;'>{right_col}</div>
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
                    items_html += f"<div style='color: {text_color}; font-size: 26px; margin-bottom: 14px; font-weight: 600;'>👉 {txt}</div>"
            eyebrow_tag = f"<div style='color: {accent_color}; font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px;'>{eyebrow}</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_tag}
  <div style='color: {primary_color}; font-size: 58px; font-weight: 900; line-height: 1.2; margin-bottom: 24px; max-width: 880px;'>{headline or 'Ready to Level Up?'}</div>
  {items_html}
  <div style='color: {subtext_color}; font-size: 28px; font-weight: 500; line-height: 1.5; max-width: 840px; margin: 30px 0 50px 0;'>{cta_highlight}</div>
  <div style='background: {primary_color}; color: {bg_color}; font-size: 28px; font-weight: 800; padding: 22px 55px; border-radius: 40px; text-transform: uppercase; letter-spacing: 1px;'>{cta_text}</div>
"""
        else:
            # Cards + dynamic pipeline SVG check
            boxes_html = ""
            for b_idx in [1, 2, 3]:
                title = slide.get(f"box{b_idx}_title", "")
                body = slide.get(f"box{b_idx}_body", "")
                if title or body:
                    boxes_html += f"""
    <div style='background: {card_bg}; border-left: 5px solid {primary_color if b_idx==1 else accent_color if b_idx==2 else subtext_color}; padding: 26px; border-radius: 12px; margin-bottom: 22px; text-align: left; width: 100%; max-width: 920px;'>
      <div style='color: {primary_color if b_idx==1 else accent_color if b_idx==2 else text_color}; font-size: 26px; font-weight: 800; margin-bottom: 10px;'>{title}</div>
      <div style='color: {subtext_color}; font-size: 24px; line-height: 1.5;'>{body}</div>
    </div>"""
            svg_pipeline = SVGFlowEngine.generate_pipeline_svg([slide.get("box1_title", "Concept"), slide.get("box2_title", "Flow"), slide.get("box3_title", "Output"), "Production"], primary_color, accent_color) if slide_num == 3 else ""
            eyebrow_tag = f"<div style='color: {accent_color}; font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px;'>{eyebrow}</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_tag}
  <div style='color: {text_color}; font-size: 46px; font-weight: 800; line-height: 1.2; margin-bottom: 25px; max-width: 900px;'>{headline}</div>
  {svg_pipeline}
  <div style='width: 100%; display: flex; flex-direction: column; align-items: center;'>{boxes_html}</div>
"""

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1350px; font-family: 'Inter', sans-serif; overflow: hidden; }}
.slide {{ width: 1080px; height: 1350px; position: relative; display: flex; flex-direction: column; background: {bg_color}; color: {text_color}; justify-content: center; align-items: center; text-align: center; padding: 90px; }}
.brand {{ position: absolute; bottom: 45px; left: 60px; font-size: 16px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: {text_color}; opacity: 0.45; }}
.slide_num {{ position: absolute; bottom: 45px; right: 60px; font-size: 16px; font-weight: 600; color: {text_color}; opacity: 0.45; }}
</style>
</head>
<body>
<div class="slide">
{inner_html}
  <div class="brand">AIWITHSUFIYAN</div>
  <div class="slide_num">{slide_num}/{total_slides}</div>
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

        cmd = ["convert", "-size", "1080x1350", f"xc:{bg_color}"]

        if layout == "hero" or slide_num == 1:
            if eyebrow:
                cmd += [
                    "(", "-size", "920x60", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", accent_color, "-gravity", "center", f"caption:{eyebrow}", ")",
                    "-gravity", "north", "-geometry", "+0+180", "-composite"
                ]
            if headline:
                cmd += [
                    "(", "-size", "940x250", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+280", "-composite"
                ]
            if subtitle:
                cmd += [
                    "(", "-size", "880x320", "-background", "none", "-font", "DejaVu-Sans", "-fill", subtext_color, "-gravity", "center", f"caption:{subtitle}", ")",
                    "-gravity", "north", "-geometry", "+0+560", "-composite"
                ]
        elif layout == "stat_highlight" or main_stat:
            if headline:
                cmd += [
                    "(", "-size", "900x120", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+220", "-composite"
                ]
            if main_stat:
                cmd += [
                    "(", "-size", "900x240", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{main_stat}", ")",
                    "-gravity", "north", "-geometry", "+0+400", "-composite"
                ]
            if stat_label or subtitle:
                cmd += [
                    "(", "-size", "860x280", "-background", "none", "-font", "DejaVu-Sans", "-fill", subtext_color, "-gravity", "center", f"caption:{stat_label or subtitle}", ")",
                    "-gravity", "north", "-geometry", "+0+680", "-composite"
                ]
        elif layout == "comparative_text" or (left_col and right_col):
            if headline:
                cmd += [
                    "(", "-size", "900x120", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+140", "-composite"
                ]
            cmd += [
                "-fill", "#181820", "-draw", "roundrectangle 80,320 520,1050 16,16",
                "-fill", accent_color, "-draw", "rectangle 80,320 88,1050",
                "(", "-size", "410x60", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", accent_color, "-gravity", "west", "caption:AMATEUR / OLD", ")",
                "-gravity", "northwest", "-geometry", "+100+340", "-composite",
                "(", "-size", "410x620", "-background", "none", "-font", "DejaVu-Sans", "-fill", text_color, "-gravity", "northwest", f"caption:{left_col}", ")",
                "-gravity", "northwest", "-geometry", "+100+410", "-composite",
                "-fill", "#181820", "-draw", "roundrectangle 560,320 1000,1050 16,16",
                "-fill", primary_color, "-draw", "rectangle 560,320 568,1050",
                "(", "-size", "410x60", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "west", "caption:PRO / NEW", ")",
                "-gravity", "northwest", "-geometry", "+580+340", "-composite",
                "(", "-size", "410x620", "-background", "none", "-font", "DejaVu-Sans", "-fill", text_color, "-gravity", "northwest", f"caption:{right_col}", ")",
                "-gravity", "northwest", "-geometry", "+580+410", "-composite"
            ]
        elif layout in ["outro", "cta_classic"] or slide_num == total_slides:
            cta_text = self._clean_txt(slide.get("cta_text", "Follow @AIWITHSUFIYAN"))
            cta_highlight = self._clean_txt(slide.get("cta_highlight", slide.get("subtitle", "Save this post for your next architecture review.")))
            items = slide.get("items", [])
            if eyebrow:
                cmd += [
                    "(", "-size", "920x50", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", accent_color, "-gravity", "center", f"caption:{eyebrow}", ")",
                    "-gravity", "north", "-geometry", "+0+140", "-composite"
                ]
            if headline or "Ready to Level Up?":
                cmd += [
                    "(", "-size", "920x140", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{headline or 'Ready to Level Up?'}", ")",
                    "-gravity", "north", "-geometry", "+0+210", "-composite"
                ]
            if items and isinstance(items, list) and len(items) > 0:
                txt0 = self._clean_txt(items[0].get("text", str(items[0])) if isinstance(items[0], dict) else str(items[0]))
                cmd += [
                    "(", "-size", "860x100", "-background", "none", "-font", "DejaVu-Sans", "-fill", text_color, "-gravity", "center", f"caption:👉 {txt0}", ")",
                    "-gravity", "north", "-geometry", "+0+380", "-composite"
                ]
            cmd += [
                "(", "-size", "860x160", "-background", "none", "-font", "DejaVu-Sans", "-fill", subtext_color, "-gravity", "center", f"caption:{cta_highlight}", ")",
                "-gravity", "north", "-geometry", "+0+530", "-composite",
                "-fill", primary_color, "-draw", "roundrectangle 240,780 840,890 55,55",
                "(", "-size", "560x80", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", bg_color if bg_color!="#FAFAFA" else "#0F0F13", "-gravity", "center", f"caption:{cta_text}", ")",
                "-gravity", "north", "-geometry", "+0+795", "-composite"
            ]
        elif layout in ["concept_deepdive", "process_detail"] or slide.get("box1_title"):
            if eyebrow:
                cmd += [
                    "(", "-size", "920x40", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", accent_color, "-gravity", "center", f"caption:{eyebrow}", ")",
                    "-gravity", "north", "-geometry", "+0+80", "-composite"
                ]
            if headline:
                cmd += [
                    "(", "-size", "920x100", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", text_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+130", "-composite"
                ]
            y_offsets = [(260, 500, 285, 345), (540, 780, 565, 625), (820, 1060, 845, 905)]
            box_colors = [primary_color, accent_color, subtext_color]
            for b_idx in [1, 2, 3]:
                title = self._clean_txt(slide.get(f"box{b_idx}_title", ""))
                body = self._clean_txt(slide.get(f"box{b_idx}_body", ""))
                if title or body:
                    y1, y2, yt, yb = y_offsets[b_idx-1]
                    bc = box_colors[b_idx-1]
                    cmd += [
                        "-fill", "#181820" if bg_color=="#0F0F13" else "#EEEEF0", "-draw", f"roundrectangle 90,{y1} 990,{y2} 16,16",
                        "-fill", bc, "-draw", f"rectangle 90,{y1} 98,{y2}"
                    ]
                    if title:
                        cmd += [
                            "(", "-size", "850x40", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", bc if b_idx<3 else text_color, "-gravity", "west", f"caption:{title}", ")",
                            "-gravity", "north", "-geometry", f"+10+{yt}", "-composite"
                        ]
                    if body:
                        cmd += [
                            "(", "-size", "850x120", "-background", "none", "-font", "DejaVu-Sans", "-fill", subtext_color, "-gravity", "west", f"caption:{body}", ")",
                            "-gravity", "north", "-geometry", f"+10+{yb}", "-composite"
                        ]
        else:
            if headline:
                cmd += [
                    "(", "-size", "900x160", "-background", "none", "-font", "DejaVu-Sans-Bold", "-fill", primary_color, "-gravity", "center", f"caption:{headline}", ")",
                    "-gravity", "north", "-geometry", "+0+250", "-composite"
                ]
            if subtitle:
                cmd += [
                    "-fill", "#181820", "-draw", "roundrectangle 90,450 990,950 16,16",
                    "(", "-size", "860x460", "-background", "none", "-font", "DejaVu-Sans", "-fill", text_color, "-gravity", "center", f"caption:{subtitle}", ")",
                    "-gravity", "north", "-geometry", "+0+470", "-composite"
                ]

        cmd += [
            "-font", "DejaVu-Sans-Bold", "-fill", "#FFFFFF66" if bg_color=="#0F0F13" else "#00000066", "-pointsize", "24", "-gravity", "southwest", "-annotate", "+60+45", "AIWITHSUFIYAN",
            "-font", "DejaVu-Sans-Bold", "-fill", "#FFFFFF66" if bg_color=="#0F0F13" else "#00000066", "-pointsize", "24", "-gravity", "southeast", "-annotate", "+60+45", f"{slide_num}/{total_slides}",
            str(output_png)
        ]

        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            pass
