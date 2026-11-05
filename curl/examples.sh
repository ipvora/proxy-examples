#!/usr/bin/env bash
# curl examples for HTTP and SOCKS5 proxies. Placeholders only.
# Usage:
#   export PROXY_URL="http://user:pass@host:port"
#   bash curl/examples.sh
set -euo pipefail

PROXY_URL="${PROXY_URL:-http://user:pass@host:port}"

echo "PROXY_URL=${PROXY_URL}"
if [[ "${PROXY_URL}" == *"user:pass@host:port"* ]]; then
  echo "Using placeholder PROXY_URL. Export a real value before production use." >&2
fi

echo "--- HTTP(S) proxy: egress IP ---"
curl --max-time 30 -x "${PROXY_URL}" https://api.ipify.org
echo

echo "--- HTTP(S) proxy: ipinfo JSON ---"
curl --max-time 30 -x "${PROXY_URL}" https://ipinfo.io/json
echo

# SOCKS5 with remote DNS (socks5h). Override with SOCKS_PROXY_URL if needed.
SOCKS_PROXY_URL="${SOCKS_PROXY_URL:-socks5h://user:pass@host:port}"
echo "--- SOCKS5 (socks5h) proxy: egress IP ---"
curl --max-time 30 -x "${SOCKS_PROXY_URL}" https://api.ipify.org
echo

echo "--- verbose HTTP connect (debug) ---"
curl -v --max-time 30 -x "${PROXY_URL}" https://example.com -o /dev/null
