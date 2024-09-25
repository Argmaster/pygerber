from __future__ import annotations

import asyncio
import threading
from contextlib import suppress
from typing import TYPE_CHECKING, Any, Optional

from pygerber.gerber.language_server.status import is_language_server_available

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self

if is_language_server_available():
    import lsprotocol.types as lspt
    from pygls.server import LanguageServer  # noqa: TCH002


class Document:
    """The `Document` class represents a single document."""

    def __init__(self, gls: LanguageServer) -> None:
        self.gls = gls
        self.async_lock = asyncio.Lock()
        self.thread_lock = threading.Lock()

    async def on_open(self, params: lspt.DidOpenTextDocumentParams) -> None:
        """Handle the document open event."""

    async def on_close(self, params: lspt.DidCloseTextDocumentParams) -> None:
        """Handle the document close event."""

    async def on_change(self, params: lspt.DidChangeTextDocumentParams) -> None:
        """Handle the document change event."""

    async def on_hover(self, params: lspt.HoverParams) -> lspt.Hover | None:
        """Handle the hover event."""

    async def on_completion(
        self, params: lspt.CompletionParams
    ) -> lspt.CompletionList | None:
        """Handle the completion event."""

    def log_info(self, msg: Any) -> None:
        """Log an informational message to server log."""
        self.gls.show_message_log(str(msg), lspt.MessageType.Info)

    async def __aenter__(self) -> Self:
        await self.acquire()
        return self

    async def acquire(self) -> None:
        try:
            self.thread_lock.acquire()
            await self.async_lock.acquire()

        except Exception:
            with suppress(Exception):
                self.thread_lock.release()

            with suppress(Exception):
                self.async_lock.release()

            raise

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.release()

    async def release(self) -> None:
        with suppress(Exception):
            self.async_lock.release()

        with suppress(Exception):
            self.thread_lock.release()
