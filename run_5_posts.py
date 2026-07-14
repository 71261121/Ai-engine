#!/usr/bin/env python3
"""Root Entrypoint Wrapper for 5 Posts Runner."""
import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Run the script module directly
import scripts.run_5_posts
