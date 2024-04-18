"""Comment token."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.tokenizer.tokens.bases.command import CommandToken

if TYPE_CHECKING:
    from pyparsing import ParseResults
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class Comment(CommandToken):
    """## 4.1 Comment (G04).

    The G04 command is used for human readable comments. It does not affect the image.
    The syntax for G04 is as follows.

    ```ebnf
    G04 = ('G04' string) '*';
    ```

    The string must follow the string syntax in [3.4.3](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=35).

    ---

    ## Example

    ```gerber
    G04 This is a comment*
    G04 The space characters as well as "," and ";" are allowed here.*
    ```

    ---

    See section 4.1 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=44)

    """

    def __init__(self, string: str, location: int, content: str) -> None:
        super().__init__(string, location)
        self.content = content

    @classmethod
    def new(cls, string: str, location: int, tokens: ParseResults) -> Self:
        """Create instance of this class.

        Created to be used as callback in `ParserElement.set_parse_action()`.
        """
        content: str = str(tokens["string"])
        return cls(string=string, location=location, content=content)

    def parser2_visit_token(self, context: Parser2Context) -> None:
        """Perform actions on the context implicated by this token."""
        context.get_hooks().comment.pre_parser_visit_token(self, context)
        context.get_hooks().comment.on_parser_visit_token(self, context)
        context.get_hooks().comment.post_parser_visit_token(self, context)

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return f"{indent}G04 {self.content}"
