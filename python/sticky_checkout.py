#!/usr/bin/env python3
"""Multi-step flow on one proxy session (sticky or static IP).

Placeholders only — set PROXY_URL. requests.Session keeps cookies across steps.
The URLs below are public echo endpoints, not a payment gateway. Point them
at a staging system you are allowed to test before using this for real QA.
"""

import os
import sys

import requests

# Expected form: http://user:pass@host:port or socks5h://user:pass@host:port
PROXY_URL = os.environ.get("PROXY_URL", "http://user:pass@host:port")


def run_checkout_qa() -> None:
    session = requests.Session()
    session.proxies = {"http": PROXY_URL, "https": PROXY_URL}
    session.headers["User-Agent"] = "checkout-qa/1.0 (+mailto:you@example.com)"
    timeout = (10, 30)

    # Public URLs illustrate step order only.
    steps = [
        ("GET", "view page", "https://httpbin.org/html"),
        ("POST", "add to cart (simulated)", "https://httpbin.org/post"),
        ("GET", "checkout page (simulated)", "https://httpbin.org/headers"),
    ]

    for method, name, url in steps:
        if method == "POST":
            response = session.post(
                url, data={"item": "demo", "qty": "1"}, timeout=timeout
            )
        else:
            response = session.get(url, timeout=timeout)
        response.raise_for_status()
        print(name, response.status_code, len(response.content))


def main() -> None:
    if "user:pass@host:port" in PROXY_URL:
        print(
            "Using placeholder PROXY_URL. Export a real value before production use.",
            file=sys.stderr,
        )
    run_checkout_qa()


if __name__ == "__main__":
    main()
