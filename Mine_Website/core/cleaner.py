from bs4 import BeautifulSoup


def extract_clean_text(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for tag in soup([
        "script",
        "style",
        "noscript"
    ]):
        tag.decompose()

    return soup.get_text(separator=" ")