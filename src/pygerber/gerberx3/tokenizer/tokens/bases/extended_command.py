"""Base class for all extended commands."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.bases.token import Token


class ExtendedCommandToken(Token):
    """## 3.3 Commands.

    Commands are the core syntactic element of the Gerber format. A Gerber file is a stream of
    commands. Commands define the graphics state, create graphical objects, defines apertures,
    manage attributes and so on.

    Commands are built with words, the basic syntactic building block of a Gerber file. A word is a
    non-empty character string, excluding the reserved characters '*' and '%', terminated with an '*'

    ```ebnf
    free_character = /[^%*]/; # All characters but * and %
    word = {free_character}+ '*';
    ```

    For historic reasons, there are two command syntax styles: word commands and extended
    commands.

    ```ebnf
    command =
    | extended_command
    | word_command
    ;
    word_command = word;
    extended_command = '%' {word}+ '%';
    ```


    Word commands are identified by a command code, the letter G, D or M followed by a positive
    integer, e.g. `G02`. Most word commands only consist of the command code, some also contain
    coordinates.

    Extended commands are identified by a two-character command code that is followed by
    parameters specific to the code. An extended command is enclosed by a pair of "%" delimiters

    An overview of all commands is in section 2.8, a full description in chapters 3.5 and 5.


    ---

    ## Example 1

    The example below shows a stream of Gerber commands.

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

    ## Example 2

    The example below shows a stream of Gerber extended commands.

    ```gerber
    %FSLAX26Y26*%
    %MOMM*%
    %AMDonut*
    1,1,$1,$2,$3*
    $4=$1x0.75*
    1,0,$4,$2,$3*
    %
    %ADD11Donut,0.30X0X0*%
    %ADD10C,0.1*%
    ```

    ---

    See section 3.3 of [The Gerber Layer Format Specification](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf#page=33)

    """  # noqa: E501

    def get_gerber_code_one_line_pretty_display(self) -> str:
        """Get gerber code represented by this token."""
        return f"%{self.get_gerber_code()}*%"
