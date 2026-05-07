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

    clean_text = soup.get_text(
        separator=" "
    )

    return clean_text