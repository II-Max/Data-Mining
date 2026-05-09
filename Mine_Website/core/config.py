from pathlib import Path

# ===== ROOT DIRECTORY =====

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== OUTPUT DIRECTORY =====

OUTPUT_DIR = BASE_DIR / "outputs"

# ===== LOG DIRECTORY =====

LOG_DIR = BASE_DIR / "logs"

# ===== TARGET FILE =====

TARGET_FILE = BASE_DIR / "targets.txt"

# ===== AUTO CREATE FOLDERS =====

OUTPUT_DIR.mkdir(exist_ok=True)

LOG_DIR.mkdir(exist_ok=True)

# ===== AUTO CREATE TARGET FILE =====

if not TARGET_FILE.exists():

    TARGET_FILE.write_text(
        "https://example.com\n",
        encoding="utf-8"
    )