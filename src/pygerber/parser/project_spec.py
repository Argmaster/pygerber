# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Any, Dict, Optional

import toml
import yaml


class ProjectSpecBase(ABC):
    def __init__(self, init_spec: Dict) -> None:
        self._load_init_spec(init_spec)

    def _load_init_spec(self, init_spec: Dict) -> None:
        for name in self.__class__.__annotations__:
            default = getattr(self.__class__, name, None)
            value = init_spec.get(name, default)
            setattr(self, name, value)
        self.__load_layers_as_LayerSpec()

    def __load_layers_as_LayerSpec(self):
        if not self.layers:
            raise ValueError("You have to provide at least one layer.")
        layers = []
        for layer_data in self.layers:
            layers.append(self.LayerSpecClass.load(layer_data))
        self.layers = layers

    @property
    @abstractmethod
    def LayerSpecClass(self) -> LayerSpecBase:
        ...

    @abstractmethod
    def render(self) -> Optional[Any]:
        ...

    @classmethod
    def from_yaml(cls, file_path: str) -> ProjectSpecBase:
        with open(file_path, "rb") as file:
            spec = yaml.safe_load(file)
        return cls(spec)

    @classmethod
    def from_json(cls, file_path: str) -> ProjectSpecBase:
        with open(file_path, "r", encoding="utf-8") as file:
            spec = json.load(file)
        return cls(spec)

    @classmethod
    def from_toml(cls, file_path: str) -> ProjectSpecBase:
        with open(file_path, "r", encoding="utf-8") as file:
            spec = toml.load(file)
        return cls(spec)


class LayerSpecBase(ABC):
    @abstractstaticmethod
    def load(contents: Dict) -> LayerSpecBase:
        ...

    @staticmethod
    def _get_checked_file_path(contents: dict) -> str:
        file_path = contents.get("file_path")
        os.path.exists(file_path)
        return file_path

    @staticmethod
    def _replace_none_color_with_named_color_based_on_file_name(
        colors_set, file_path, named_colors
    ):
        if colors_set is None:
            file_name = os.path.basename(file_path)
            for name, named_color_set in named_colors.items():
                if name in file_name:
                    colors_set = named_color_set
                    break
        return colors_set
