"""
V7 Template Engine — Produces V7-quality HTML from structured content data.
With V10 Macro-Level Layout Variants!
"""
import os
from pathlib import Path
from typing import Dict, List, Any
import re

# Path to shared CSS (relative from output HTML)
CSS_PATH = "v7_shared.css"

# Avoid circular imports, import dynamically if needed, or import at top
from src.visual.svg_variants import get_mesh, get_sparkline, get_flowchart_path, get_heatmap_html, ambient_glows, SVGRandom


def _brand_footer(slide_num: int = None, total: int = None) -> str:
    """Generate brand footer with optional slide count."""
    count = f'{slide_num:02d} / {total:02d}' if slide_num and total else "→"
    return f'''<div class="brand-footer">
    <div class="brand-logo">AIWITHSUFIYAN</div>
    <div class="slide-count">{count}</div>
  </div>'''


def _eyebrow(text: str, centered: bool = False, left_align: bool = False) -> str:
    """Generate eyebrow pill."""
    style = 'justify-content:center;' if centered else 'justify-content:flex-start;' if left_align else ''
    margin = 'margin: 0 auto;' if centered else 'margin: 0;' if left_align else ''
    return f'''<div class="eyebrow-container" style="{style}"><div class="eyebrow" style="{margin}">{text}</div></div>'''


def _source_citation(text: str, bottom: str = "120px") -> str:
    if not text:
        return ""
    return f'<div class="source-citation" style="bottom:{bottom};">{text}</div>'


