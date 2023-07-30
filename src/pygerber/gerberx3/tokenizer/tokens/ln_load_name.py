"""### Load Name (LN).

Note: The LN command was deprecated in revision I4 from October 2013.

The historic `LN` command doesn't influence the image in any manner and can safely be
overlooked.

Function of the `LN` command:
- `LN` is designed to allocate a name to the following section of the file.
- It was originally conceptualized to serve as a human-readable comment.
- For creating human-readable comments, it's advisable to utilize the standard `G04`
    command.
- The `LN` command has the flexibility to be executed multiple times within a file.

SPEC: `2023.03` SECTION: `8.1.6`
"""


from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pygerber.gerberx3.tokenizer.tokens.token import Token

if TYPE_CHECKING:
    from typing_extensions import Self


class LoadName(Token):
    """Comment token.

    ### Load Name (LN)

    Note: The LN command was deprecated in revision I4 from October 2013.

    The historic `LN` command doesn't influence the image in any manner and can safely
    be overlooked.

    Function of the `LN` command:
    - `LN` is designed to allocate a name to the following section of the file.
    - It was originally conceptualized to serve as a human-readable comment.
    - For creating human-readable comments, it's advisable to utilize the standard `G04`
        command.
    - The `LN` command has the flexibility to be executed multiple times within a file.

    SPEC: `2023.03` SECTION: `8.1.6`
    """

    content: str

    @classmethod
    def from_tokens(cls, **tokens: Any) -> Self:
        """Initialize token object."""
        content: str = tokens["string"]
        return cls(content=content)

    def __str__(self) -> str:
        return f"%LN {self.content}*%"
