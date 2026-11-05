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
python python/curl_cffi_example.py
# Selenium needs a local Chrome/Chromium install:
# python python/selenium_http_proxy.py

bash curl/examples.sh
```

### Environment variable

| Variable   | Description |
|------------|-------------|
| `PROXY_URL` | Full proxy URL, e.g. `http://user:pass@host:port` or `socks5h://user:pass@host:port` |

Special characters in username/password must be URL-encoded.

## Layout

```
python/requests_http.py       # requests over HTTP proxy
python/requests_socks5.py     # requests over SOCKS5 (needs PySocks)
python/curl_cffi_example.py   # curl_cffi HTTP proxy
python/selenium_http_proxy.py # Selenium + Chrome HTTP proxy
curl/examples.sh              # curl HTTP and SOCKS5 checks
```

## Notes

- Chrome does not support SOCKS5 username/password authentication well. Prefer an HTTP proxy with Selenium, or a local relay that adds auth.
- Residential connections can be slower than datacenter; use explicit timeouts and retries.
- For sticky sessions, country targeting, and product details, see the docs links above.

---

**Tiếng Việt (ngắn):** Repo ví dụ proxy HTTP/HTTPS/SOCKS5 cho ipvora. Chỉ dùng placeholder; đặt `PROXY_URL` rồi chạy script. Tài liệu: https://ipvora.github.io/ · https://www.ipvora.com · https://ipvora.gitbook.io/ipvora-docs. Do đội ngũ tài liệu ipvora duy trì. MIT.
