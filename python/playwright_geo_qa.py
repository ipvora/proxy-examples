"""Localization QA across regions with Playwright + residential proxies.

Placeholders only. Set one proxy URL per region before running, e.g.:
  export PROXY_URL_VN="http://user:pass@host:port"
  export PROXY_URL_JP="http://user:pass@host:port"
  export PROXY_URL_US="http://user:pass@host:port"
  export TARGET_URL="https://example.com/"
Requires: pip install playwright && playwright install chromium
Only test sites and ads you own or are authorized to test.
"""
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

REGIONS = {
    "VN": {"env": "PROXY_URL_VN", "locale": "vi-VN",
           "timezone": "Asia/Ho_Chi_Minh", "currency": r"₫|VND"},
    "JP": {"env": "PROXY_URL_JP", "locale": "ja-JP",
           "timezone": "Asia/Tokyo", "currency": r"¥|円|JPY"},
    "US": {"env": "PROXY_URL_US", "locale": "en-US",
           "timezone": "America/New_York", "currency": r"\$|USD"},
}

TARGET_URL = os.environ.get("TARGET_URL", "https://example.com/")
OUT_DIR = Path("qa_output")


def playwright_proxy(proxy_url):
    """Chuyển http://user:pass@host:port thành dict mà Playwright yêu cầu."""
    parts = urlsplit(proxy_url)
    proxy = {"server": f"{parts.scheme}://{parts.hostname}:{parts.port}"}
    if parts.username:
        proxy["username"] = parts.username
        proxy["password"] = parts.password or ""
    return proxy


def check_region(browser, code, cfg):
    proxy_url = os.environ.get(cfg["env"])
    if not proxy_url:
        return {"region": code, "skipped": f"thiếu biến {cfg['env']}"}

    context = browser.new_context(
        proxy=playwright_proxy(proxy_url),
        locale=cfg["locale"],
        timezone_id=cfg["timezone"],
        viewport={"width": 1366, "height": 900},
    )
    page = context.new_page()
    result = {"region": code}
    try:
        page.goto("https://ipinfo.io/json", timeout=30_000)
        info = json.loads(page.inner_text("body"))
        result["exit_ip"] = info.get("ip")
        result["exit_country"] = info.get("country")
        result["geo_ok"] = info.get("country") == code

        page.goto(TARGET_URL, wait_until="networkidle", timeout=60_000)
        result["html_lang"] = page.get_attribute("html", "lang")
        result["browser_tz"] = page.evaluate(
            "Intl.DateTimeFormat().resolvedOptions().timeZone")
        text = page.inner_text("body")
        result["currency_found"] = bool(re.search(cfg["currency"], text))

        shot = OUT_DIR / f"{code}.png"
        page.screenshot(path=str(shot), full_page=True)
        result["screenshot"] = str(shot)
    except Exception as exc:  # ghi lỗi để lượt sau xem lại
        result["error"] = repr(exc)
    finally:
        context.close()
    return result


def main():
    OUT_DIR.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        results = [check_region(browser, c, cfg) for c, cfg in REGIONS.items()]
        browser.close()
    (OUT_DIR / "report.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
