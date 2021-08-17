from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from pygerber.exceptions import InvalidCommandFormat, suppress_context
from pygerber.validators.validator import Validator

if TYPE_CHECKING:
    from pygerber.meta import Meta


class ValidatorDispatcher:
    """
    Whenever You subclass ValidatorDispatcher, you have to wrap your class
    in @load_validators decorator from pygerber.validators to preload validators
    into class when it is created. If U won't do it, your code will fail.
    """

    validators: Dict[str, Validator]

    def dispatch(self, meta: Meta) -> None:
        self.dispatch_into_namespace(meta, self)

    def dispatch_into_namespace(self, meta: Meta, namespace: object) -> object:
        self.meta = meta
        group_dict = self.get_groupdict()
        for attribute_name, validator in self.validators.items():
            try:
                value = group_dict.get(attribute_name, None)
                cleaned_value = validator(self, value)
                setattr(namespace, attribute_name, cleaned_value)
            except ValueError as e:
                self.raise_invalid_format(e.__str__())
        return namespace

    def get_groupdict(self) -> dict:
        if self.re_match is not None:
            return self.re_match.groupdict()
        else:
            return {}

    def raise_invalid_format(self, message) -> None:
        raise suppress_context(
            InvalidCommandFormat(
                f"Failed to dispatch expression `{self.re_match.group()}`, {message}"
            )
        )
