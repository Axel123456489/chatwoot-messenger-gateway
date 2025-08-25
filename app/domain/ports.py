from typing import Awaitable, Callable, Protocol, Set

from app.domain.message import (
    ContactContent,
    LocationContent,
    MediaContent,
    StickerContent,
    TextContent,
    UnifiedMessage,
)

OnMessage = Callable[[UnifiedMessage], Awaitable[None]]


class MessengerAdapter(Protocol):
    """Minimal contract each channel adapter must implement."""

    def on_message(self, cb: OnMessage) -> None: ...
    async def start(self) -> None: ...
    async def stop(self) -> None: ...

    async def send_text(self, recipient_id: str, content: TextContent) -> None: ...
    async def send_media(self, recipient_id: str, content: MediaContent) -> None: ...
    async def send_sticker(
        self, recipient_id: str, content: StickerContent
    ) -> None: ...
    async def send_contact(
        self, recipient_id: str, content: ContactContent
    ) -> None: ...
    async def send_location(
        self, recipient_id: str, content: LocationContent
    ) -> None: ...

    def capabilities(self) -> Set[str]: ...
