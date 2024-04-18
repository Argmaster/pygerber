"""Wrapper for G74 token."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.bases.token import Token


class EndOfExpression(Token):
    """## 3.3 Commands (`'*' - end of command`).

    Commands are the core syntactic element of the Gerber format. A Gerber file is a stream of
    commands. Commands define the graphics state, create graphical objects, defines apertures,
    manage attributes and so on.

    Commands are built with words, the basic syntactic building block of a Gerber file. A word is a
    non-empty character string, excluding the reserved characters '*' and '%', terminated with an '*'

    ```ebnf
    word = {free_character}+ '*';
    ```

    For historic reasons, there are two command syntax styles: word commands and extended
    commands.

    (...)

    The example below shows a stream of Gerber commands.

    ---

    ## Example

    ```gerber
    G04 Different command styles*
    G75*
    G02*
    D10*
    X0Y0D02*
    X2000000Y0I1000000J0D01*
    D11*
    X0Y2000000D03*
    M02*
    ```

    ---

    See section 3.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=33)

    """  # noqa: E501

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return "*"
