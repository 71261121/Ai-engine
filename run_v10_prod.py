#!/usr/bin/env python3
"""Root Entrypoint Wrapper for V10 Production Engine."""
import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from scripts.run_v10_prod import main

if __name__ == "__main__":
    main()
