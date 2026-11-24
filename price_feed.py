"""Real market data. Replaces every literal in position_monitor."""
import time
import httpx

DEX = "https://api.dexscreener.com/latest/dex/tokens/"
RPC = None
_cache: dict[str, tuple[float, dict]] = {}
TTL = 20.0


async def _get(client: httpx.AsyncClient, url: str, **kw):
    r = await client.get(url, timeout=12.0, **kw)
    r.raise_for_status()
    return r.json()


async def token_stats(mint: str, rpc_url: str) -> dict:
    now = time.time()
    if mint in _cache and now - _cache[mint][0] < TTL:
        return _cache[mint][1]

    out = {"price_usd": 0.0, "liquidity_usd": 0.0, "volume_24h": 0.0,
           "holders": 0, "market_cap": 0.0, "live": False}

    async with httpx.AsyncClient() as c:
        try:
            data = await _get(c, DEX + mint)
            pairs = [p for p in (data.get("pairs") or []) if p.get("chainId") == "solana"]
            if pairs:
                p = max(pairs, key=lambda x: (x.get("liquidity") or {}).get("usd", 0) or 0)
                out.update(
                    price_usd=float(p.get("priceUsd") or 0),
                    liquidity_usd=float((p.get("liquidity") or {}).get("usd") or 0),
                    volume_24h=float((p.get("volume") or {}).get("h24") or 0),
                    market_cap=float(p.get("marketCap") or p.get("fdv") or 0),
                    live=True,
                )
        except Exception:
            pass

        try:
            body = {"jsonrpc": "2.0", "id": 1, "method": "getTokenLargestAccounts", "params": [mint]}
            r = await c.post(rpc_url, json=body, timeout=12.0)
            accounts = r.json().get("result", {}).get("value") or []
            out["holders"] = len(accounts)
        except Exception:
            pass

    _cache[mint] = (now, out)
    return out


def is_rug_worthy(s: dict) -> bool:
    return (
        s["live"]
        and s["liquidity_usd"] >= 2_000
        and s["holders"] >= 30
        and s["price_usd"] > 0
    )
