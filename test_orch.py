import sys
from pathlib import Path

# Add project root to path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(r"C:\Users\mdsal\OneDrive\Desktop\AI_Carousel_Engine_V2_EXPERIMENTAL")))
sys.path.insert(0, str(Path(r"C:\Users\mdsal\OneDrive\Desktop\AI_Carousel_Engine_V2_EXPERIMENTAL\01_The_Engine")))

from src.graph.orchestrator_v10 import V10Orchestrator

if __name__ == "__main__":
    print("Initializing orchestrator...", flush=True)
    orch = V10Orchestrator()
    print("Orchestrator initialized. Running...", flush=True)
    try:
        res = orch.run(topic="Testing AI Workflows", run_id="run_20260706_test")
        print("Run complete!", flush=True)
    except Exception as e:
        print(f"Error during run: {e}", flush=True)
        import traceback
        traceback.print_exc()
