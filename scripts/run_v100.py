"""
Execution Runner for V100 Masterpiece Cyclic State-Graph Engine.
"""
import sys
import time
import argparse
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.graph.orchestrator_v100 import V100Orchestrator

DEFAULT_TOPICS = [
    "Why AI Agents Are Replacing Standard SaaS in 2026",
    "How to Design Idempotent Microservice Boundaries",
    "The 5 SQL Anti-Patterns Killing Your Database Performance",
    "Understanding Kubernetes Architecture Like a Senior Dev"
]


def parse_args():
    p = argparse.ArgumentParser(description="V100 Masterpiece Carousel Engine")
    p.add_argument("--topic",    type=str,   default=None,  help="Single specific topic")
    p.add_argument("--count",    type=int,   default=1,     help="Number of topics (default: 1)")
    p.add_argument("--iters",    type=int,   default=2,     help="Max revision iterations (default: 2)")
    p.add_argument("--dry-run",  action="store_true",       help="Print topic queue without running")
    return p.parse_args()


def main():
    args = parse_args()
    topics = [args.topic] if args.topic else DEFAULT_TOPICS[:args.count]

    print(f"\n{'='*65}")
    print(f"  🔥 V100 GOD-TIER MASTERPIECE ENGINE  —  {len(topics)} carousel(s)")
    print(f"{'='*65}")

    if args.dry_run:
        for i, t in enumerate(topics, 1):
            print(f"  [{i}] {t}")
        print("\nDry run — nothing processed.")
        return

    orchestrator = V100Orchestrator(max_iterations=args.iters)
    success, fail = 0, 0

    for i, topic in enumerate(topics, 1):
        print(f"\n{'─'*65}")
        print(f"  [{i}/{len(topics)}]  {topic}")
        print(f"{'─'*65}")
        try:
            result = orchestrator.run(topic=topic)
            success += 1
            print(f"\n  ✅  Done  →  {result.get('run_id')}")
            print(f"     Critic Score : {result.get('critic_score', '?')}/10")
            print(f"     Vision Score : {result.get('vision_score', '?')}/100")
            print(f"     Verdict      : {result.get('verdict', '?')}")
            print(f"     Time         : {result.get('total_time_s', '?')}s")
        except Exception as exc:
            fail += 1
            print(f"\n  ❌  FAILED: {exc}")
            traceback.print_exc()

    print(f"\n{'='*65}")
    print(f"  COMPLETE  —  ✅ {success} success  /  ❌ {fail} failed")
    print(f"{'='*65}\n")


if __name__ == "__main__":
    main()
