#!/usr/bin/env python3
"""Playwright + Chromium over an HTTP proxy with username/password.

Chromium does not support SOCKS5 username/password authentication.
Prefer an HTTP proxy with this script, or a local relay that adds SOCKS5 auth.

PROXY_URL must be http://user:pass@host:port (placeholders by default).
Install the browser once with: playwright install chromium
"""

from __future__ import annotations

import os
import sys
from urllib.parse import unquote, urlparse

from playwright.sync_api import sync_playwright

PROXY_URL = os.environ.get("PROXY_URL", "http://user:pass@host:port")


def parse_http_proxy(proxy_url: str) -> tuple[str, str, str]:
    parsed = urlparse(proxy_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            "Use an HTTP proxy URL for this script "
            "(Chromium SOCKS5 auth is not supported). "
            "Example: http://user:pass@host:port"
        )
    if not parsed.hostname or not parsed.port:
        raise ValueError("PROXY_URL must include host and port")
    # PROXY_URL keeps special characters percent-encoded. Playwright wants them raw.
    user = unquote(parsed.username or "user")
    password = unquote(parsed.password or "pass")
    server = f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"
    return server, user, password


def main() -> None:
    if "user:pass@host:port" in PROXY_URL:
        print(
            "Using placeholder PROXY_URL. Export a real value before production use.",
            file=sys.stderr,
        )

    server, user, password = parse_http_proxy(PROXY_URL)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            proxy={"server": server, "username": user, "password": password},
        )
        try:
            page = browser.new_page(locale="vi-VN")
            page.goto("https://api.ipify.org", timeout=60_000)
            print(page.inner_text("body"))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
