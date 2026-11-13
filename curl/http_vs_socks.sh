#!/usr/bin/env bash
# Same credentials over HTTP, socks5 (client DNS), and socks5h (proxy DNS).
# Placeholders only. User, password, host, and port all come from PROXY_URL;
# only the scheme changes. URL-encode special characters in the password.
# Usage:
#   export PROXY_URL="http://user:pass@host:port"
#   bash curl/http_vs_socks.sh
set -euo pipefail

PROXY_URL="${PROXY_URL:-http://user:pass@host:port}"

if [[ "${PROXY_URL}" == *"user:pass@host:port"* ]]; then
  echo "Using placeholder PROXY_URL. Export a real value before production use." >&2
fi

# authority is user:pass@host:port (scheme stripped).
authority="${PROXY_URL#*://}"
authority="${authority%/}"
if [[ -z "${authority}" || "${authority}" == "${PROXY_URL}" ]]; then
  echo "PROXY_URL must look like scheme://user:pass@host:port" >&2
  exit 1
fi

HTTP_URL="http://${authority}"
SOCKS5_URL="socks5://${authority}"
SOCKS5H_URL="socks5h://${authority}"

echo "--- HTTP proxy (proxy resolves DNS) ---"
curl --max-time 30 -x "${HTTP_URL}" https://api.ipify.org
echo

echo "--- SOCKS5 (client resolves DNS) ---"
curl --max-time 30 -x "${SOCKS5_URL}" https://api.ipify.org
echo

echo "--- SOCKS5h (proxy resolves DNS) ---"
curl --max-time 30 -x "${SOCKS5H_URL}" https://api.ipify.org
echo
