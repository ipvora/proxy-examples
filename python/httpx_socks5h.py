#!/usr/bin/env python3
"""SOCKS5h proxy example with httpx. DNS is resolved on the proxy side.

Set PROXY_URL to socks5h://user:pass@host:port.
Requires httpx[socks] (socksio). httpx >= 0.28 accepts the socks5h scheme
and the proxy= client argument.
"""

import asyncio
import os
import sys

import httpx

# Expected form: socks5h://user:pass@host:port
PROXY_URL = os.environ.get("PROXY_URL", "socks5h://user:pass@host:port")


async def fetch_status_codes(urls: list[str]) -> list[int]:
    limits = httpx.Limits(max_connections=5)
    timeout = httpx.Timeout(30.0, connect=10.0)
    async with httpx.AsyncClient(
        proxy=PROXY_URL, limits=limits, timeout=timeout
    ) as client:
        ip_response = await client.get("https://api.ipify.org")
        ip_response.raise_for_status()
        print(ip_response.text.strip())
        responses = await asyncio.gather(*(client.get(url) for url in urls))
        for response in responses:
            response.raise_for_status()
        return [response.status_code for response in responses]


def main() -> None:
    if "user:pass@host:port" in PROXY_URL:
        print(
            "Using placeholder PROXY_URL. Export a real value before production use.",
            file=sys.stderr,
        )
    codes = asyncio.run(
        fetch_status_codes(["https://example.com", "https://example.org"])
    )
    print(codes)


if __name__ == "__main__":
    main()
