import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def check_url(url):
    start = time.monotonic()
    code = None

    try:
        with urlopen(url, timeout=3) as response:
            code = response.status
    except HTTPError as error:
        code = error.code
        error.close()
    except (URLError, OSError):
        pass

    status = "down"
    if code is not None and 200 <= code < 300:
        status = "up"

    return {
        "status": status,
        "http_status": code,
        "response_ms": round((time.monotonic() - start) * 1000),
    }


if __name__ == "__main__":
    url = os.getenv("TARGET_URL", "http://localhost:8000")
    print(json.dumps(check_url(url)))
