import io
import pandas as pd

from core.logger import logger

def score_table(df):

    rows, cols = df.shape

    score = rows * cols

    missing_ratio = (
        df.isnull()
        .mean()
        .mean()
    )

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
            io.StringIO(html),
            header=0,
            thousands=',',
            decimal='.',
            na_values=[
                '-',
                'N/A',
                ''
            ]
        )

    except ValueError:

        logger.warning(
            "No tables found"
        )

        return []

    ranked_tables = []

    for idx, df in enumerate(tables):

        score = score_table(df)

        ranked_tables.append({
            "index": idx + 1,
            "score": score,
            "dataframe": df
        })

    ranked_tables.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    logger.info(
        f"Found {len(ranked_tables)} tables"
    )

    return ranked_tables