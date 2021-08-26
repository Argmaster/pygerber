# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from pygerber.meta import Meta
from pygerber.parser.pillow.apertures import *
from typing import Generator, Tuple

from PIL import Image, ImageDraw
from pygerber.meta.apertureset import ApertureSet
from pygerber.tokenizer import Tokenizer


@dataclass
class ColorSet:

    Color = Tuple[float, float, float, float]

    dark: Color
    clear: Color
    region: Color


DEFAULT_COLOR_SET = ColorSet((66, 166, 66, 255), (16, 66, 36, 255), (66, 166, 66, 255))


class ParserWithPillow:

    tokenizer: Tokenizer
    apertureSet = ApertureSet(
        PillowCircle,
        PillowRectangle,
        PillowObround,
        PillowPolygon,
        PillowCustom,
        PillowRegion,
    )
    is_rendered: bool

    def __init__(
        self,
        filepath: str = None,
        string_source: str = None,
        *,
        dpi: int = 600,
        colors: ColorSet = DEFAULT_COLOR_SET,
        ignore_deprecated: bool = True,
    ) -> None:
        """
        If filepath is None, string_source will be used as source,
        otherwise filepath will be used to read and parse file, then
        string_source will be complitely ignored. Passing None to both
        will result in RuntimeError.
        """
        self.is_rendered = False
        self.tokenizer = Tokenizer(
            self.apertureSet,
            ignore_deprecated=ignore_deprecated,
        )
        self.colors = colors
        self.dpmm = dpi / 25.4
        self._tokenize(filepath, string_source)

    def _tokenize(self, filepath: str, string_source: str) -> None:
        if filepath is not None:
            self.tokenizer.tokenize_file(filepath)
        elif string_source is not None:
            self.tokenizer.tokenize_string(string_source)
        else:
            raise RuntimeError("filepath and source_string can't be both None.")

    @property
    def canvas(self) -> Image.Image:
        return self.tokenizer.meta.canvas

    def render(self) -> None:
        self._preprare_meta()
        if not self.is_rendered:
            self.tokenizer.render()
            self.is_rendered = True
        else:
            raise RuntimeError("Attempt to render already rendered canvas.")

    def _preprare_meta(self) -> None:
        self._prepare_canvas()
        self.tokenizer.meta.colors = self.colors
        self.tokenizer.meta.dpmm = self.dpmm

    def _prepare_canvas(self) -> None:
        bbox = self.tokenizer.get_bbox()
        width = self._prepare_co(bbox.width())
        height = self._prepare_co(bbox.height())
        self.tokenizer.meta.canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        self.tokenizer.meta.draw_canvas = ImageDraw.Draw(self.canvas)
        self.tokenizer.meta.left_offset = self._prepare_co(-bbox.left)
        self.tokenizer.meta.bottom_offset = self._prepare_co(-bbox.lower)

    def _prepare_co(self, value: float) -> float:
        return int(value * self.dpmm)

    def get_image(self) -> Image.Image:
        if self.is_rendered:
            return self.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            raise RuntimeError("Can't return canvas that was not rendered.")

    def save(self, filepath: str, format: str) -> None:
        self.canvas.save(filepath, format)
