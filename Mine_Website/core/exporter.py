import pandas as pd

from core.config import OUTPUT_DIR
from core.logger import logger


def export_site_tables(ranked_tables, site_name):

    if not ranked_tables:

        logger.warning(
            f"No tables found for {site_name}"
        )

        return

    # ===== EXCEL EXPORT =====

    excel_file = (
        OUTPUT_DIR /
        f"{site_name}.xlsx"
    )

    with pd.ExcelWriter(
        excel_file,
        engine="openpyxl"
    ) as writer:

        for table in ranked_tables:

            df = table["dataframe"]

            df.to_excel(
                writer,
                sheet_name=f"Table_{table['index']}",
                index=False
            )

    # ===== COMBINED CSV EXPORT =====

    combined_file = (
        OUTPUT_DIR /
        f"{site_name}_combined.csv"
    )

    with open(
        combined_file,
        "w",
        encoding="utf-8-sig"
    ) as f:

        for table in ranked_tables:

            df = table["dataframe"]

            separator = (
                f"\n--- CUT TABLE "
                f"{table['index']} ---\n"
            )

            f.write(separator)

            df.to_csv(
                f,
                index=False
            )

            f.write("\n")

    logger.info(
        f"Export completed for {site_name}"
    )