# ipvora proxy examples

Runnable HTTP / HTTPS / SOCKS5 examples for residential proxies. Values are placeholders only (`user:pass@host:port`). Replace them before running. Do not commit real credentials.

Primary docs: [GitHub Pages](https://ipvora.github.io/) · [ipvora.com](https://www.ipvora.com) · [GitBook](https://ipvora.gitbook.io/ipvora-docs)

This repository is maintained by the ipvora docs team. License: MIT.

## Quick start

```bash
# Set a single proxy URL (placeholder form)
export PROXY_URL="http://user:pass@host:port"
# SOCKS5 example:
# export PROXY_URL="socks5h://user:pass@host:port"

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python python/requests_http.py
python python/requests_socks5.py
python python/httpx_socks5h.py
python python/curl_cffi_example.py
python python/static_ip_check.py
python python/sticky_checkout.py
# Selenium needs a local Chrome/Chromium install:
# python python/selenium_http_proxy.py
# Playwright needs a Chromium install: playwright install chromium
# python python/playwright_http_proxy.py

bash curl/examples.sh
bash curl/http_vs_socks.sh
```

### Environment variable

| Variable   | Description |
|------------|-------------|
| `PROXY_URL` | Full proxy URL, e.g. `http://user:pass@host:port` or `socks5h://user:pass@host:port` |

Special characters in username/password must be URL-encoded.

## Layout

```
python/requests_http.py         # requests over HTTP proxy
python/requests_socks5.py       # requests over SOCKS5h (needs PySocks)
python/httpx_socks5h.py         # httpx over SOCKS5h (needs httpx[socks])
python/curl_cffi_example.py     # curl_cffi HTTP proxy
python/static_ip_check.py       # same egress IP across repeated requests
python/sticky_checkout.py       # one session across checkout-style steps
python/selenium_http_proxy.py   # Selenium + Chrome HTTP proxy
python/playwright_http_proxy.py # Playwright + Chromium HTTP proxy
curl/examples.sh                # curl HTTP and SOCKS5 checks
curl/http_vs_socks.sh           # same URL over HTTP, socks5, and socks5h
```

## Notes

- Chrome does not support SOCKS5 username/password authentication well. Prefer an HTTP proxy with Selenium, or a local relay that adds auth.
- Chromium (Playwright) does not support SOCKS5 username/password authentication. Use an HTTP proxy, or a local relay.
- `socks5://` resolves DNS on the client. `socks5h://` sends the hostname to the proxy. Prefer `socks5h` when the site uses GeoDNS.
- Residential connections can be slower than datacenter; use explicit timeouts and retries.
- For sticky sessions, country targeting, and product details, see the docs links above.

## Related guides (Vietnamese)

- [Dùng residential proxy trong Python: rotating hay sticky session? (ví dụ với requests, httpx và Playwright)](https://viblo.asia/p/dung-residential-proxy-trong-python-rotating-hay-sticky-session-vi-du-voi-requests-httpx-va-playwright-7Z4DEWAoJnX)
- [Proxy dân cư tĩnh (ISP): khi nào nên thuê IP cố định thay vì xoay?](https://dev.to/ipvora/proxy-dan-cu-tinh-isp-khi-nao-nen-thue-ip-co-dinh-thay-vi-xoay-1jp6)
- [SOCKS5 hay HTTP/HTTPS proxy: chọn giao thức nào cho scraper, bot kiểm thử và công cụ dòng lệnh?](https://haiwaihuiguo.substack.com/p/socks5-hay-httphttps-proxy-chon-giao)

---

**Tiếng Việt (ngắn):** Repo ví dụ proxy HTTP/HTTPS/SOCKS5 cho ipvora. Chỉ dùng placeholder; đặt `PROXY_URL` rồi chạy script. Tài liệu: https://ipvora.github.io/ · https://www.ipvora.com · https://ipvora.gitbook.io/ipvora-docs. Do đội ngũ tài liệu ipvora duy trì. MIT.
