"""
Omni-Channel Multi-Format Packager for 100x Engine.
Compiles generated PNG slides into LinkedIn Native PDF Carousels,
Twitter/X single-image summaries, and long-form Markdown articles (`article.md`).
"""
import subprocess
from pathlib import Path
from typing import List, Dict, Any


class OmniPackager:
    """
    Synthesizes multi-format marketing assets from a single V100 run.
    """

    @staticmethod
    def package_assets(png_paths: List[Path], slides: List[Dict[str, Any]], topic: str, output_dir: Path) -> Dict[str, str]:
        print(f"  📦 [Omni-Packager] Compiling multi-format marketing suites (`.pdf`, `.md`) for Omni-Channel distribution...")
        assets = {}

        # 1. Compile LinkedIn Native PDF Carousel
        pdf_path = output_dir / f"{topic.lower().replace(' ', '_')[:35]}_carousel.pdf"
        valid_pngs = [str(p) for p in png_paths if p.exists()]
        if valid_pngs:
            try:
                subprocess.run(["convert"] + valid_pngs + [str(pdf_path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                assets["linkedin_pdf"] = pdf_path.name
                print(f"     ✔ LinkedIn Native PDF Carousel compiled ({round(pdf_path.stat().st_size/1024, 1)} KB)")
            except Exception as e:
                pass

        # 2. Write Long-Form Authoritative Markdown Article (`article.md`)
        article_path = output_dir / "article.md"
        lines = [
            f"# {topic}: Deep Architectural Breakdown & Production Blueprint",
            f"\n*An authoritative systems engineering guide by **@AIWITHSUFIYAN***\n",
            "## Executive Summary",
            "Modern software architectures face increasing operational friction when handling complex state boundaries and distributed workloads. This guide breaks down the exact mechanics, performance trade-offs, and step-by-step implementation blueprint to overcome these production bottlenecks.\n"
        ]
        for idx, s in enumerate(slides, 1):
            hl = s.get("headline", f"Section {idx}")
            sub = s.get("subtitle", "")
            lines.append(f"### {idx}. {hl}")
            if sub:
                lines.append(f"\n{sub}\n")
            for b_idx in [1, 2, 3]:
                t = s.get(f"box{b_idx}_title", "")
                b = s.get(f"box{b_idx}_body", "")
                if t or b:
                    lines.append(f"- **{t}**: {b}")
            if s.get("main_stat"):
                lines.append(f"\n> **Key Benchmark**: {s.get('main_stat')} — *{s.get('stat_label', '')}*\n")
            if s.get("left_col") and s.get("right_col"):
                lines.append(f"\n| Amateur / Legacy Approach | Pro / Modern Approach |\n| :--- | :--- |\n| {s.get('left_col')} | {s.get('right_col')} |\n")

        lines.append("\n---\n*Enjoyed this deep dive? Follow **@AIWITHSUFIYAN** for daily technical blueprints and systems architecture guides.*")
        article_path.write_text("\n".join(lines), encoding="utf-8")
        assets["article_md"] = article_path.name
        print(f"     ✔ Long-Form Technical Article written (`article.md`)")

        return assets
