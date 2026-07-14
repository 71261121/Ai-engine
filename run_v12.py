"""
run_v12.py  —  V12 Masterpiece Engine Runner

THE CORRECT RUNNER. Previous scripts (run_batch.py, run_5_posts.py, run_v10_prod.py)
all used V10Orchestrator. This runs the ACTUAL best version: V12.

V12 adds over V10:
  ✦ TopicDNA  —  unique visual language per topic
  ✦ Narrative Arc selection  (8 arc types, not generic)
  ✦ 5 Specialized Critics  (Narrative, Concept, Data, Voice, Novelty)
  ✦ Art Director revision loop until MASTERPIECE (score ≥7.5)
  ✦ Voice Engine  —  detects and fixes buzzwords
  ✦ Novelty Tracker  —  prevents visual repetition across runs
  ✦ NarrativeWriter V11  —  per-layout schemas (RC7 fix: no more empty slides)

RC fixes applied in this session:
  RC1  concept_enrichment.py  →  glow layers stripped (_strip_glow_elements)
  RC2  v7_shared.css          →  --accent-primary / --accent-secondary defined
  RC4  THIS FILE              →  V12 now has a runner
  RC5  orchestrator_v12.py    →  model_tier="smart" → "strong"
  RC6  concept_enrichment.py  →  enrichment LLM call removed (fallback only)
  RC7  orchestrator_v12.py    →  NarrativeWriterV11 (per-layout schemas)

Usage:
  python run_v12.py                           # 5 default topics
  python run_v12.py --count 1                 # 1 topic
  python run_v12.py --topic "Docker vs K8s"  # specific topic
  python run_v12.py --list topics.txt         # topics from file
  python run_v12.py --dry-run                 # show queue only
"""

import sys
import time
import random
import argparse
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src.graph.orchestrator_v12 import V12Orchestrator

DEFAULT_TOPICS = [
    "Rust vs Go: Which Should You Learn in 2025",
    "How Kafka Works Under the Hood",
    "The 5 SQL Commands Most Developers Misuse",
    "Docker Networking Explained Simply",
    "Why Your API Design is Slowing Down Your Team",
]


def parse_args():
    p = argparse.ArgumentParser(description="V12 Masterpiece Carousel Engine")
    p.add_argument("--topic",    type=str,   default=None,  help="Single specific topic")
    p.add_argument("--count",    type=int,   default=5,     help="Number of topics (default: 5)")
    p.add_argument("--list",     type=str,   default=None,  help="Path to topics.txt (one per line)")
    p.add_argument("--sleep",    type=float, default=8,     help="Seconds between runs (default: 8)")
    p.add_argument("--iters",    type=int,   default=2,     help="Max revision iterations (default: 2)")
    p.add_argument("--dry-run",  action="store_true",       help="Print topic queue without running")
    return p.parse_args()


def main():
    args = parse_args()

    # ── Build topic list ──────────────────────────────────────
    if args.topic:
        topics = [args.topic]
    elif args.list:
        path = Path(args.list)
        if not path.exists():
            print(f"ERROR: topic file not found: {path}"); sys.exit(1)
        topics = [ln.strip() for ln in path.read_text().splitlines() if ln.strip()]
    else:
        topics = DEFAULT_TOPICS[:args.count]

    print(f"\n{'='*65}")
    print(f"  V12 MASTERPIECE ENGINE  —  {len(topics)} carousel(s)")
    print(f"{'='*65}")

    if args.dry_run:
        for i, t in enumerate(topics, 1):
            print(f"  [{i}] {t}")
        print("\nDry run — nothing processed.")
        return

    orchestrator = V12Orchestrator(max_iterations=args.iters)
    success, fail = 0, 0

    for i, topic in enumerate(topics, 1):
        print(f"\n{'─'*65}")
        print(f"  [{i}/{len(topics)}]  {topic}")
        print(f"{'─'*65}")
        try:
            result = orchestrator.run(topic=topic)
            success += 1
            rr = result.get("revision_report", {})
            pkg = result.get("publish_package", {})
            print(f"\n  ✅  Done  →  {result['output_dir']}")
            print(f"     Score   : {rr.get('final_score', '?'):.2f}/10")
            print(f"     Verdict : {rr.get('verdict', '?')}")
            print(f"     Time    : {pkg.get('total_time_s', '?')}s")
        except Exception as exc:
            fail += 1
            print(f"\n  ❌  FAILED: {exc}")
            traceback.print_exc()

        if i < len(topics):
            sleep = max(3, args.sleep + random.uniform(-2, 2))
            print(f"\n  ⏳  Waiting {sleep:.1f}s...", flush=True)
            time.sleep(sleep)

    print(f"\n{'='*65}")
    print(f"  COMPLETE  —  ✅ {success} success  /  ❌ {fail} failed")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()
