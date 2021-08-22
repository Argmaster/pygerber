# -*- coding: utf-8 -*-
from collections import deque

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

    def __init__(self, apertureSet: ApertureSet) -> None:
        self.token_stack = deque()
        self.meta = Meta(apertureSet)
        self.begin_index = 0
        self.char_index = 0
        self.line_index = 1

    def evaluate(self) -> None:
        pass

    def tokenize_file(self, filepath: str) -> None:
        self.filepath = filepath
        source = self.load_file()
        self.tokenize_string(source)

    def load_file(self) -> str:
        with open(self.filepath, "r", encoding="utf-8") as file:
            source = file.read()
        return source

    def tokenize_string(self, string: str) -> deque:
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

    def next_token(self):
        token: Token = self.find_matching_token()
        token.dispatch(self.meta)
        self.push_token(token)
        self.update_indexes(token)
        token.affect_meta()

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
