"""Launcher script for SignBridge Live Application.

Usage:
    python scripts/run_app.py          # Run live with webcam (or auto-fallback to mock)
    python scripts/run_app.py --mock   # Force synthetic mock camera
    python scripts/run_app.py --help   # Show options
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.ui.app import run_app

if __name__ == "__main__":
    run_app()
