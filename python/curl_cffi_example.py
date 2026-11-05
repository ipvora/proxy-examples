#!/usr/bin/env python3
"""HTTP(S) proxy example with curl_cffi. Placeholders only — set PROXY_URL."""

import os
import sys

from curl_cffi import requests

# Expected form: http://user:pass@host:port
PROXY_URL = os.environ.get("PROXY_URL", "http://user:pass@host:port")


def main() -> None:
    if "user:pass@host:port" in PROXY_URL:
        print(
            "Using placeholder PROXY_URL. Export a real value before production use.",
            file=sys.stderr,
        )
    proxies = {"http": PROXY_URL, "https": PROXY_URL}
    response = requests.get(
        "https://api.ipify.org",
        proxies=proxies,
        timeout=30,
        impersonate="chrome",
    )
    response.raise_for_status()
    print(response.text)


if __name__ == "__main__":
    main()
