# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import ABC, abstractmethod
from pygerber.mathclasses import BoundingBox
from pygerber.tokens.token import Token
from typing import Deque
from pygerber.renderer import Renderer
from pygerber.tokenizer import Tokenizer
from pygerber.renderer.apertureset import ApertureSet



class AbstractParser(ABC):

    apertureSet: ApertureSet

    def __init__(self, ignore_deprecated: bool=True) -> None:
        self.tokenizer = Tokenizer(ignore_deprecated)
        self.renderer = Renderer(self.apertureSet)

    def parse_file(self, file_path: str):
        with open(file_path) as file:
            source_string = file.read()
        self.parse(source_string, file_path)

    def parse(self, source_string: str, file_path: str="<string>"):
        token_stack = self.tokenizer.tokenize(source_string, file_path)
        bbox = self.renderer.total_bounding_box(token_stack)
        self._pre_render(bbox)
        self._render(token_stack)

    def _pre_render(self, bbox: BoundingBox):
        pass

    @abstractmethod
    def _render(self, token_stack: Deque[Token]):
        pass

    @abstractmethod
    def save(self, file_path: str, format: str = None) -> None:
        pass