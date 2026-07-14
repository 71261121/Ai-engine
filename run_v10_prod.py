import os
import sys
from pathlib import Path

# Ensure utf-8 output for Windows console
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src.graph.orchestrator_v10 import V10Orchestrator

def main():
    print("Starting V10 Orchestrator Full Production Run...")
    orch = V10Orchestrator()
    results = orch.run_continuous(count=1, topics=['Why AI Agents Are Replacing Standard SaaS'])
    
    for r in results:
        if 'error' in r:
            print(f"Failed: {r['error']}")
        else:
            print(f"Success! Output saved to: {r.get('output_dir')}")

if __name__ == '__main__':
    main()
