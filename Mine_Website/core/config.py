from pathlib import Path

# Root project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Output directory
OUTPUT_DIR = BASE_DIR / "outputs"

# Log directory
LOG_DIR = BASE_DIR / "logs"

# Create folders automatically
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)