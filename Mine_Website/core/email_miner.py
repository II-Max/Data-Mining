import re
import pandas as pd

from core.cleaner import extract_clean_text
from core.logger import logger
from core.config import OUTPUT_DIR

EMAIL_REGEX = (
    r'\b[A-Za-z0-9._%+-]+'
    r'@[A-Za-z0-9.-]+'
    r'\.[A-Za-z]{2,}\b'
)

def mine_emails(html):

    logger.info("Starting email mining")

    clean_text = extract_clean_text(html)

    emails = sorted(
        set(
            re.findall(
                EMAIL_REGEX,
                clean_text
            )
        )
    )

    logger.info(
        f"Found {len(emails)} emails"
    )

    return emails

def export_emails(emails):

    if not emails:
        logger.warning(
            "No emails to export"
        )
        return

    output_file = OUTPUT_DIR / "emails.csv"

    df = pd.DataFrame(
        emails,
        columns=["Email"]
    )

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info(
        "Emails exported successfully"
    )