import logging

import httpx

logger = logging.getLogger(__name__)


class WasenderClient:
    """Minimal async client for sending text messages via Wasender API (demo only)."""

    def __init__(self, api_key: str, base_url: str = "https://www.wasenderapi.com/api"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def send_text(self, to: str, text: str) -> dict:
        """Send a plain text message. Adjust endpoint if your Wasender differs."""
        payload = {"to": to, "text": text}
        url = f"{self.base_url}/send-message"
        async with httpx.AsyncClient(headers=self._headers, timeout=15) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            logger.info("[wasender] API send_message ok: to=%s", to)
            return data
