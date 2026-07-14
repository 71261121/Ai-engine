import sys
import os
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.graph.orchestrator_v10 import V10Orchestrator

# Topics requested
topics = [
    "5 Ways AI is Changing Software Development",
    "Why Microservices are a Double-Edged Sword",
    "The Future of Data Engineering",
    "How to Write Cleaner Python Code",
    "Understanding Kubernetes Architecture"
]

orchestrator = V10Orchestrator()
for i, topic in enumerate(topics, 1):
    print(f"\n{'='*50}", flush=True)
    print(f"Generating Carousel {i}/5: {topic}", flush=True)
    print(f"{'='*50}\n", flush=True)
    try:
        res = orchestrator.run(topic=topic)
        print(f"Successfully generated carousel for: {topic}", flush=True)
        print(f"Output saved to: {res['output_dir']}", flush=True)
    except Exception as e:
        print(f"Error generating carousel for {topic}: {e}", flush=True)
        import traceback
        traceback.print_exc()
    
    print("\nWaiting 5 seconds before next...", flush=True)
    time.sleep(5)
