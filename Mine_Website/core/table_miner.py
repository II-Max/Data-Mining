import io

import pandas as pd

from core.logger import logger


MIN_ROWS = 3
MIN_COLS = 2


def is_valid_table(df):

    rows, cols = df.shape

    # ===== TOO SMALL =====

    if rows < MIN_ROWS:
        return False

    if cols < MIN_COLS:
        return False

    # ===== MOSTLY EMPTY =====

    missing_ratio = (
        df.isnull()
        .mean()
        .mean()
    )

    if pd.isna(missing_ratio):
        return False

    if missing_ratio > 0.8:
        return False

    # ===== HEADER QUALITY =====

    bad_headers = 0

    for col in df.columns:

        if "unnamed" in str(col).lower():
            bad_headers += 1

    if bad_headers >= len(df.columns):
        return False

    return True


def score_table(df):

    rows, cols = df.shape

    score = rows * cols

    missing_ratio = (
        df.isnull()
        .mean()
        .mean()
    )

    if pd.isna(missing_ratio):
        missing_ratio = 1

    score -= int(
        missing_ratio * 100
    )

    return score


def mine_tables(html):

    logger.info(
        "Starting table mining"
    )

    try:

        tables = pd.read_html(
            io.StringIO(html)
        )

    except ValueError:

        logger.warning(
            "No tables found"
        )

        return []

    ranked_tables = []

    for idx, df in enumerate(tables):

        try:

            # ===== FILTER BAD TABLE =====

            if not is_valid_table(df):
                continue

            score = score_table(df)

            ranked_tables.append({
                "index": idx + 1,
                "score": score,
                "dataframe": df
            })

        except Exception as e:

            logger.error(
                f"Table processing error: {e}"
            )

    ranked_tables.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    logger.info(
        f"Valid tables found: "
        f"{len(ranked_tables)}"
    )

    return ranked_tables