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

def fetch_page(url):

    try:
        logger.info(f"Connecting to: {url}")

        session = requests.Session()

        session.headers.update(HEADERS)

        response = session.get(
            url,
            timeout=15
        )

        response.raise_for_status()

        logger.info("Connection successful")

        return response.text

    except requests.exceptions.RequestException as e:

        logger.error(f"Connection error: {e}")

        raise