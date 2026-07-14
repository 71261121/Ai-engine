"""
Level 100x God-Tier Visual Compositor (1080x1350).
Synthesizes exact 1:1 replicas of the 2026/2027 Benchmark Studio Slides using
Rust-powered @resvg/resvg-js engine + dynamic SVG architecture primitives across
ALL 10 V7 & V11 LAYOUT ARCHETYPES:
- `hero` (Isometric 3D Geometry Wireframe Grids with glowing cyan vertices)
- `bento` (3-Tier Glass Bento Grid with massive metrics and glowing insight pills)
- `flowchart` (Interconnected node pipelines + glowing stat badges)
- `split` (50/50 Magazine split matrices + strategic developer insights)
- `grid` (4-Panel Glassmorphism 2x2 grid exact to studio layout specs)
- `stat_highlight` / `comparative_text` / `concept_deepdive` / `process_detail` / `outro`
"""
import json
import re
import shutil
import subprocess
import textwrap
from pathlib import Path
from typing import List, Dict, Any, Optional
from .topic_dna import get_topic_dna
from .svg_flow_engine import SVGFlowEngine


class NextGenRenderer:
    """
    Level 100x Renderer using @resvg/resvg-js Rust bridge for benchmark-exact PNG & HTML synthesis across V7 & V11.
    """

    ARCHETYPES = {
        "cyber_dark": {"background": "#0D0E11", "primary": "#00E5CC", "accent": "#FF5F2E", "text": "#FFFFFF", "subtext": "#C4C4CC", "card_bg": "#14161C"},
        "minimalist_white": {"background": "#FAFAFA", "primary": "#2563EB", "accent": "#DC2626", "text": "#18181B", "subtext": "#52525B", "card_bg": "#F4F4F5"},
        "monokai_code": {"background": "#141416", "primary": "#A6E22E", "accent": "#F92672", "text": "#F8F8F2", "subtext": "#94949C", "card_bg": "#22242C"},
        "brutalist_swiss": {"background": "#FACC15", "primary": "#000000", "accent": "#DC2626", "text": "#000000", "subtext": "#27272A", "card_bg": "#FFFFFF"},
        "infrastructure_blue": {"background": "#080C14", "primary": "#38BDF8", "accent": "#F59E0B", "text": "#F9FAFB", "subtext": "#9CA3AF", "card_bg": "#101826"}
    }

    def __init__(self):
        self.has_node = shutil.which("node") is not None
        self.bridge_path = Path(__file__).resolve().parent / "svg_to_png.js"

    def _clean_txt(self, text: Any) -> str:
        if not text:
            return ""
        cleaned = re.sub(r'<[^>]+>', '', str(text))
        cleaned = cleaned.replace('"', "'").replace('`', "'").replace('$', "").strip()
        return cleaned

    def _wrap(self, text: str, width: int) -> str:
        if not text:
            return ""
        return textwrap.fill(self._clean_txt(text), width=width)

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
        if self.has_node:
            png_dir.mkdir(parents=True, exist_ok=True)

        for idx, slide in enumerate(slides, 1):
            file_path = output_dir / f"slide_{idx:02d}.html"
            html_content = self._render_slide_html(slide, idx, total_slides, colors)
            file_path.write_text(html_content, encoding="utf-8")
            rendered_paths.append(file_path)

            if self.has_node and self.bridge_path.exists():
                png_path = output_dir / f"slide_{idx:02d}.png"
                self._render_slide_png_resvg(slide, idx, total_slides, colors, png_path, topic)
                if png_path.exists():
                    png_paths.append(png_path)
                    try:
                        shutil.copy2(png_path, png_dir / f"slide_{idx:02d}.png")
                    except Exception:
                        pass

        package_file = output_dir / "carousel_data.json"
        package_data = {
            "topic": topic,
            "version": "v100.0_v7_v11_god_tier",
            "topic_dna": topic_dna,
            "archetype_used": archetype or topic_dna.get("category", "cyber_dark"),
            "slides": slides,
            "slide_files": [p.name for p in rendered_paths],
            "png_files": [p.name for p in png_paths]
        }
        package_file.write_text(json.dumps(package_data, indent=2, ensure_ascii=False), encoding="utf-8")

        return rendered_paths

    def _render_slide_html(self, slide: Dict[str, Any], slide_num: int, total_slides: int, colors: Dict[str, str]) -> str:
        bg_color = colors["background"]
        primary_color = colors["primary"]
        text_color = colors["text"]
        subtext_color = colors["subtext"]
        card_bg = colors.get("card_bg", "#14161C")

        headline = slide.get("headline", "") or slide.get("eyebrow", "Overview")
        subtitle = slide.get("subtitle", "") or slide.get("main_desc", "")

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ width: 1080px; height: 1350px; font-family: 'Inter', -apple-system, sans-serif; overflow: hidden; background: {bg_color}; color: {text_color}; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 80px; }}
.card {{ background: {card_bg}; border: 1px solid rgba(0, 229, 204, 0.3); border-radius: 24px; padding: 40px; margin: 20px 0; max-width: 920px; }}
.brand {{ position: absolute; bottom: 45px; left: 0; right: 0; font-size: 16px; font-weight: 800; letter-spacing: 4px; text-transform: uppercase; color: {text_color}; opacity: 0.6; text-anchor: middle; }}
.slide_num {{ position: absolute; bottom: 45px; right: 60px; font-size: 16px; font-weight: 800; color: {primary_color}; }}
</style>
</head>
<body>
  <div style="color: {primary_color}; font-size: 64px; font-weight: 900; margin-bottom: 30px;">{headline}</div>
  <div class="card" style="font-size: 32px; color: {subtext_color}; line-height: 1.5;">{subtitle}</div>
  <div class="brand">AIWITHSUFIYAN →</div>
  <div class="slide_num">{slide_num:02d} / {total_slides:02d}</div>