# ═══════════════════════════════════════════════════
# LAYOUT 1: HERO — Massive title + SVGs
# ═══════════════════════════════════════════════════
def layout_hero(slide: Dict, slide_num: int, total: int, seed: str = "", variants: dict = None) -> str:
    if variants is None: variants = {}
    rng = SVGRandom(seed, slide_num + 10)
    struct_var = rng.rand_int(0, 2)
    mesh_v = variants.get("mesh", 0)

    eyebrow_text = slide.get("eyebrow", "")
    headline_top = slide.get("headline_top", "")  
    headline_accent = slide.get("headline_accent", "") 
    subtitle = slide.get("subtitle", "")
    source = slide.get("source", "")

    mesh_svg = get_mesh(seed, mesh_v)
    g1, g2 = ambient_glows(seed, mesh_v)

    if struct_var == 0:
        # Variant 0: The Classic Centered with Mesh
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  .hero-container {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; padding: 100px; text-align: center; }}
  .eyebrow-pill {{ display: inline-flex; align-items: center; gap: 12px; background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.08), rgba(255,255,255,0.03)); border: 1px solid rgba(255, 255, 255, 0.15); backdrop-filter: blur(20px); padding: 12px 24px; border-radius: 50px; box-shadow: 0 10px 40px rgba(0,229,204,0.1), inset 0 1px 0 rgba(255,255,255,0.3); margin-bottom: 50px; }}
  .eyebrow-text {{ font-size: 15px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; color: var(--accent-teal); text-shadow: 0 0 10px rgba(0,229,204,0.5); }}
  h1 .gradient-text {{ background: linear-gradient(180deg, #FFFFFF 0%, #A3A3A3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: block; }}
  h1 .accent {{ background: var(--highlight-orange); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-style: italic; letter-spacing: -3px; display: block; margin-top: 20px; filter: drop-shadow(0 0 15px rgba(255,107,53,0.4)); }}
  .subtitle {{ max-width: 650px; margin-top: 60px; z-index: 10; backdrop-filter: blur(10px); padding: 24px; border-radius: 20px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); }}
  .subtitle strong {{ color: #fff; font-weight: 700; }}
</style>
</head>
<body>
  <div class="topo-bg"></div>
  {g1}
  {g2}
  {mesh_svg}

  <div class="hero-container">
    <div class="eyebrow-pill">
      <div class="eyebrow-text">{eyebrow_text}</div>
    </div>
    <h1>
      <span class="gradient-text">{headline_top}</span>
      <span class="accent">{headline_accent}</span>
    </h1>
    <div class="subtitle">
      <p class="body-base">{subtitle}</p>
    </div>
  </div>
  {_brand_footer(slide_num, total)}
</body>
</html>'''

    elif struct_var == 1:
        # Variant 1: Left-aligned, massive typography, gradient background (No mesh)
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  body {{ background: linear-gradient(135deg, #0a0a0c 0%, #1a1a24 100%); }}
  .hero-container {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; z-index: 10; padding: 100px 80px; text-align: left; }}
  .eyebrow-pill {{ display: inline-flex; align-items: center; gap: 12px; background: rgba(0,229,204,0.1); border-left: 4px solid var(--accent-teal); padding: 12px 24px; margin-bottom: 40px; }}
  .eyebrow-text {{ font-size: 16px; font-weight: 900; letter-spacing: 4px; text-transform: uppercase; color: #fff; }}
  h1 {{ font-size: 140px; line-height: 0.9; letter-spacing: -4px; max-width: 900px; text-align: left; margin: 0; }}
  h1 .gradient-text {{ color: #fff; display: block; }}
  h1 .accent {{ color: var(--accent-teal); display: block; margin-top: 10px; text-shadow: 0 0 40px rgba(0,229,204,0.5); }}
  .subtitle {{ max-width: 700px; margin-top: 50px; z-index: 10; padding: 0; border-left: 2px solid rgba(255,255,255,0.2); padding-left: 24px; }}
  .subtitle p {{ font-size: 32px; color: #D4D4D8; line-height: 1.5; font-weight: 400; }}
  .sub-glow {{ position: absolute; bottom: 0; right: 0; width: 800px; height: 800px; background: radial-gradient(circle, var(--accent-teal-dim) 0%, transparent 70%); filter: blur(100px); opacity: 0.8; z-index: 1; }}
</style>
</head>
<body>
  <div class="sub-glow"></div>
  <div class="hero-container">
    <div class="eyebrow-pill">
      <div class="eyebrow-text">{eyebrow_text}</div>
    </div>
    <h1>
      <span class="gradient-text">{headline_top}</span>
      <span class="accent">{headline_accent}</span>
    </h1>
    <div class="subtitle">
      <p>{subtitle}</p>
    </div>
  </div>
  {_brand_footer(slide_num, total)}
</body>
</html>'''

    else:
        # Variant 2: Bottom-aligned block over tech grid
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  .grid-bg {{ position: absolute; inset: 0; background-image: linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px); background-size: 50px 50px; z-index: 2; opacity: 0.5; }}
  .hero-container {{ position: absolute; bottom: 150px; left: 80px; right: 80px; display: flex; flex-direction: column; justify-content: flex-end; align-items: flex-start; z-index: 10; background: rgba(15,15,20,0.85); backdrop-filter: blur(24px); border: 1px solid rgba(255,255,255,0.1); border-radius: 40px; padding: 60px; box-shadow: 0 30px 80px rgba(0,0,0,0.8); }}
  .eyebrow-text {{ font-size: 18px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; color: var(--highlight-orange); margin-bottom: 20px; }}
  h1 {{ font-size: 100px; line-height: 1; letter-spacing: -2px; text-align: left; margin: 0; }}
  h1 .gradient-text {{ color: #fff; display: inline; }}
  h1 .accent {{ color: var(--accent-teal); display: inline; }}
  .subtitle {{ max-width: 800px; margin-top: 30px; }}
  .subtitle p {{ font-size: 28px; color: #A1A1AA; line-height: 1.6; font-weight: 500; }}
</style>
</head>
<body>
  <div class="topo-bg"></div>
  <div class="grid-bg"></div>
  {g1}
  {mesh_svg}

  <div class="hero-container">
    <div class="eyebrow-text">{eyebrow_text}</div>
    <h1>
      <span class="gradient-text">{headline_top}</span>
      <span class="accent">{headline_accent}</span>
    </h1>
    <div class="subtitle">
      <p>{subtitle}</p>
    </div>
  </div>
  {_brand_footer(slide_num, total)}
</body>
</html>'''


# ═══════════════════════════════════════════════════
# LAYOUT 2: BENTO — 3-tier grid with glass cards
# ═══════════════════════════════════════════════════
def layout_bento(slide: Dict, slide_num: int, total: int, seed: str = "", variants: dict = None) -> str:
    if variants is None: variants = {}
    rng = SVGRandom(seed, slide_num + 20)
    struct_var = rng.rand_int(0, 1)

    eyebrow_text = slide.get("eyebrow", "")
    headline = slide.get("headline", "")
    headline_accent = slide.get("headline_accent", "")
    source = slide.get("source", "")
    main_stat = slide.get("main_stat", "0")
    main_stat_suffix = slide.get("main_stat_suffix", "")
    main_label = slide.get("main_label", "")
    main_desc = slide.get("main_desc", "")
    stat2_value = slide.get("stat2_value", "")
    stat2_label = slide.get("stat2_label", "")
    stat3_value = slide.get("stat3_value", "")
    stat3_label = slide.get("stat3_label", "")
    insight_icon = slide.get("insight_icon", "⚡")
    insight_text = slide.get("insight_text", "")

    sparkline_svg = get_sparkline(seed, variants.get("sparkline", 0))
    heatmap_html = get_heatmap_html(seed, slide_num, 3, 8)
    g1, g2 = ambient_glows(seed, slide_num)

    if struct_var == 0:
        # Standard Bento (2 cols, 3 rows)
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  h2 em {{ font-style: normal; color: var(--accent-teal); }}
  .bento-grid {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto 1fr 1fr; gap: 24px; z-index: 10; flex: 1; min-height: 0; margin-top: 40px; }}
  .c-main {{ grid-column: 1 / span 2; grid-row: 1; justify-content: space-between; border: 1px solid rgba(0,229,204,0.3); background: rgba(0,229,204,0.02); overflow: hidden; }}
  .cm-label {{ font-size: 16px; font-weight: 700; color: var(--accent-teal); text-transform: uppercase; letter-spacing: 2px; }}
  .cm-stat {{ font-size: 150px; font-weight: 900; line-height: 0.8; letter-spacing: -6px; color: #fff; margin: 32px 0; text-shadow: 0 10px 40px rgba(0,229,204,0.4); }}
  .c-metric {{ grid-column: 1; grid-row: 2; justify-content: center; overflow: hidden; }}
  .heatmap {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 6px; margin-bottom: 24px; }}
  .heat-cell {{ height: 24px; border-radius: 4px; background: rgba(255,255,255,0.05); }}
  .heat-active {{ background: var(--accent-teal); box-shadow: 0 0 10px var(--accent-teal); }}
  .c-highlight {{ grid-column: 2; grid-row: 2; justify-content: center; background: rgba(255,107,53,0.05); border-color: rgba(255,107,53,0.2); overflow: hidden; }}
  .ch-stat {{ font-size: 72px; font-weight: 900; color: var(--highlight-orange); letter-spacing: -3px; line-height: 1; margin-bottom: 16px; text-shadow: 0 10px 30px rgba(255,107,53,0.4); }}
  .c-insight {{ grid-column: 1 / span 2; grid-row: 3; justify-content: center; flex-direction: row; align-items: center; gap: 32px; padding: 32px 48px; overflow: hidden; }}
  .ci-icon {{ font-size: 48px; color: var(--accent-teal); }}
  .ci-text {{ font-size: 22px; color: #E5E7EB; line-height: 1.5; font-weight: 500; }}
  .ci-text strong {{ color: var(--accent-teal); }}
</style>
</head>
<body>
  <div class="topo-bg"></div>
  {g1}
  <div class="layout-wrapper">
    <div>
      {_eyebrow(eyebrow_text)}
      <h2>{headline} <em>{headline_accent}</em></h2>
    </div>
    <div class="bento-grid">
      <div class="glass-card c-main">
        <div class="cm-label">{main_label}</div>
        <div class="cm-stat">{main_stat}<span style="font-size: 72px; color: var(--accent-teal); vertical-align: top;">{main_stat_suffix}</span></div>
        <p class="body-base" style="position: relative; z-index: 10; max-width: 400px;">{main_desc}</p>
        {sparkline_svg}
      </div>
      <div class="glass-card c-metric">
        {heatmap_html}
        <p class="body-base"><span style="color: var(--accent-teal); font-weight: 800; font-size: 32px; letter-spacing: -1px;">{stat2_value}</span><br>{stat2_label}</p>
      </div>
      <div class="glass-card c-highlight">
        <div class="ch-stat">{stat3_value}</div>
        <p class="body-base">{stat3_label}</p>
      </div>
      <div class="glass-card c-insight">
        <div class="ci-icon">{insight_icon}</div>
        <p class="body-large ci-text">{insight_text}</p>
      </div>
    </div>
  </div>
  {_source_citation(source)}
  {_brand_footer(slide_num, total)}
</body>
</html>'''

    else:
        # Variant 1: Asymmetric Bento (Left column big, right column stacked)
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  h2 em {{ font-style: normal; color: var(--highlight-orange); }}
  .bento-grid {{ display: grid; grid-template-columns: 1.5fr 1fr; grid-template-rows: 1fr 1fr; gap: 24px; z-index: 10; flex: 1; min-height: 0; margin-top: 40px; }}
  .c-main {{ grid-column: 1; grid-row: 1 / span 2; justify-content: flex-start; border: 1px solid rgba(0,229,204,0.4); background: rgba(0,229,204,0.05); overflow: hidden; padding: 60px; }}
  .cm-label {{ font-size: 18px; font-weight: 800; color: var(--accent-teal); text-transform: uppercase; letter-spacing: 3px; margin-bottom: 20px; }}
  .cm-stat {{ font-size: 160px; font-weight: 900; line-height: 0.9; letter-spacing: -8px; color: #fff; margin: 0 0 40px 0; }}
  .c-metric {{ grid-column: 2; grid-row: 1; justify-content: center; overflow: hidden; }}
  .heatmap {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 6px; margin-bottom: 24px; }}
  .heat-cell {{ height: 24px; border-radius: 4px; background: rgba(255,255,255,0.05); }}
  .heat-active {{ background: var(--accent-teal); box-shadow: 0 0 10px var(--accent-teal); }}
  .c-highlight {{ grid-column: 2; grid-row: 2; justify-content: center; background: rgba(255,107,53,0.08); border-color: rgba(255,107,53,0.3); overflow: hidden; }}
  .ch-stat {{ font-size: 80px; font-weight: 900; color: var(--highlight-orange); letter-spacing: -4px; line-height: 1; margin-bottom: 16px; }}
  .ci-insight-embedded {{ margin-top: auto; padding: 30px; background: rgba(0,0,0,0.3); border-radius: 20px; border-left: 4px solid var(--accent-teal); }}
  .ci-text {{ font-size: 20px; color: #E5E7EB; line-height: 1.5; font-weight: 500; }}
</style>
</head>
<body>
  <div class="topo-bg"></div>
  {g2}
  <div class="layout-wrapper">
    <div style="text-align: left;">
      {_eyebrow(eyebrow_text, left_align=True)}
      <h2 style="text-align: left;">{headline} <em>{headline_accent}</em></h2>
    </div>
    <div class="bento-grid">
      <div class="glass-card c-main">
        <div class="cm-label">{main_label}</div>
        <div class="cm-stat">{main_stat}<span style="font-size: 60px; color: var(--accent-teal); vertical-align: super;">{main_stat_suffix}</span></div>
        <p class="body-base" style="position: relative; z-index: 10; margin-bottom: 40px;">{main_desc}</p>
        <div class="ci-insight-embedded">
          <p class="ci-text">{insight_icon} {insight_text}</p>
        </div>
        {sparkline_svg}
      </div>
      <div class="glass-card c-metric">
        {heatmap_html}
        <p class="body-base"><span style="color: var(--accent-teal); font-weight: 800; font-size: 40px; letter-spacing: -2px;">{stat2_value}</span><br>{stat2_label}</p>
      </div>
      <div class="glass-card c-highlight">
        <div class="ch-stat">{stat3_value}</div>
        <p class="body-base">{stat3_label}</p>
      </div>
    </div>
  </div>
  {_source_citation(source)}
  {_brand_footer(slide_num, total)}
</body>
</html>'''


# ═══════════════════════════════════════════════════
# LAYOUT 3: FLOWCHART — Vertical timeline
# ═══════════════════════════════════════════════════
def layout_flowchart(slide: Dict, slide_num: int, total: int, seed: str = "", variants: dict = None) -> str:
    if variants is None: variants = {}
    eyebrow_text = slide.get("eyebrow", "")
    headline = slide.get("headline", "")
    headline_accent = slide.get("headline_accent", "")
    source = slide.get("source", "")
    nodes = slide.get("nodes", []) 
    badge_value = slide.get("badge_value", "")
    badge_label = slide.get("badge_label", "")

    badge_html = f'''<div class="roi-badge">
      {badge_value}
      <span class="roi-sub">{badge_label}</span>
    </div>''' if badge_value else ""

    nodes_html = ""
    offsets = [0, -480, 0, 480, -480]
    for i, node in enumerate(nodes):
        active_class = " active" if node.get("active") else ""
        ml = f" margin-left: {offsets[i % len(offsets)]}px;" if node.get("active") else ""
        nodes_html += f'''<div class="node{active_class}" style="{ml}">
        <div class="n-icon">{i+1}</div>
        <div class="n-text">{node['text']}</div>
      </div>\n'''

    flowchart_svg = get_flowchart_path(seed, variants.get("flowchart", 0))
    g1, g2 = ambient_glows(seed, slide_num)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  body {{ text-align: center; }}
  h2 em {{ font-style: normal; color: var(--accent-teal); }}
  .timeline-container {{ flex: 1; position: relative; z-index: 10; display: flex; align-items: center; justify-content: center; min-height: 0; margin-top: 40px; }}
  .nodes-layer {{ position: absolute; inset: 0; z-index: 2; display: flex; flex-direction: column; align-items: center; justify-content: space-between; padding: 40px 0; }}
  .node {{ background: rgba(20,20,20,0.8); border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(16px); padding: 24px 40px; border-radius: 100px; display: flex; align-items: center; gap: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.6); position: relative; }}
  .node.active {{ border-color: var(--accent-teal); background: rgba(0,229,204,0.05); box-shadow: 0 15px 50px rgba(0,229,204,0.2), inset 0 0 20px rgba(0,229,204,0.1); transform: scale(1.1); }}
  .n-icon {{ width: 48px; height: 48px; background: rgba(255,255,255,0.05); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 800; color: var(--text-muted); }}
  .active .n-icon {{ background: rgba(0,229,204,0.2); color: var(--accent-teal); box-shadow: 0 0 20px rgba(0,229,204,0.5); }}
  .n-text {{ font-size: 22px; font-weight: 700; color: #fff; letter-spacing: -0.5px; }}
  .roi-badge {{ position: absolute; top: 50%; right: 100px; transform: translateY(-50%); background: var(--highlight-orange); color: #000; font-size: 72px; font-weight: 900; letter-spacing: -3px; padding: 24px 40px; border-radius: 32px; box-shadow: 0 20px 60px rgba(255,107,53,0.5); text-align: center; }}
  .roi-sub {{ display: block; font-size: 16px; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; opacity: 0.9; margin-top: 8px; }}
</style>
</head>
<body>
  <div class="topo-bg"></div>
  {g1}
  <div class="layout-wrapper">
    <div style="text-align: center;">
      {_eyebrow(eyebrow_text, centered=True)}
      <h2>{headline} <em>{headline_accent}</em></h2>
    </div>
    <div class="timeline-container">
    {flowchart_svg}
    <div class="nodes-layer">
      {nodes_html}
    </div>
    {badge_html}
  </div>
  </div>
  {_source_citation(source)}
  {_brand_footer(slide_num, total)}
</body>
</html>'''


# ═══════════════════════════════════════════════════
# LAYOUT 4: SPLIT — 50/50 vertical or horizontal
# ═══════════════════════════════════════════════════
def layout_split(slide: Dict, slide_num: int, total: int, seed: str = "", variants: dict = None) -> str:
    if variants is None: variants = {}
    rng = SVGRandom(seed, slide_num + 30)
    struct_var = rng.rand_int(0, 1)

    eyebrow_text = slide.get("eyebrow", "")
    headline = slide.get("headline", "")
    headline_accent = slide.get("headline_accent", "")
    body_text = slide.get("body_text", "")
    source = slide.get("source", "")
    stat_value = slide.get("stat_value", "+202%")
    stat_label = slide.get("stat_label", "Higher Engagement")
    insight_text = slide.get("insight_text", "")
    g1, g2 = ambient_glows(seed, slide_num)

    if struct_var == 0:
        # Standard Top/Bottom Split
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  body {{ padding: 0; }}
  .top-pane {{ width: 100%; height: 50%; padding: 100px 80px; display: flex; flex-direction: column; justify-content: center; position: relative; z-index: 10; }}
  .bottom-pane {{ width: 100%; height: 50%; position: relative; background: #15151A; border-top: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 80px; }}
  .grid-bg {{ position: absolute; inset: 0; background-image: radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px); background-size: 8px 8px; opacity: 0.3; z-index: 2; }}
  h2 em {{ font-style: normal; color: var(--accent-teal); }}
  .top-text-wrapper {{ max-width: 800px; margin: 0 auto; text-align: center; }}
  .data-container {{ position: relative; z-index: 10; display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%; }}
  .massive-stat {{ font-size: min(180px, 15vw); font-weight: 900; line-height: 0.85; letter-spacing: -10px; color: #fff; text-shadow: 0 20px 60px rgba(0,229,204,0.4); margin-bottom: 30px; }}
  .massive-stat span {{ color: var(--accent-teal); font-size: min(90px, 8vw); vertical-align: top; }}
  .stat-label {{ background: rgba(0,229,204,0.1); border: 1px solid rgba(0,229,204,0.3); padding: 16px 32px; border-radius: 50px; font-size: 18px; font-weight: 800; text-transform: uppercase; letter-spacing: 4px; color: var(--accent-teal); }}
  .insight-card {{ margin-top: 40px; max-width: 700px; background: rgba(255,255,255,0.02); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); padding: 40px; border-radius: 32px; text-align: left; }}
  .ic-text {{ font-size: 22px; color: #E5E7EB; line-height: 1.6; font-weight: 500; }}
</style>
</head>
<body>
  <div class="top-pane">
    <div class="topo-bg"></div>
    {g1}
    <div class="top-text-wrapper">
      {_eyebrow(eyebrow_text, centered=True)}
      <h2>{headline}<br><em>{headline_accent}</em></h2>
      {f'<p class="body-large" style="margin-top: 32px;">{body_text}</p>' if body_text else ''}
    </div>
  </div>
  <div class="bottom-pane">
    <div class="grid-bg"></div>
    {g2}
    <div class="data-container">
      <div class="massive-stat">{stat_value}</div>
      <div class="stat-label">{stat_label}</div>
      {'<div class="insight-card"><p class="ic-text">' + insight_text + '</p></div>' if insight_text else ''}
    </div>
    {_source_citation(source, "40px")}
    {_brand_footer(slide_num, total)}
  </div>
</body>
</html>'''

    else:
        # Variant 1: Left/Right Horizontal Split
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  body {{ padding: 0; display: flex; flex-direction: row; }}
  .left-pane {{ width: 50%; height: 100%; padding: 100px 60px; display: flex; flex-direction: column; justify-content: center; position: relative; z-index: 10; border-right: 1px solid rgba(255,255,255,0.1); }}
  .right-pane {{ width: 50%; height: 100%; position: relative; background: #15151A; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 60px; }}
  .grid-bg {{ position: absolute; inset: 0; background-image: radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px); background-size: 8px 8px; opacity: 0.3; z-index: 2; }}
  h2 {{ text-align: left; font-size: 64px; line-height: 1.1; }}
  h2 em {{ font-style: normal; color: var(--highlight-orange); display: block; margin-top: 10px; }}
  .data-container {{ position: relative; z-index: 10; display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%; }}
  .massive-stat {{ font-size: 140px; font-weight: 900; line-height: 0.9; letter-spacing: -6px; color: var(--accent-teal); text-shadow: 0 20px 50px rgba(0,229,204,0.3); margin-bottom: 30px; word-break: break-word; }}
  .stat-label {{ background: rgba(255,107,53,0.1); border: 1px solid rgba(255,107,53,0.3); padding: 16px 32px; border-radius: 50px; font-size: 16px; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; color: var(--highlight-orange); margin-bottom: 40px; }}
  .insight-card {{ width: 100%; background: rgba(0,0,0,0.3); border-left: 4px solid var(--accent-teal); padding: 30px; text-align: left; }}
  .ic-text {{ font-size: 20px; color: #E5E7EB; line-height: 1.6; font-weight: 500; }}
</style>
</head>
<body>
  <div class="left-pane">
    <div class="topo-bg"></div>
    {g1}
    {_eyebrow(eyebrow_text, left_align=True)}
    <h2>{headline} <em>{headline_accent}</em></h2>
    {f'<p class="body-large" style="margin-top: 32px; text-align: left;">{body_text}</p>' if body_text else ''}
    <div class="brand-footer" style="bottom: 40px; left: 60px;">
      <div class="brand-logo">AIWITHSUFIYAN</div>
      <div class="slide-count">{slide_num:02d} / {total:02d}</div>
    </div>
  </div>
  <div class="right-pane">
    <div class="grid-bg"></div>
    {g2}
    <div class="data-container">
      <div class="massive-stat">{stat_value}</div>
      <div class="stat-label">{stat_label}</div>
      {'<div class="insight-card"><p class="ic-text">' + insight_text + '</p></div>' if insight_text else ''}
    </div>
    {_source_citation(source, "40px")}
  </div>
</body>
</html>'''


# ═══════════════════════════════════════════════════
# LAYOUT 5: GRID — 4-panel glassmorphism
# ═══════════════════════════════════════════════════
def layout_grid(slide: Dict, slide_num: int, total: int, seed: str = "", variants: dict = None) -> str:
    if variants is None: variants = {}
    eyebrow_text = slide.get("eyebrow", "")
    headline = slide.get("headline", "")
    headline_accent = slide.get("headline_accent", "")
    source = slide.get("source", "")
    panels = slide.get("panels", [])
    while len(panels) < 4:
        panels.append({"icon": "📌", "title": "", "body": "", "accent": "teal"})
    panels_html = ""
    for i, p in enumerate(panels[:4]):
        accent = "var(--accent-teal)" if p.get("accent", "teal") == "teal" else "var(--highlight-orange)"
        panels_html += f'''<div class="glass-card grid-cell">
        <div class="gc-icon" style="color:{accent}; font-size: 48px; margin-bottom: 24px;">{p.get('icon', '📌')}</div>
        <h3 style="color:{accent}; margin-bottom: 16px;">{p.get('title', '')}</h3>
        <p class="body-base">{p.get('body', '')}</p>
      </div>\n'''
    g1, g2 = ambient_glows(seed, slide_num)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  h2 em {{ font-style: normal; color: var(--accent-teal); }}
  .data-grid {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 24px; z-index: 10; flex: 1; min-height: 0; margin-top: 40px; }}
  .grid-cell {{ display: flex; flex-direction: column; justify-content: center; }}
  .grid-cell h3 {{ font-size: 28px; font-weight: 800; line-height: 1.2; }}
</style>
</head>
<body>
  <div class="topo-bg"></div>
  {g1}
  <div class="layout-wrapper">
    <div>
      {_eyebrow(eyebrow_text)}
      <h2>{headline} <em>{headline_accent}</em></h2>
    </div>
    <div class="data-grid">
      {panels_html}
    </div>
  </div>
  {_source_citation(source)}
  {_brand_footer(slide_num, total)}
</body>
</html>'''


# ═══════════════════════════════════════════════════
# LAYOUT 6: OUTRO
# ═══════════════════════════════════════════════════
def layout_outro(slide: Dict, slide_num: int, total: int, seed: str = "", variants: dict = None) -> str:
    if variants is None: variants = {}
    eyebrow_text = slide.get("eyebrow", "The Bottom Line")
    headline = slide.get("headline", "AI is the engine.")
    headline_accent = slide.get("headline_accent", "driver.")
    items = slide.get("items", [])
    cta_text = slide.get("cta_text", "Save this post.")
    cta_highlight = slide.get("cta_highlight", "You'll need these stats.")
    cta_icon = slide.get("cta_icon", "📌")
    items_html = ""
    for i, item in enumerate(items[:3], 1):
        items_html += f'''<div class="l-item">
        <div class="l-num">{i:02d}.</div>
        <div class="l-text">{item.get('text', '')}</div>
      </div>\n'''
    g1, g2 = ambient_glows(seed, slide_num)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  body {{ align-items: center; justify-content: center; text-align: center; }}
  .center-glow {{ position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); width: 700px; height: 700px; background: radial-gradient(circle, var(--accent-teal-dim) 0%, transparent 60%); filter: blur(60px); border-radius: 50%; z-index: 1; }}
  .content {{ position: relative; z-index: 10; width: 100%; max-width: 850px; }}
  h2 {{ margin-bottom: 80px; }}
  h2 span {{ color: var(--accent-teal); }}
  .list-container {{ text-align: left; display: flex; flex-direction: column; gap: 48px; margin-bottom: 80px; }}
  .l-item {{ display: flex; align-items: flex-start; gap: 40px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 48px; }}
  .l-item:last-child {{ border-bottom: none; }}
  .l-num {{ font-size: 32px; font-weight: 900; color: var(--accent-teal); letter-spacing: -1px; font-family: monospace; margin-top: 4px; }}
  .l-text {{ font-size: 32px; font-weight: 500; color: #D4D4D8; line-height: 1.5; letter-spacing: -0.5px; }}
  .l-text strong {{ color: #fff; font-weight: 800; }}
  .cta-box {{ background: rgba(255,107,53,0.1); border: 1px solid rgba(255,107,53,0.3); border-radius: 32px; padding: 40px; text-align: center; box-shadow: 0 20px 40px rgba(255,107,53,0.15); display: flex; flex-direction: column; align-items: center; gap: 16px; }}
  .cta-icon {{ font-size: 48px; }}
  .cta-text {{ font-size: 28px; font-weight: 800; color: #fff; }}
  .cta-text span {{ color: var(--highlight-orange); }}
  .trailing-light {{ position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 400px; height: 3px; background: linear-gradient(90deg, transparent, var(--accent-teal), transparent); box-shadow: 0 -10px 40px rgba(0,229,204,0.6); }}
</style>
</head>
<body>
  <div class="topo-bg"></div>
  <div class="center-glow"></div>
  {g1}
  <div class="content">
    {_eyebrow(eyebrow_text, centered=True)}
    <h2>{headline}<br><span>{headline_accent}</span></h2>
    <div class="list-container">
      {items_html}
    </div>
    <div class="cta-box">
      <div class="cta-icon">{cta_icon}</div>
      <div class="cta-text">{cta_text} <span>{cta_highlight}</span></div>
    </div>
  </div>
  <div class="brand-footer" style="bottom: 80px;">
    <div class="brand-logo">AIWITHSUFIYAN</div>
  </div>
  <div class="trailing-light"></div>
</body>
</html>'''


# ═══════════════════════════════════════════════════
# TEMPLATE ENGINE
# ═══════════════════════════════════════════════════
LAYOUT_MAP = {
    "hero": layout_hero,
    "bento": layout_bento,
    "flowchart": layout_flowchart,
    "split": layout_split,
    "grid": layout_grid,
    "outro": layout_outro,
}

LAYOUT_DIVERSE_ORDER = ["hero", "bento", "flowchart", "split", "grid", "outro"]

# ═══════════════════════════════════════════════
# V8 VARIANT RENDERER
# ═══════════════════════════════════════════════
def render_carousel_v8(slides: list, seed: str = "", variants: dict = None) -> list:
    if variants is None:
        variants = {"mesh": 0, "sparkline": 0, "flowchart": 0}

    total = len(slides)
    rendered = []
    prev_layout = None

    for i, slide in enumerate(slides):
        layout = slide.get("layout", "hero")
        if layout == prev_layout:
            for alt in LAYOUT_DIVERSE_ORDER:
                if alt != layout:
                    slide["layout"] = alt
                    layout = alt
                    break
        prev_layout = layout

        # Get layout function and pass seed and variants directly
        func = LAYOUT_MAP.get(layout, layout_hero)
        html = func(slide, i + 1, total, seed=seed, variants=variants)
        
        rendered.append(html)

    return rendered

def save_carousel(slides_html: List[str], output_dir: str, prefix: str = "slide") -> list:
    """Save rendered HTML slides to disk."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, html in enumerate(slides_html, 1):
        fname = f"{prefix}_{i:02d}.html"
        fpath = out / fname
        fpath.write_text(html, encoding="utf-8")
        paths.append(str(fpath))
    return paths
