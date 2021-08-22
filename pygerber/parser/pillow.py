# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.meta.apertureset import ApertureSet
from pygerber.tokenizer import Tokenizer


class ParserWithPillow:

    tokenizer: Tokenizer
    apertureSet = ApertureSet()

    def __init__(
        self,
        filepath: str,
        *,
        dpi: int = 600,
        ignore_deprecated: bool = True,
    ) -> None:
        self.dpi = dpi
        self.tokenizer = Tokenizer(
            self.apertureSet,
            ignore_deprecated=ignore_deprecated,
        )
        self.tokenizer.tokenize_file(filepath)

    def render(self):
        return self.tokenizer.render()

    def render_generator(self, yield_after: int = 10):
        return self.tokenizer.render_generator(yield_after)
