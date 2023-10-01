from __future__ import annotations

from hashlib import sha256
from typing import Optional

from pygerber.gerberx3.tokenizer.tokenizer import Tokenizer
from pygerber.gerberx3.tokenizer.tokens.groups.ast import AST

MAX_CACHE_SIZE = 64
TOKENIZER_CACHE: dict[bytes, AST] = {}
TOKENIZER: Optional[Tokenizer] = None


def tokenize(source: str) -> AST:
    sha = sha256(source.encode("utf-8")).digest()
    if (ast := TOKENIZER_CACHE.get(sha, None)) is not None:
        return ast

    ast = get_tokenizer().tokenize_expressions(source)
    if len(TOKENIZER_CACHE) > MAX_CACHE_SIZE:
        TOKENIZER_CACHE.popitem()

    TOKENIZER_CACHE[sha] = ast
    return ast


def get_tokenizer() -> Tokenizer:
    global TOKENIZER  # noqa: PLW0603
    if TOKENIZER is None:
        TOKENIZER = Tokenizer()
    return TOKENIZER
