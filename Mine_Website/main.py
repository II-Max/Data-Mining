from rich.console import Console
from rich.table import Table
from rich import print

from core.scraper import fetch_page
from core.table_miner import mine_tables
from core.email_miner import (
    mine_emails,
    export_emails
)
from core.exporter import (
    export_tables_csv,
    export_tables_excel
)

console = Console()

def display_table_summary(ranked_tables):

    summary = Table(
        title="Detected Tables"
    )

    summary.add_column(
        "Rank",
        style="cyan"
    )

    summary.add_column(
        "Rows",
        style="green"
    )

    summary.add_column(
        "Columns",
        style="yellow"
    )

    summary.add_column(
        "Score",
        style="magenta"
    )

    for idx, item in enumerate(
        ranked_tables,
        1
    ):

        df = item["dataframe"]

        rows, cols = df.shape

        summary.add_row(
            str(idx),
            str(rows),
            str(cols),
            str(item["score"])
        )

    console.print(summary)

def show_emails(emails):

    if not emails:

        print(
            "[red]No emails found[/red]"
        )

        return

    print(
        "\n[bold green]Emails Found:[/bold green]"
    )

    for idx, email in enumerate(
        emails,
        1
    ):

        print(
            f"[cyan]{idx}.[/cyan] {email}"
        )

def main():

    print(
        "[bold cyan]"
        "===> DataMine Framework V3 <==="
        "[/bold cyan]"
    )

    url = input(
        "\nEnter target URL: "
    ).strip()

    try:

        html = fetch_page(url)

        while True:

            print(
                "\n[bold yellow]"
                "MENU"
                "[/bold yellow]"
            )

            print(
                "1. Mine all tables"
            )

            print(
                "2. Mine emails"
            )

            print(
                "3. Full scan"
            )

            print(
                "4. Exit"
            )

            choice = input(
                "\nSelect option: "
            ).strip()

            if choice == '1':

                ranked_tables = (
                    mine_tables(html)
                )

                if ranked_tables:

                    display_table_summary(
                        ranked_tables
                    )

                    export_tables_csv(
                        ranked_tables
                    )

                    export_tables_excel(
                        ranked_tables
                    )

                    print(
                        "[green]"
                        "Tables exported successfully"
                        "[/green]"
                    )

                else:

                    print(
                        "[red]"
                        "No tables found"
                        "[/red]"
                    )

            elif choice == '2':

                emails = mine_emails(
                    html
                )

                show_emails(emails)

                export_emails(emails)

                print(
                    "[green]"
                    "Emails exported successfully"
                    "[/green]"
                )

            elif choice == '3':

                ranked_tables = (
                    mine_tables(html)
                )

                emails = mine_emails(
                    html
                )

                if ranked_tables:

                    display_table_summary(
                        ranked_tables
                    )

                    export_tables_csv(
                        ranked_tables
                    )

                    export_tables_excel(
                        ranked_tables
                    )

                show_emails(emails)

                export_emails(emails)

                print(
                    "[bold green]"
                    "Full scan completed"
                    "[/bold green]"
                )

            elif choice == '4':

                print(
                    "[bold red]"
                    "Exiting DataMine..."
                    "[/bold red]"
                )

                break

            else:

                print(
                    "[red]"
                    "Invalid option"
                    "[/red]"
                )

    except Exception as e:

        print(
            f"[bold red]ERROR:[/bold red] {e}"
        )

if __name__ == "__main__":
    main()