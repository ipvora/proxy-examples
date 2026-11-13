#!/usr/bin/env python3
"""Check that a sticky or static proxy keeps the same egress IP.

Placeholders only — set PROXY_URL to http://user:pass@host:port
or socks5h://user:pass@host:port. The same URL is reused for every request.
URL-encode special characters in the username or password before exporting it.
"""

import os
import sys
import time

import requests

# Expected form: http://user:pass@host:port or socks5h://user:pass@host:port
PROXY_URL = os.environ.get("PROXY_URL", "http://user:pass@host:port")


def get_exit_ip(session: requests.Session) -> str:
    response = session.get("https://api.ipify.org?format=json", timeout=(10, 30))
    response.raise_for_status()
    return response.json()["ip"]


def verify_stable_ip(checks: int = 5, pause_s: float = 2.0) -> str:
    session = requests.Session()
    session.proxies.update({"http": PROXY_URL, "https": PROXY_URL})
    session.headers["User-Agent"] = "qa-static-check/1.0 (+mailto:you@example.com)"

    first_ip = get_exit_ip(session)
    for i in range(1, checks):
        time.sleep(pause_s)
        current = get_exit_ip(session)
        if current != first_ip:
            raise SystemExit(
                f"IP changed on check {i + 1}: {first_ip} -> {current}. "
                "A static or sticky proxy should keep the same egress IP. "
                "Check that PROXY_URL points at that gateway."
            )
    print(f"IP unchanged after {checks} checks: {first_ip}")
    return first_ip


def main() -> None:
    if "user:pass@host:port" in PROXY_URL:
        print(
            "Using placeholder PROXY_URL. Export a real value before production use.",
            file=sys.stderr,
        )
    verify_stable_ip()


if __name__ == "__main__":
    main()
