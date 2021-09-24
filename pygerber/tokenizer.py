# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Deque

if TYPE_CHECKING:
    from pathlib import Path
    from pygerber.tokens.token import Token

from pygerber.drawing_state import DrawingState

from .exceptions import DeprecatedSyntax, EndOfStream, InvalidSyntaxError, TokenNotFound
from .tokens import token_classes

DEFAULT_TRACE_FILEPATH = "<string>"


class Tokenizer:

    token_stack: deque  # contains Token objects
    state: DrawingState
    token_stack_size: int = 0
    begin_index: int = 0
    char_index = 0
    line_index = 1

    def __init__(self, ignore_deprecated: bool = True) -> None:
        self.ignore_deprecated = ignore_deprecated
        self.token_stack = deque()
        self.state = DrawingState()
        self.set_defaults()

    def set_defaults(self):
        self.state.set_defaults()
        self.token_stack_size = 0
        self.begin_index = 0
        self.char_index = 0
        self.line_index = 1

    def tokenize_file(self, file_path: str | Path) -> Deque[Token]:
        with open(file_path) as file:
            source = file.read()
        return self.tokenize(source, file_path)

    def tokenize(self, source, file_path: str = "<string>") -> Deque[Token]:
        try:
            while not self.__has_reached_end(source):
                self.__next_token(source)
        except EndOfStream:
            pass
        except InvalidSyntaxError as e:
            raise e.__class__(
                f"""File "{file_path}", line {self.line_index}, char {self.char_index}:\n{e}"""
            ) from e
        else:
            raise InvalidSyntaxError(
                """File "{file_path}",No explicit indication of end at the end of source."""
            )
        return self.token_stack

    def __next_token(self, source) -> int:
        token: Token = self.__find_matching_token(source)
        self.__check_deprecated_syntax(token.__deprecated__)
        self.push_token(token)
        self.__update_indexes(token)
        token.alter_state(self.state)
        # token.alter_state()
        # token.pre_render()
        # self.__update_bbox(token.bbox())
        # token.post_render()

    def __check_deprecated_syntax(self, message: str):
        if message is not None and not self.ignore_deprecated:
            raise DeprecatedSyntax(message)

    def __find_matching_token(self, source):
        for token_class in token_classes:
            re_match = token_class.regex.match(source, pos=self.begin_index)
            if re_match is not None:
                return token_class(re_match, self.state)
        else:
            self.raise_token_not_found(source)

    def __has_reached_end(self, source):
        return self.begin_index >= len(source)

    # def __update_bbox(self, bbox: BoundingBox):
    #     if bbox is not None:
    #         if self.bbox is None:
    #             self.bbox = bbox
    #         else:
    #             self.bbox += bbox

    def push_token(self, token: Token) -> None:
        if token.keep == True:
            self.token_stack.append(token)
            self.token_stack_size += 1

    def __update_indexes(self, token: Token) -> None:
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

    def raise_token_not_found(self, source):
        end_index = min(len(source), self.begin_index + 30)
        raise TokenNotFound(f"{source[self.begin_index:end_index]}")
