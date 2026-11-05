#!/usr/bin/env python3
"""Selenium + Chrome over an HTTP proxy with username/password.

Chrome does not support SOCKS5 username/password authentication reliably.
Prefer an HTTP proxy with this script, or a local relay that adds SOCKS5 auth.

PROXY_URL must be http://user:pass@host:port (placeholders by default).
Requires a local Chrome/Chromium binary (Selenium 4 Manager resolves the driver).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PROXY_URL = os.environ.get("PROXY_URL", "http://user:pass@host:port")


def parse_http_proxy(proxy_url: str) -> tuple[str, str, str, int]:
    parsed = urlparse(proxy_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            "Use an HTTP proxy URL for this script "
            "(Chrome SOCKS5 auth is limited). "
            "Example: http://user:pass@host:port"
        )
    if not parsed.hostname or not parsed.port:
        raise ValueError("PROXY_URL must include host and port")
    user = parsed.username or "user"
    password = parsed.password or "pass"
    return user, password, parsed.hostname, int(parsed.port)


def build_proxy_auth_extension(user: str, password: str, host: str, port: int) -> str:
    """Build a temporary Chrome extension that supplies Proxy-Authorization."""
    manifest = {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "proxy-auth-placeholder",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking",
        ],
        "background": {"scripts": ["background.js"]},
        "minimum_chrome_version": "22.0.0",
    }
    background = f"""
var config = {{
  mode: "fixed_servers",
  rules: {{
    singleProxy: {{
      scheme: "http",
      host: {json.dumps(host)},
      port: {port}
    }},
    bypassList: ["localhost"]
  }}
}};
chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
function callbackFn(details) {{
  return {{
    authCredentials: {{
      username: {json.dumps(user)},
      password: {json.dumps(password)}
    }}
  }};
}}
chrome.webRequest.onAuthRequired.addListener(
  callbackFn,
  {{urls: ["<all_urls>"]}},
  ["blocking"]
);
"""
    tmp = tempfile.mkdtemp(prefix="chrome-proxy-auth-")
    zip_path = Path(tmp) / "proxy_auth_extension.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("manifest.json", json.dumps(manifest))
        zf.writestr("background.js", background)
    return str(zip_path)


def main() -> None:
    if "user:pass@host:port" in PROXY_URL:
        print(
            "Using placeholder PROXY_URL. Export a real value before production use.",
            file=sys.stderr,
        )

    user, password, host, port = parse_http_proxy(PROXY_URL)
    extension = build_proxy_auth_extension(user, password, host, port)

    options = Options()
    options.add_extension(extension)
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    try:
        driver.set_page_load_timeout(60)
        driver.get("https://api.ipify.org")
        print(driver.find_element("tag name", "body").text)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
