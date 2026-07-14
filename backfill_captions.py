import os
import re
import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src.agents.caption_agent import CaptionAgent

agent = CaptionAgent()

runs = [
    "run_20260703_140942",
    "run_20260703_141529",
    "run_20260703_142114",
    "run_20260703_142621",
    "run_20260703_143214"
]

output_dir = Path("output")

for run_id in runs:
    run_dir = output_dir / run_id
    pkg_file = run_dir / "publish_package.json"
    
    if not pkg_file.exists():
        continue
        
    with open(pkg_file, "r", encoding="utf-8") as f:
        pkg = json.load(f)
        
    if pkg.get("caption"):
        print(f"Skipping {run_id} - already has caption")
        continue
        
    print(f"\nProcessing {run_id} - {pkg['topic']}")
    
    html_dir = run_dir / "html"
    slides = []
    
    # Read HTML files and extract text
    if html_dir.exists():
        html_files = sorted(html_dir.glob("slide_*.html"))
        for hf in html_files:
            with open(hf, "r", encoding="utf-8") as f:
                content = f.read()
            # Strip html tags
            text = re.sub(r'<[^>]+>', ' ', content)
            # Remove extra spaces
            text = re.sub(r'\s+', ' ', text).strip()
            # The LLM just needs the text bits
            slides.append({"text": text})
            
    # The agent expects a list of dicts. We packed the text into {"text": text}
    # It will extract it because it looks for isinstance(v, str).
    caption_data = agent.generate_caption(pkg["topic"], slides, pkg["narrative_arc"])
    
    pkg["caption"] = caption_data["caption"]
    pkg["hashtags"] = caption_data["hashtags"]
    
    with open(pkg_file, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully added caption to {run_id}")
    time.sleep(2) # rate limit

