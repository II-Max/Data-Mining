from urllib.parse import urlparse

from rich import print

from core.scraper import fetch_page
from core.table_miner import mine_tables
from core.exporter import export_site_tables
from core.email_miner import (
    mine_emails,
    export_emails
)

from core.config import TARGET_FILE


def sanitize_site_name(url):

    parsed = urlparse(url)

    domain = parsed.netloc

    safe_name = (
        domain
        .replace("www.", "")
        .replace(".", "_")
        .replace(":", "_")
    )

    return safe_name


def process_single_site(url):

    print(
        f"\n[cyan]Scanning:[/cyan] {url}"
    )

    html = fetch_page(url)

    if not html:

        print(
            f"[red]Failed:[/red] {url}"
        )

        return

    site_name = sanitize_site_name(url)

    ranked_tables = mine_tables(html)

    emails = mine_emails(html)

    export_site_tables(
        ranked_tables,
        site_name
    )

    export_emails(
        emails,
        site_name
    )

    print(
        f"[green]Completed:[/green] "
        f"{site_name}"
    )

    print(
        f"  Tables: {len(ranked_tables)}"
    )

    print(
        f"  Emails: {len(emails)}"
    )


def process_multiple_sites(
    file_path=TARGET_FILE
):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        urls = [
            line.strip()
            for line in f
            if line.strip()
        ]

    print(
        f"\n[bold yellow]"
        f"Loaded {len(urls)} target websites"
        f"[/bold yellow]"
    )

    for url in urls:

        process_single_site(url)