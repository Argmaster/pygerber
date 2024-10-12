"""The `_gerber_job_file` module contains definition of `GerberJobFile` class."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from pygerber.gerber.api._composite_view import CompositeView
from pygerber.gerber.api._enums import FileTypeEnum
from pygerber.gerber.api._errors import PathToGerberJobProjectNotDefinedError
from pygerber.gerber.api._gerber_file import GerberFile
from pygerber.gerber.api._project import Project


class _ModelType(BaseModel):
    """Model Type."""

    config: ClassVar[ConfigDict] = ConfigDict(extra="allow")


class GenerationSoftware(_ModelType):
    """Generation Software."""

    vendor: str = Field(alias="Vendor")
    application: str = Field(alias="Application")
    version: str = Field(alias="Version")


class Header(_ModelType):
    """Header."""

    creation_date: str = Field(alias="CreationDate")
    generation_software: GenerationSoftware = Field(alias="GenerationSoftware")


class ProjectId(_ModelType):
    """Project ID."""

    name: str = Field(alias="Name")
    guid: str = Field(alias="GUID")
    revision: str = Field(alias="Revision")


class Size(_ModelType):
    """Size."""

    x: float = Field(alias="X")
    y: float = Field(alias="Y")


class GeneralSpecs(_ModelType):
    """General Specs."""

    project_id: ProjectId = Field(alias="ProjectId")
    size: Size = Field(alias="Size")
    layer_number: int = Field(alias="LayerNumber")
    board_thickness: float = Field(alias="BoardThickness")
    finish: Optional[str] = Field(alias="Finish", default=None)


class DesignRules(_ModelType):
    """Design Rules."""

    layers: str = Field(alias="Layers")
    pad_to_pad: float = Field(alias="PadToPad")
    pad_to_track: float = Field(alias="PadToTrack")
    track_to_track: float = Field(alias="TrackToTrack")
    track_to_region: float = Field(alias="TrackToRegion")
    region_to_region: float = Field(alias="RegionToRegion")


class FilesAttributes(_ModelType):
    """Files Attributes."""

    path: str = Field(alias="Path")
    file_function: str = Field(alias="FileFunction")
    file_polarity: str = Field(alias="FilePolarity")


class MaterialStackup(_ModelType):
    """Material Stackup."""

    name: str = Field(alias="Name")
    type: str = Field(alias="Type")
    thickness: Optional[float] = Field(alias="Thickness", default=None)
    material: Optional[str] = Field(alias="Material", default=None)
    notes: Optional[str] = Field(alias="Notes", default=None)


class GerberJobFile(_ModelType):
    """Gerber Job File."""

    header: Header = Field(alias="Header")
    general_specs: GeneralSpecs = Field(alias="GeneralSpecs")
    files_attributes: List[FilesAttributes] = Field(alias="FilesAttributes")
    material_stackup: List[MaterialStackup] = Field(alias="MaterialStackup")

    __file_path__: Optional[Path] = None

    def model_post_init(self, __context: Any) -> None:
        self.__file_path__ = Path(__context["__file_path__"])
        return super().model_post_init(__context)

    @classmethod
    def from_file(cls, path: str | Path) -> GerberJobFile:
        """Load Gerber Job File.

        Parameters
        ----------
        path : str | Path
            Path to a `.gbrjob` file.

        Returns
        -------
        GerberJobFile
            Object representing Gerber Job File.

        """
        path = Path(path)
        return cls.model_validate_json(
            path.read_text("utf-8"), context={"__file_path__": path}
        )

    def to_project(self, *, path: Optional[Path] = None) -> Project:  # noqa: C901
        """Convert Gerber Job File to PyGerber Project object.

        Parameters
        ----------
        path : Optional[Path], optional
            If GerberJobFile was not loaded from file on disk, you must provide a path
            to where that file should be, including file name, by default None

        Returns
        -------
        Project
            New project object containing Gerber files from Gerber Job File.

        """
        root_path = self.__file_path__ or path

        if root_path is None:
            raise PathToGerberJobProjectNotDefinedError(self)

        root_path = root_path.parent

        top: dict[FileTypeEnum, GerberFile] = {}
        bottom: dict[FileTypeEnum, GerberFile] = {}
        inner: dict[str, dict[FileTypeEnum, GerberFile]] = {}

        all_layers: list[GerberFile] = []

        layer_identifier_regex = re.compile(r"L([0-9]+)")

        for file in self.files_attributes:
            split_file_function = file.file_function.upper().split(",")
            # First part should always be a valid FileFunction value
            file_function, *_ = split_file_function
            file_type = FileTypeEnum(file_function)
            gerber_file = GerberFile.from_file(
                file_path=root_path / file.path,
                file_type=file_type,
            )

            if file_type == FileTypeEnum.PROFILE:
                all_layers.append(gerber_file)
                continue

            if "TOP" in split_file_function:
                top[file_type] = gerber_file
                continue

            if "BOT" in split_file_function:
                bottom[file_type] = gerber_file
                continue

            for part in split_file_function:
                match = layer_identifier_regex.match(part)
                if match is not None:
                    layer = match.group(1)
                    inner_layer = inner.get(layer, {})

                    inner_layer[file_type] = gerber_file

                    inner[layer] = inner_layer
                    break
            else:
                logging.warning("Could not determine layer for file %s", file.path)

        for file in all_layers:
            top[file.file_type] = file
            bottom[file.file_type] = file

            for inner_layer in inner.values():
                inner_layer[file.file_type] = file

        def extract_and_sort_files(
            file_map: dict[FileTypeEnum, GerberFile],
        ) -> list[GerberFile]:
            ordered_files: list[GerberFile] = []

            if (file := file_map.get(FileTypeEnum.COPPER)) is not None:
                ordered_files.append(file)

            if (file := file_map.get(FileTypeEnum.MASK)) is not None:
                ordered_files.append(file)

            if (file := file_map.get(FileTypeEnum.SOLDERMASK)) is not None:
                ordered_files.append(file)

            if (file := file_map.get(FileTypeEnum.PASTE)) is not None:
                ordered_files.append(file)

            if (file := file_map.get(FileTypeEnum.SILK)) is not None:
                ordered_files.append(file)

            if (file := file_map.get(FileTypeEnum.LEGEND)) is not None:
                ordered_files.append(file)

            if (file := file_map.get(FileTypeEnum.PROFILE)) is not None:
                ordered_files.append(file)

            return ordered_files

        return Project(
            top=CompositeView(extract_and_sort_files(top)),
            inner=(
                CompositeView(extract_and_sort_files(inner[key]))
                for key in sorted(inner)
            ),
            bottom=CompositeView(extract_and_sort_files(bottom)),
        )
