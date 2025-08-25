import logging
from typing import Optional

from pyee.asyncio import AsyncIOEventEmitter

from app.config import WasenderWebhookConfig
from app.domain.message import TextContent, UnifiedMessage
from app.domain.ports import MessengerAdapter, OnMessage
from app.domain.webhooks.wasender import WasenderWebhookPayload
from app.infra.wasender_client import WasenderClient

logger = logging.getLogger(__name__)


class WasenderAdapter(MessengerAdapter):
    """WhatsApp adapter (text only) via Wasender."""

    def __init__(self, bus: AsyncIOEventEmitter, config: WasenderWebhookConfig):
        self._bus = bus
        self._config = config
        self.inbox_id = config.inbox_id  # expose per-channel inbox
        self._cb: Optional[OnMessage] = None
        self._client = WasenderClient(api_key=self._config.api_key)

    def on_message(self, cb: OnMessage) -> None:
        self._cb = cb

    async def start(self) -> None:
        @self.bus.on("wasender.incoming")
        async def _incoming(payload: dict):
            if not self._cb:
                logger.warning("[wasender] No on_message callback set; dropping event")
                return

            try:
                parsed = WasenderWebhookPayload.model_validate(payload)
            except Exception as e:
                logger.warning("[wasender] Invalid webhook payload: %s", e)
                return

            if parsed.event != "messages.upsert":
                logger.info("[wasender] Ignored event: %s", parsed.event)
                return

            info = parsed.get_basic_info()
            if not info:
                logger.warning("[wasender] Missing basic message info; skipping")
                return

            if info.get("fromMe") is True:
                logger.info(
                    "[wasender] Skipping echo/outgoing message id=%s", info.get("id")
                )
                return

            text = info.get("text") or ""
            if not text:
                logger.info(
                    "[wasender] Skipping non-text message from %s",
                    info.get("remoteJid"),
                )
                return

            recipient_id = (info.get("remoteJid") or "").split("@")[0]
            msg = UnifiedMessage(
                channel="whatsapp",
                recipient_id=recipient_id,
                sender_id=recipient_id,
                sender_name=info.get("pushName"),
                content=TextContent(type="text", text=text),
                raw=payload,
            )
            try:
                await self._cb(msg)
            except Exception as e:
                logger.exception("[wasender] on_message callback failed: %s", e)

        @self.bus.on("wasender.outgoing")
        async def _outgoing(payload: dict):
            logger.debug("[wasender] Outgoing event received (noop)")

        logger.info("[wasender] adapter started (listening for incoming messages)")

    async def stop(self) -> None:
        logger.info("[wasender] adapter stopped")

    async def send_text(self, recipient_id: str, content: TextContent) -> None:
        """Send text via Wasender."""
        text = content.text
        try:
            await self._client.send_text(to=recipient_id, text=text)
            logger.info("[wasender] SENT: %s -> %s", recipient_id, text)
        except Exception as e:
            logger.exception("[wasender] Failed to send text: %s", e)
