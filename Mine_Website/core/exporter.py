import pandas as pd

from core.config import OUTPUT_DIR
from core.logger import logger

def export_tables_csv(ranked_tables):

    if not ranked_tables:

        logger.warning(
            "No tables to export"
        )

        return

    for table in ranked_tables:

        filename = (
            OUTPUT_DIR /
            f"table_{table['index']}.csv"
        )

        table["dataframe"].to_csv(
            filename,
            index=False,
            encoding="utf-8-sig"
        )

    logger.info(
        "CSV export completed"
    )

def export_tables_excel(ranked_tables):

    if not ranked_tables:

        logger.warning(
            "No tables to export"
        )

        return

    output_file = (
        OUTPUT_DIR /
        "all_tables.xlsx"
    )

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        for table in ranked_tables:

            sheet_name = (
                f"Table_{table['index']}"
            )

            table["dataframe"].to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

    logger.info(
        "Excel export completed"
    )