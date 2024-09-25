from __future__ import annotations

import asyncio
import threading
from contextlib import suppress
from typing import TYPE_CHECKING, Optional

from pygerber.gerber.language_server._server.documents.document import Document

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self


class DocumentCache:
    def __init__(self) -> None:
        self.documents: dict[str, Document] = {}
        self.async_lock = asyncio.Lock()
        self.thread_lock = threading.Lock()

    def get(self, uri: str) -> Document | None:
        return self.documents.get(uri)

    def set(self, uri: str, document: Document) -> None:
        self.documents[uri] = document

    def delete(self, uri: str) -> None:
        del self.documents[uri]

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
