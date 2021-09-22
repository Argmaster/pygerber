# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import ABCMeta
from inspect import isclass

from typing import TYPE_CHECKING, Dict, Tuple, Type

if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState

import re

from pygerber.validators.validator import Validator


class DispatcherMeta(ABCMeta):

    validators: Dict[str, Validator] = {}

    def __new__(cls, name, bases, attributes):
        attributes["__validators__"] = cls.get_inherited_validators(bases)
        attributes["__validators__"].extend(cls.get_validators(attributes))
        return ABCMeta.__new__(cls, name, bases, attributes)

    def get_inherited_validators(bases: Tuple[Type[Dispatcher]]) -> dict:
        inherited_fields = []
        for base in bases:
            if issubclass(base, Dispatcher):
                inherited_fields.extend(getvalidators(base))
        return inherited_fields

    def get_validators(attributes: dict) -> dict:
        fields = []
        for name, field in attributes.items():
            if isinstance(field, Validator):
                fields.append((name, field))
        return fields


class Dispatcher(metaclass=DispatcherMeta):

    __validators__: Dict[str, Validator]

    def __init__(self, match_object: re.Match, drawing_state: DrawingState) -> None:
        self.re_match = match_object
        group_dict = self.re_match.groupdict()
        for name, validator in self.__validators__:
            cleaned_value = validator(self, drawing_state, group_dict.get(name))
            setattr(self, name, cleaned_value)


def getvalidators(mesh_factory: Dispatcher) -> dict:
    """Returns validators specified for given Dispatcher.

    :param mesh_factory: Object to fetch validators from.
    :type mesh_factory: Dispatcher
    :return: dictionary of factory fields.
    :rtype: dict
    """
    if isclass(mesh_factory):
        return mesh_factory.__dict__["__validators__"]
    else:
        return mesh_factory.__class__.__dict__["__validators__"]
