# -*- coding: utf-8 -*-
from collections import deque
from pygerber.mathclasses import BoundingBox
from typing import Tuple

from pygerber.meta import Meta
from pygerber.meta.apertureset import ApertureSet
from pygerber.tokens.token import Token

from .exceptions import EndOfStream, InvalidSyntaxError, TokenNotFound
from .tokens import token_classes


class Tokenizer:

    token_stack: deque  # contains Token objects
    meta: Meta
    source: str = ""
    begin_index: int = 0
    token_stack_size: int = 0
    filepath: str = "<string>"
    bbox: BoundingBox

    def __init__(
        self, apertureSet: ApertureSet, *, ignore_deprecated: bool = True
    ) -> None:
        self.token_stack = deque()
        self.apertureSet = apertureSet
        self.ignore_deprecated = ignore_deprecated
        self.clean_tokenization_data()
        self.bbox = None

    def clean_tokenization_data(self):
        self.meta = Meta(self.apertureSet, ignore_deprecated=self.ignore_deprecated)
        self.begin_index = 0
        self.char_index = 0
        self.line_index = 1

    def render(self) -> None:
        """
        Render all tokens contained in token_stack.
        """
        self.clean_tokenization_data()
        for token in self.token_stack:
            self.render_token(token)

    def render_generator(self, yield_after: int = 10) -> Tuple[int, int]:
        """
        Generator version of render, renders `yield_after` of tokens and
        yields total number of tokens rendered.
        """
        i = 0
        self.clean_tokenization_data()
        for token in self.token_stack:
            self.render_token(token)
            i += 1
            if i % yield_after == 0:
                yield i

    def render_token(self, token: Token) -> None:
        token: Token
        token.affect_meta()
        token.render()

    def tokenize_file(self, filepath: str) -> deque:
        """
        Opens file that filepath is pointing to and tokenizes its contents.
        Deque containing all of the tokens is returned.
        """
        self.filepath = filepath
        source = self.load_file()
        return self.tokenize_string(source)

    def load_file(self) -> str:
        with open(self.filepath, "r", encoding="utf-8") as file:
            source = file.read()
        return source

    def tokenize_string(self, string: str) -> deque:
        """
        Tokenizes source string, assuming that it contains Gerber code.
        Deque containing all of the tokens is returned.
        """
        self.source = string
        return self.tokenize()

    def tokenize(self) -> deque:
        try:
            while not self.hasReachedEnd():
                self.next_token()
        except EndOfStream:
            pass
        else:
            raise InvalidSyntaxError(
                "No explicit indication of end at the end of file."
            )
        return self.token_stack

    def hasReachedEnd(self):
        return self.begin_index >= len(self.source)

    def next_token(self) -> int:
        token: Token = self.find_matching_token()
        token.dispatch(self.meta)
        self.push_token(token)
        self.update_indexes(token)
        token.affect_meta()
        bbox = token.bbox()
        if bbox is not None:
            if self.bbox is None:
                self.bbox = bbox
            else:
                self.bbox += bbox

    def push_token(self, token: Token) -> None:
        if token.keep == True:
            self.token_stack.append(token)
            self.token_stack_size += 1

    def update_indexes(self, token: Token) -> None:
        # update begin index
        self.begin_index = token.re_match.end()
        matched_string: str = token.re_match.group()
        endl_count = matched_string.count("\n")
        # update line index
        self.line_index += endl_count
        source_length = len(matched_string)
        # update char index
        if endl_count == 0:
            self.char_index += source_length
        else:
            last_endl_index = matched_string.rfind("\n")
            self.char_index = source_length - last_endl_index

    def find_matching_token(self):
        for token_class in token_classes:
            if token := token_class.match(
                self.source,
                self.begin_index,
            ):
                return token
        else:
            self.raise_token_not_found()

    def raise_token_not_found(self):
        end_index = min(len(self.source), self.begin_index + 30)
        raise TokenNotFound(
            f'\n  File "{self.filepath}", line {self.line_index}, character {self.char_index}:\n{self.source[self.begin_index:end_index]}'
        )

    def get_bbox(self):
        if self.bbox is not None:
            return self.bbox
        else:
            return BoundingBox(0, 0, 0, 0)
