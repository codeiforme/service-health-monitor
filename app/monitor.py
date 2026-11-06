import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


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


def send_event(webhook_url, event):
    body = json.dumps(event).encode()
    request = Request(webhook_url, data=body,
                      headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=3) as response:
            return 200 <= response.status < 300
    except (URLError, OSError) as error:
        print("Webhook failed:", error, flush=True)
        return False


def main():
    url = os.getenv("TARGET_URL", "http://localhost:8000/health")
    interval = int(os.getenv("CHECK_INTERVAL", "10"))
    if interval < 1:
        raise SystemExit("CHECK_INTERVAL must be at least 1 second")
    webhook_url = os.getenv("WEBHOOK_URL", "")
    last_sent_status = None

    while True:
        result = check_url(url)
        result["target"] = url
        result["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        print(json.dumps(result), flush=True)

        if webhook_url and result["status"] != last_sent_status:
            if send_event(webhook_url, result):
                last_sent_status = result["status"]

        time.sleep(interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Monitor stopped")
