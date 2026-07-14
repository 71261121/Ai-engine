"""
Utility script to backfill captions for existing carousel run outputs.
Dynamically scans outputs/runs/ for any run missing caption data and generates it via CaptionAgent.
"""
import os
import re
import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.agents.caption_agent import CaptionAgent

agent = CaptionAgent()

_root = Path(__file__).resolve().parent.parent
runs_dir = _root / "outputs" / "runs"

if not runs_dir.exists():
    print(f"No runs directory found at {runs_dir}")
    sys.exit(0)

print(f"Scanning {runs_dir} for runs missing captions...\n")

for run_dir in sorted(runs_dir.iterdir()):
    if not run_dir.is_dir():
        continue

    pkg_file = run_dir / "publish_package.json"
    if not pkg_file.exists():
        pkg_file = run_dir / "report.json"
        if not pkg_file.exists():
            continue

    with open(pkg_file, "r", encoding="utf-8") as f:
        try:
            pkg = json.load(f)
        except Exception:
            continue

    if pkg.get("caption"):
        print(f"✔ Skipping {run_dir.name} — already has caption ({len(pkg['caption'])} chars)")
        continue

    print(f"\n⚡ Processing {run_dir.name} — Topic: '{pkg.get('topic', 'Unknown')}'")

    # Find slide HTML files
    slides = []
    html_files = sorted(run_dir.glob("slide_*.html"))
    if not html_files and (run_dir / "html").exists():
        html_files = sorted((run_dir / "html").glob("slide_*.html"))

    if html_files:
        for hf in html_files:
            with open(hf, "r", encoding="utf-8") as f:
                content = f.read()
            text = re.sub(r'<[^>]+>', ' ', content)
            text = re.sub(r'\s+', ' ', text).strip()
            slides.append({"text": text})
    else:
        # Check if slides are in json
        slides = pkg.get("slides", [{"text": pkg.get("topic", "")}])

    topic = pkg.get("topic", "General Technical Topic")
    arc = pkg.get("arc_id", pkg.get("narrative_arc", "explainer"))

    caption_data = agent.generate_caption(topic, slides, arc)

    pkg["caption"] = caption_data.get("caption", "")
    pkg["hashtags"] = caption_data.get("hashtags", [])

    with open(pkg_file, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully backfilled caption for {run_dir.name}")
    time.sleep(1)

print("\n🎉 Backfill complete!")
