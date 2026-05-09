from rich import print

from core.batch_processor import (
    process_multiple_sites
)


def main():

    print(
        "[bold cyan]"
        "===> DataMine Multi-Site Crawler V4 <==="
        "[/bold cyan]"
    )

    print(
        "\n[green]"
        "Automatically scans multiple websites"
        "[/green]"
    )

    print(
        "[green]"
        "Exports CSV + Excel for each website"
        "[/green]"
    )

    try:

        process_multiple_sites(
            "targets.txt"
        )

        print(
            "\n[bold green]"
            "All websites processed successfully"
            "[/bold green]"
        )

    except Exception as e:

        print(
            f"[bold red]ERROR:[/bold red] {e}"
        )


if __name__ == "__main__":
    main()