</body>
</html>"""

    def _render_slide_png_resvg(self, slide: Dict[str, Any], slide_num: int, total_slides: int, colors: Dict[str, str], output_png: Path, topic: str):
        bg_color = colors["background"]
        primary_color = colors["primary"]
        accent_color = colors["accent"]
        text_color = colors["text"]
        subtext_color = colors["subtext"]
        card_bg = colors.get("card_bg", "#14161C")

        layout = slide.get("layout", "concept_deepdive").lower()
        headline = self._clean_txt(slide.get("headline", "") or (slide.get("headline_top", "") + " " + slide.get("headline_accent", "")).strip() or slide.get("eyebrow", "Overview"))
        eyebrow = self._clean_txt(slide.get("eyebrow", ""))
        subtitle = self._clean_txt(slide.get("subtitle", "") or slide.get("main_desc", ""))

        svg_defs = f"""
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_color}" />
      <stop offset="50%" stop-color="#12141F" />
      <stop offset="100%" stop-color="{bg_color}" />
    </linearGradient>
    <radialGradient id="cyan-glow" cx="50%" cy="40%" r="50%">
      <stop offset="0%" stop-color="{primary_color}" stop-opacity="0.28" />
      <stop offset="100%" stop-color="{primary_color}" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="orange-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent_color}" stop-opacity="0.25" />
      <stop offset="100%" stop-color="{accent_color}" stop-opacity="0" />
    </radialGradient>
  </defs>
  <rect width="1080" height="1350" fill="url(#bg)" />
  <circle cx="540" cy="450" r="420" fill="url(#cyan-glow)" />"""

        svg_content = ""

        if layout == "hero" or slide_num == 1:
            wireframe = SVGFlowEngine.generate_isometric_wireframe(primary_color, accent_color)
            eb_txt = eyebrow or "SOFTWARE ARCHITECTURE 101"
            words = headline.split()
            hl_top = slide.get("headline_top", "") or (" ".join(words[:len(words)//2]) if len(words) > 1 else "TYPES OF")
            hl_bottom = slide.get("headline_accent", "") or (" ".join(words[len(words)//2:]) if len(words) > 1 else "APIs.")
            if not hl_bottom.endswith("."):
                hl_bottom += "."

            w_sub = self._wrap(subtitle or f"{topic} are the backbone of modern applications. Let's look at the 6 most important types you need to know in 2026.", 58)
            sub_lines = w_sub.splitlines()
            sub_svg = ""
            for idx_l, l_txt in enumerate(sub_lines):
                fw = "900" if idx_l == 1 else "500"
                fc = "#FFFFFF" if idx_l == 1 else subtext_color
                sub_svg += f'<text x="450" y="{65 + idx_l*46}" font-family="Inter, sans-serif" font-size="30" font-weight="{fw}" fill="{fc}" text-anchor="middle">{l_txt}</text>'

            svg_content = f"""
  {wireframe}
  <g transform="translate(390, 160)">
    <rect width="300" height="44" rx="22" fill="rgba(0,229,204,0.08)" stroke="{primary_color}" stroke-width="2"/>
    <text x="150" y="28" font-family="Inter, sans-serif" font-size="15" font-weight="800" fill="{primary_color}" text-anchor="middle" letter-spacing="2">{eb_txt.upper()}</text>
  </g>
  <text x="540" y="390" font-family="Inter, sans-serif" font-size="105" font-weight="900" fill="#FFFFFF" text-anchor="middle" letter-spacing="-2">{self._clean_txt(hl_top).upper()}</text>
  <text x="540" y="505" font-family="Inter, sans-serif" font-size="115" font-weight="900" fill="none" stroke="{accent_color}" stroke-width="4" text-anchor="middle" letter-spacing="-2">{self._clean_txt(hl_bottom).upper()}</text>
  <g transform="translate(90, 710)">
    <rect width="900" height="210" rx="24" fill="{card_bg}" stroke="rgba(0,229,204,0.3)" stroke-width="2"/>
    {sub_svg}
  </g>"""

        elif layout == "bento":
            # V7 Bento Grid Layout (3-tier bento grid with sparkline/insight cards)
            eb_txt = eyebrow or "Visual Volume"
            hl_txt = headline or "The Baseline has Shifted."
            main_stat = self._clean_txt(slide.get("main_stat", "34M+"))
            main_lbl = self._clean_txt(slide.get("main_label", "DAILY AI OUTPUT"))
            main_dsc = self._wrap(slide.get("main_desc", subtitle or "Images and requests generated across major platforms every 24 hours."), 46)
            s2_val = self._clean_txt(slide.get("stat2_value", "71%"))
            s2_lbl = self._wrap(slide.get("stat2_label", "of feed data is now synthetic."), 28)
            s3_val = self._clean_txt(slide.get("stat3_value", "-70%"))
            s3_lbl = self._wrap(slide.get("stat3_label", "Reduction in latency."), 28)
            icon = self._clean_txt(slide.get("insight_icon", "⚡"))
            insight_txt = self._wrap(slide.get("insight_text", "The barrier to entry isn't creation anymore—it is decoupled differentiation."), 60)
            src_txt = self._clean_txt(slide.get("source", ""))

            svg_content = f"""
  <text x="540" y="110" font-family="Inter, sans-serif" font-size="16" font-weight="800" fill="{accent_color}" text-anchor="middle" letter-spacing="3">✦ {eb_txt.upper()} ✦</text>
  <text x="540" y="170" font-family="Inter, sans-serif" font-size="48" font-weight="900" fill="#FFFFFF" text-anchor="middle">{hl_txt}</text>
  
  <!-- Top Bento Box (Main Stat) -->
  <g transform="translate(80, 220)">
    <rect width="920" height="260" rx="26" fill="{card_bg}" stroke="rgba(0,229,204,0.4)" stroke-width="2"/>
    <text x="50" y="130" font-family="Inter, sans-serif" font-size="115" font-weight="900" fill="{primary_color}">{main_stat}</text>
    <text x="360" y="70" font-family="Inter, sans-serif" font-size="22" font-weight="800" fill="{accent_color}" letter-spacing="2">{main_lbl}</text>
    <text x="360" y="125" font-family="Inter, sans-serif" font-size="26" fill="{subtext_color}">{main_dsc.splitlines()[0] if main_dsc.splitlines() else ''}</text>
    <text x="360" y="165" font-family="Inter, sans-serif" font-size="26" fill="{subtext_color}">{main_dsc.splitlines()[1] if len(main_dsc.splitlines())>1 else ''}</text>
  </g>

  <!-- Middle Bento Split Boxes -->
  <g transform="translate(80, 510)">
    <rect width="445" height="180" rx="22" fill="{card_bg}" stroke="#2A2F3D" stroke-width="2"/>
    <text x="40" y="85" font-family="Inter, sans-serif" font-size="64" font-weight="900" fill="#FFFFFF">{s2_val}</text>
    <text x="40" y="135" font-family="Inter, sans-serif" font-size="23" fill="{subtext_color}">{s2_lbl.splitlines()[0] if s2_lbl.splitlines() else ''}</text>
  </g>
  
  <g transform="translate(555, 510)">
    <rect width="445" height="180" rx="22" fill="{card_bg}" stroke="#2A2F3D" stroke-width="2"/>
    <text x="40" y="85" font-family="Inter, sans-serif" font-size="64" font-weight="900" fill="{accent_color}">{s3_val}</text>
    <text x="40" y="135" font-family="Inter, sans-serif" font-size="23" fill="{subtext_color}">{s3_lbl.splitlines()[0] if s3_lbl.splitlines() else ''}</text>
  </g>

  <!-- Bottom Insight Box -->
  <g transform="translate(80, 720)">
    <rect width="920" height="180" rx="26" fill="#181A26" stroke="{primary_color}" stroke-width="2"/>
    <circle cx="70" cy="90" r="32" fill="rgba(0,229,204,0.15)"/>
    <text x="70" y="98" font-family="Inter, sans-serif" font-size="30" text-anchor="middle">{icon}</text>
    <text x="130" y="80" font-family="Inter, sans-serif" font-size="26" font-weight="700" fill="#FFFFFF">{insight_txt.splitlines()[0] if insight_txt.splitlines() else ''}</text>
    <text x="130" y="125" font-family="Inter, sans-serif" font-size="26" fill="{subtext_color}">{insight_txt.splitlines()[1] if len(insight_txt.splitlines())>1 else ''}</text>
  </g>
  
  <text x="990" y="935" font-family="Inter, sans-serif" font-size="18" fill="{subtext_color}" text-anchor="end">Source: {src_txt or 'Industry Benchmark, 2026'}</text>"""

        elif layout == "flowchart":
            # V7 Flowchart / Sequence Layout
            eb_txt = eyebrow or "THE MULTIPLIER"
            hl_txt = headline or "The Human-in-the-Loop Premium"
            nodes = slide.get("nodes", [{"text": "Isolate State"}, {"text": "Async Streams"}, {"text": "Telemetry"}])
            node_strs = [n.get("text", str(n)) if isinstance(n, dict) else str(n) for n in nodes]
            pipe_svg = SVGFlowEngine.generate_pipeline_svg(node_strs, primary_color, accent_color)
            bv = self._clean_txt(slide.get("badge_value", "+372%"))
            bl = self._clean_txt(slide.get("badge_label", "Median ROI Boost"))
            src_txt = self._clean_txt(slide.get("source", ""))

            svg_content = f"""
  <text x="540" y="130" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="{primary_color}" text-anchor="middle" letter-spacing="3">✦ {eb_txt.upper()} ✦</text>
  <text x="540" y="195" font-family="Inter, sans-serif" font-size="52" font-weight="900" fill="#FFFFFF" text-anchor="middle">{hl_txt}</text>
  <g transform="translate(50, 260)">{pipe_svg}</g>
  <g transform="translate(180, 530)">
    <rect width="720" height="260" rx="32" fill="{card_bg}" stroke="{primary_color}" stroke-width="3"/>
    <circle cx="360" cy="130" r="220" fill="url(#cyan-glow)"/>
    <text x="360" y="130" font-family="Inter, sans-serif" font-size="110" font-weight="900" fill="{primary_color}" text-anchor="middle">{bv}</text>
    <text x="360" y="195" font-family="Inter, sans-serif" font-size="32" font-weight="800" fill="#FFFFFF" text-anchor="middle">{bl.upper()}</text>
  </g>
  <text x="990" y="935" font-family="Inter, sans-serif" font-size="18" fill="{subtext_color}" text-anchor="end">Source: {src_txt or 'Engineering Metrics, 2026'}</text>"""

        elif layout == "split" or slide_num == 4:
            # V7 Split Magazine Layout
            eb_txt = eyebrow or "THE PERFORMANCE SCALE"
            hl_txt = headline or "Hyper-Targeting Scale."
            bt = self._wrap(slide.get("body_text", subtitle or "Decoupled systems publish events and immediately release threads without blocking."), 60)
            sv = self._clean_txt(slide.get("stat_value", "+202%"))
            sl = self._clean_txt(slide.get("stat_label", "Higher Throughput"))
            it = self._wrap(slide.get("insight_text", "Strategic decoupling prevents cascading outages under high load."), 58)
            src_txt = self._clean_txt(slide.get("source", ""))

            svg_content = f"""
  <!-- Top Half -->
  <g transform="translate(80, 120)">
    <rect width="920" height="280" rx="26" fill="{card_bg}" stroke="#2A2F3D" stroke-width="2"/>
    <text x="50" y="60" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="{accent_color}" letter-spacing="2">✦ {eb_txt.upper()} ✦</text>
    <text x="50" y="125" font-family="Inter, sans-serif" font-size="46" font-weight="900" fill="#FFFFFF">{hl_txt}</text>
    <text x="50" y="180" font-family="Inter, sans-serif" font-size="24" fill="{subtext_color}">{bt.splitlines()[0] if bt.splitlines() else ''}</text>
    <text x="50" y="220" font-family="Inter, sans-serif" font-size="24" fill="{subtext_color}">{bt.splitlines()[1] if len(bt.splitlines())>1 else ''}</text>
  </g>
  <line x1="80" y1="435" x2="1000" y2="435" stroke="#222530" stroke-width="2"/>
  <!-- Bottom Half -->
  <g transform="translate(80, 470)">
    <rect width="920" height="420" rx="28" fill="{card_bg}" stroke="{primary_color}" stroke-width="2"/>
    <circle cx="220" cy="210" r="180" fill="url(#cyan-glow)"/>
    <text x="50" y="160" font-family="Inter, sans-serif" font-size="125" font-weight="900" fill="{primary_color}">{sv}</text>
    <text x="50" y="225" font-family="Inter, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" letter-spacing="1">{sl.upper()}</text>
    <line x1="50" y1="265" x2="870" y2="265" stroke="#2A2F3D" stroke-width="1.5"/>
    <text x="50" y="325" font-family="Inter, sans-serif" font-size="25" fill="{subtext_color}">{it.splitlines()[0] if it.splitlines() else ''}</text>
    <text x="50" y="365" font-family="Inter, sans-serif" font-size="25" fill="{subtext_color}">{it.splitlines()[1] if len(it.splitlines())>1 else ''}</text>
  </g>
  <text x="990" y="935" font-family="Inter, sans-serif" font-size="18" fill="{subtext_color}" text-anchor="end">Source: {src_txt or 'Systems Benchmark, 2026'}</text>"""

        elif layout == "grid":
            # V7 4-Panel Glass Grid Layout
            eb_txt = eyebrow or "CORE PILLARS"
            hl_txt = headline or "The 4 Architecture Commandments"
            src_txt = self._clean_txt(slide.get("source", ""))
            
            grid_svg = ""
            coords = [(80, 220), (555, 220), (80, 540), (555, 540)]
            for p_idx in [1, 2, 3, 4]:
                pt = self._clean_txt(slide.get(f"panel{p_idx}_title", f"Pillar {p_idx}"))
                pb = self._wrap(slide.get(f"panel{p_idx}_text", "Execute idempotent boundaries to eliminate duplicate records."), 33)
                gx, gy = coords[p_idx-1]
                bc = primary_color if p_idx in [1, 4] else accent_color
                grid_svg += f"""
  <g transform="translate({gx}, {gy})">
    <rect width="445" height="290" rx="24" fill="{card_bg}" stroke="{bc}" stroke-width="2"/>
    <circle cx="60" cy="60" r="22" fill="rgba(255,255,255,0.05)"/>
    <text x="60" y="66" font-family="Inter, sans-serif" font-size="20" font-weight="800" fill="{bc}" text-anchor="middle">0{p_idx}</text>
    <text x="35" y="130" font-family="Inter, sans-serif" font-size="26" font-weight="800" fill="#FFFFFF">{pt[:26]}</text>
    <text x="35" y="180" font-family="Inter, sans-serif" font-size="22" fill="{subtext_color}">{pb.splitlines()[0] if pb.splitlines() else ''}</text>
    <text x="35" y="220" font-family="Inter, sans-serif" font-size="22" fill="{subtext_color}">{pb.splitlines()[1] if len(pb.splitlines())>1 else ''}</text>
    <text x="35" y="260" font-family="Inter, sans-serif" font-size="22" fill="{subtext_color}">{pb.splitlines()[2] if len(pb.splitlines())>2 else ''}</text>
  </g>"""

            svg_content = f"""
  <text x="540" y="110" font-family="Inter, sans-serif" font-size="16" font-weight="800" fill="{primary_color}" text-anchor="middle" letter-spacing="3">✦ {eb_txt.upper()} ✦</text>
  <text x="540" y="175" font-family="Inter, sans-serif" font-size="48" font-weight="900" fill="#FFFFFF" text-anchor="middle">{hl_txt}</text>
  {grid_svg}
  <text x="990" y="935" font-family="Inter, sans-serif" font-size="18" fill="{subtext_color}" text-anchor="end">Source: {src_txt or 'Engineering Architecture, 2026'}</text>"""

        elif layout in ["outro", "cta_classic"] or slide_num == total_slides:
            # Outro / Checklist & Pin card
            cta_text = self._clean_txt(slide.get("cta_text", "SAVE THIS CHEAT SHEET."))
            cta_highlight = self._clean_txt(slide.get("cta_highlight", slide.get("subtitle", "You'll need these insights for your next backend interview.")))
            items = slide.get("items", [{"text": "Start with REST APIs for standard web apps."}, {"text": "Move to GraphQL when optimizing payload sizes."}, {"text": "Use WebSockets only when real-time is mandatory."}])
            
            items_svg = ""
            for idx_i, item in enumerate(items[:3], 1):
                txt = self._wrap(item.get("text", str(item)) if isinstance(item, dict) else str(item), 48)
                lines = txt.splitlines()
                l0 = lines[0] if lines else ""
                l1 = lines[1] if len(lines) > 1 else ""
                items_svg += f"""
    <text x="0" y="{idx_i*130 - 90}" font-family="Inter, sans-serif" font-size="34" font-weight="800" fill="{primary_color}">0{idx_i}.</text>
    <text x="70" y="{idx_i*130 - 90}" font-family="Inter, sans-serif" font-size="30" font-weight="700" fill="#FFFFFF">{l0}</text>
    <text x="70" y="{idx_i*130 - 50}" font-family="Inter, sans-serif" font-size="30" font-weight="700" fill="#FFFFFF">{l1}</text>
    <line x1="0" y1="{idx_i*130 - 15}" x2="800" y2="{idx_i*130 - 15}" stroke="#1E222D" stroke-width="2"/>"""

            svg_content = f"""
  <text x="540" y="140" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="{primary_color}" text-anchor="middle" letter-spacing="3">— KEEP EXPLORING</text>
  <text x="540" y="210" font-family="Inter, sans-serif" font-size="64" font-weight="900" fill="#FFFFFF" text-anchor="middle">The possibilities are</text>
  <text x="540" y="285" font-family="Inter, sans-serif" font-size="64" font-weight="900" fill="{primary_color}" text-anchor="middle">endless.</text>
  <g transform="translate(140, 380)">{items_svg}</g>
  <g transform="translate(100, 860)">
    <rect width="880" height="230" rx="30" fill="#14161C" stroke="{accent_color}" stroke-width="2"/>
    <circle cx="440" cy="115" r="280" fill="url(#orange-glow)"/>
    <text x="440" y="85" font-family="Inter, sans-serif" font-size="38" text-anchor="middle">📌</text>
    <text x="440" y="140" font-family="Inter, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF" text-anchor="middle">{cta_text}</text>
    <text x="440" y="185" font-family="Inter, sans-serif" font-size="26" font-weight="800" fill="{accent_color}" text-anchor="middle">{cta_highlight[:60]}</text>
  </g>"""
        else:
            # Fallback for deep dive boxes
            svg_content = f"""
  <text x="540" y="120" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="{primary_color}" text-anchor="middle" letter-spacing="3">✦ {self._clean_txt(slide.get('eyebrow', 'OVERVIEW')).upper()} ✦</text>
  <text x="540" y="185" font-family="Inter, sans-serif" font-size="52" font-weight="900" fill="#FFFFFF" text-anchor="middle">{self._clean_txt(headline)}</text>
  <g transform="translate(90, 260)">
    <rect width="900" height="660" rx="28" fill="{card_bg}" stroke="rgba(0,229,204,0.3)" stroke-width="2"/>
    <text x="450" y="330" font-family="Inter, sans-serif" font-size="32" fill="{subtext_color}" text-anchor="middle">{self._wrap(subtitle, 54)}</text>
  </g>"""

        svg_footer = f"""
  <text x="540" y="1285" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" opacity="0.6" text-anchor="middle" letter-spacing="4">AIWITHSUFIYAN   {slide_num:02d} / {total_slides:02d}</text>
</svg>"""

        full_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
{svg_defs}
{svg_content}
{svg_footer}"""

        temp_svg = output_png.with_suffix(".temp.svg")
        temp_svg.write_text(full_svg, encoding="utf-8")

        try:
            subprocess.run(["node", str(self.bridge_path), str(temp_svg), str(output_png)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            pass
        finally:
            if temp_svg.exists():
                temp_svg.unlink()
