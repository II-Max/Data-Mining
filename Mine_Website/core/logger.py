import logging

from core.config import LOG_DIR

log_file = LOG_DIR / "datamine.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("DataMine")