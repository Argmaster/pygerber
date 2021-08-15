from collections import deque
from pygerber.tokens.token import Token

from pygerber.meta import Meta

from .exceptions import TokenNotFound
from .tokens import token_classes


class GerberParser:

    TOKEN_STACK: deque
    meta: Meta
    source: str = ""
    begin_index: int = 0

    def clean(self):
        self.TOKEN_STACK = deque()
        self.meta = Meta()
        self.begin_index = 0
        self.char_index = 0
        self.line_indxe = 0

    def evaluate(self, backend) -> None:
        pass

    def tokenize_string(self, string: str) -> None:
        self.source = string
        self.clean()
        while self.begin_index < len(self.source):
            token = self.find_matching_token()
            self.push_token(token)
            self.update_indexes(token)

    def push_token(self, token: Token) -> None:
        self.TOKEN_STACK.append(token)

    def update_indexes(self, token: Token) -> None:
        pass

    def find_matching_token(self):
        for token_class in token_classes:
            if token := token_class.match(
                self.meta,
                self.source,
                self.begin_index,
            ):
                return token
        else:
            self.raise_token_not_found()

    def raise_token_not_found(self):
        end_index = min(len(self.source), 30)
        line_index = self.source.count("\n", 0, self.begin_index)
        raise TokenNotFound(
            f"No matching token in line {line_index}: {self.source[self.begin_index:end_index]}"
        )
