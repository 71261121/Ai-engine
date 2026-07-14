"""
HTML Concept Renderer for Instagram Carousels (1080x1350).
Generates standalone, responsive HTML slide files based on narrative slide blueprints
and TopicDNA color language.
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from .topic_dna import get_topic_dna


class ConceptRenderer:
    """
    Renders visual blueprints into HTML slides matching 1080x1350 Instagram specs.
    """

    def __init__(self):
        pass

    def render(self, slides: List[Dict[str, Any]], topic: str, output_dir: Path,
               topic_dna: Optional[Dict[str, Any]] = None) -> List[Path]:
        """
        Render each slide into slide_01.html, slide_02.html, ... in output_dir.
        Also writes carousel_data.json.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        if topic_dna is None:
            topic_dna = get_topic_dna(topic)

        colors = topic_dna.get("color_language", {
            "background": "#0F0F13",
            "primary": "#00E5CC",
            "accent": "#FF4B4B",
            "text": "#FFFFFF",
            "subtext": "#B0B0B0"
        })

        total_slides = len(slides)
        rendered_paths = []

        for idx, slide in enumerate(slides, 1):
            file_path = output_dir / f"slide_{idx:02d}.html"
            html_content = self._render_slide_html(slide, idx, total_slides, colors)
            file_path.write_text(html_content, encoding="utf-8")
            rendered_paths.append(file_path)

        # Write data package
        package_file = output_dir / "carousel_data.json"
        package_data = {
            "topic": topic,
            "topic_dna": topic_dna,
            "slides": slides,
            "slide_files": [p.name for p in rendered_paths]
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

        bg_color = colors.get("background", "#0F0F13")
        primary_color = colors.get("primary", "#00E5CC")
        accent_color = colors.get("accent", "#FF4B4B")
        text_color = colors.get("text", "#FFFFFF")
        subtext_color = colors.get("subtext", "#B0B0B0")

        # Layout specific body rendering
        if layout == "hero" or slide_num == 1:
            eyebrow_tag = f"<div style='color: {accent_color}; font-size: 22px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 24px;'>{eyebrow}</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_tag}
  <div style='color: {primary_color}; font-size: 68px; font-weight: 900; line-height: 1.15; margin-bottom: 40px; max-width: 920px;'>{headline}</div>
  <div style='color: {subtext_color}; font-size: 34px; font-weight: 500; line-height: 1.5; max-width: 880px;'>{subtitle}</div>
"""
        elif layout == "stat_highlight" or main_stat:
            inner_html = f"""
  <div style='color: {primary_color}; font-size: 44px; font-weight: 700; line-height: 1.2; margin-bottom: 30px;'>{headline}</div>
  <div style='font-size: 150px; font-weight: 900; color: {primary_color}; line-height: 1; margin-bottom: 25px;'>{main_stat}</div>
  <div style='color: {subtext_color}; font-size: 32px; font-weight: 400; line-height: 1.5; max-width: 860px;'>{stat_label or subtitle}</div>
"""
        elif layout == "comparative_text" or (left_col and right_col):
            inner_html = f"""
  <div style='color: {primary_color}; font-size: 48px; font-weight: 800; line-height: 1.2; margin-bottom: 50px;'>{headline}</div>
  <div style='display: flex; gap: 40px; width: 100%; max-width: 920px; text-align: left;'>
    <div style='flex: 1; background: rgba(255, 75, 75, 0.08); border-left: 4px solid {accent_color}; padding: 30px; border-radius: 8px;'>
      <div style='color: {accent_color}; font-size: 24px; font-weight: 700; margin-bottom: 15px;'>AMATEUR / OLD</div>
      <div style='color: {text_color}; font-size: 26px; line-height: 1.5;'>{left_col}</div>
    </div>
    <div style='flex: 1; background: rgba(0, 229, 204, 0.08); border-left: 4px solid {primary_color}; padding: 30px; border-radius: 8px;'>
      <div style='color: {primary_color}; font-size: 24px; font-weight: 700; margin-bottom: 15px;'>PRO / NEW</div>
      <div style='color: {text_color}; font-size: 26px; line-height: 1.5;'>{right_col}</div>
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
                    items_html += f"<div style='color: {subtext_color}; font-size: 26px; margin-bottom: 14px;'>👉 {txt}</div>"
            eyebrow_tag = f"<div style='color: {accent_color}; font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px;'>{eyebrow}</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_tag}
  <div style='color: {primary_color}; font-size: 58px; font-weight: 900; line-height: 1.2; margin-bottom: 24px; max-width: 880px;'>{headline or 'Ready to Level Up?'}</div>
  {items_html}
  <div style='color: {subtext_color}; font-size: 28px; font-weight: 500; line-height: 1.5; max-width: 840px; margin: 30px 0 50px 0;'>{cta_highlight}</div>
  <div style='background: {primary_color}; color: {bg_color}; font-size: 28px; font-weight: 800; padding: 22px 55px; border-radius: 40px; text-transform: uppercase; letter-spacing: 1px;'>{cta_text}</div>
"""
        elif layout in ["concept_deepdive", "process_detail"] or slide.get("box1_title"):
            boxes_html = ""
            for b_idx in [1, 2, 3]:
                title = slide.get(f"box{b_idx}_title", "")
                body = slide.get(f"box{b_idx}_body", "")
                if title or body:
                    boxes_html += f"""
    <div style='background: rgba(255,255,255,0.03); border-left: 4px solid {primary_color if b_idx==1 else accent_color if b_idx==2 else subtext_color}; padding: 26px; border-radius: 12px; margin-bottom: 24px; text-align: left; width: 100%; max-width: 900px;'>
      <div style='color: {primary_color if b_idx==1 else accent_color if b_idx==2 else text_color}; font-size: 26px; font-weight: 700; margin-bottom: 10px;'>{title}</div>
      <div style='color: {subtext_color}; font-size: 24px; line-height: 1.5;'>{body}</div>
    </div>"""
            eyebrow_tag = f"<div style='color: {accent_color}; font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px;'>{eyebrow}</div>" if eyebrow else ""
            inner_html = f"""
  {eyebrow_tag}
  <div style='color: {text_color}; font-size: 46px; font-weight: 800; line-height: 1.2; margin-bottom: 35px; max-width: 900px;'>{headline}</div>
  <div style='width: 100%; display: flex; flex-direction: column; align-items: center;'>{boxes_html}</div>
"""
        else:
            # Default fallback
            inner_html = f"""
  <div style='color: {primary_color}; font-size: 52px; font-weight: 800; line-height: 1.2; margin-bottom: 40px; max-width: 900px;'>{headline}</div>
  <div style='color: {text_color}; font-size: 32px; font-weight: 400; line-height: 1.6; max-width: 880px; text-align: left; background: rgba(255,255,255,0.03); padding: 40px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08);'>{subtitle}</div>
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
