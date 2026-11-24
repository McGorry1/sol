"""Jito block engine: tip accounts, bundle submission, status polling."""
import asyncio
import base64
import httpx

STATUS = "https://mainnet.block-engine.jito.wtf/api/v1/getBundleStatuses"


class BundleError(RuntimeError):
    pass


class Jito:
    def __init__(self, url: str):
        self.url = url

    async def tip_account(self) -> str:
        body = {"jsonrpc": "2.0", "id": 1, "method": "getTipAccounts", "params": []}
        async with httpx.AsyncClient() as c:
            r = await c.post(self.url, json=body, timeout=15.0)
        accounts = r.json().get("result") or []
        if not accounts:
            raise BundleError("no tip accounts returned")
        return accounts[0]

    async def send(self, signed_txs: list[str]) -> str:
        body = {"jsonrpc": "2.0", "id": 1, "method": "sendBundle",
                "params": [signed_txs]}
        async with httpx.AsyncClient() as c:
            r = await c.post(self.url, json=body, timeout=25.0)
        data = r.json()
        if "error" in data:
            raise BundleError(f"sendBundle rejected: {data['error']}")
        return data["result"]

    async def wait(self, bundle_id: str, attempts: int = 20) -> bool:
        body = {"jsonrpc": "2.0", "id": 1, "method": "getBundleStatuses",
                "params": [[bundle_id]]}
        for _ in range(attempts):
            await asyncio.sleep(3)
            async with httpx.AsyncClient() as c:
                r = await c.post(STATUS, json=body, timeout=15.0)
            value = (r.json().get("result") or {}).get("value") or []
            if not value:
                continue
            status = value[0].get("confirmation_status")
            if status in ("confirmed", "finalized"):
                return True
            if status == "failed":
                return False
        return False
