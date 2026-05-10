import requests

from core.logger import logger

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}

session = requests.Session()

session.headers.update(HEADERS)


def fetch_page(url):

    try:

        logger.info(
            f"Connecting to: {url}"
        )

        response = session.get(
            url,
            timeout=30,
            verify=False,
            allow_redirects=True
        )

        response.raise_for_status()

        # ===== FIX ENCODING =====

        response.encoding = response.apparent_encoding

        logger.info(
            f"Success: {url}"
        )

        return response.text

    except requests.exceptions.RequestException as e:

        logger.error(
            f"Connection error for {url}: {e}"
        )

        return None