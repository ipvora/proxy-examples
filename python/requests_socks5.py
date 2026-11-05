#!/usr/bin/env python3
"""SOCKS5 proxy example with requests. Requires PySocks (pip install PySocks).

Set PROXY_URL to socks5h://user:pass@host:port
(socks5h = DNS resolved on the proxy side).
"""

import os
import sys
import time

import requests

# Expected form: socks5h://user:pass@host:port
PROXY_URL = os.environ.get("PROXY_URL", "socks5h://user:pass@host:port")


def fetch(url: str, retries: int = 3) -> requests.Response:
    # requests uses PySocks when the scheme is socks5 / socks5h
    proxies = {"http": PROXY_URL, "https": PROXY_URL}
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, proxies=proxies, timeout=(10, 30))
            if response.status_code in (429, 502, 503):
                raise requests.HTTPError(f"status {response.status_code}")
            return response
        except requests.RequestException:
            if attempt == retries:
                raise
            time.sleep(2**attempt)


def main() -> None:
    if "user:pass@host:port" in PROXY_URL:
        print(
            "Using placeholder PROXY_URL. Export a real value before production use.",
            file=sys.stderr,
        )
    text = fetch("https://api.ipify.org").text
    print(text)


if __name__ == "__main__":
    main()
