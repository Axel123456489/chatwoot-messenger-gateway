from typing import Optional

from pydantic import BaseModel


class WasenderMessageKey(BaseModel):
    remoteJid: str
    fromMe: bool
    id: str


class WasenderMessage(BaseModel):
    conversation: Optional[str] = None


class WasenderMessagesPayload(BaseModel):
    key: WasenderMessageKey
    pushName: Optional[str] = None
    message: Optional[WasenderMessage] = None


class WasenderWebhookPayload(BaseModel):
    """Minimal model for Wasender 'messages.upsert' webhook."""

    event: str
    data: dict  # keep generic for now

    def get_basic_info(self):
        """Extract basic message data (if available)."""
        try:
            msg_data = self.data["messages"]
            key = msg_data.get("key", {})
            text = (msg_data.get("message") or {}).get("conversation")
            return {
                "fromMe": key.get("fromMe"),
                "remoteJid": key.get("remoteJid"),
                "id": key.get("id"),
                "text": text,
                "pushName": msg_data.get("pushName"),
            }
        except Exception:
            return None
