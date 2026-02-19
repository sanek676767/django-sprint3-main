import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
PROJECT_DIR = REPO_ROOT / "blogicum"

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogicum.settings")
