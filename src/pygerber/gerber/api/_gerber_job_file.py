"""The `_gerber_job_file` module contains definition of `GerberJobFile` class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class _ModelType(BaseModel):
    """Model Type."""

    config: ClassVar[ConfigDict] = ConfigDict(
        extra="allow",
    )


class GenerationSoftware(_ModelType):
    """Generation Software."""

    vendor: str = Field(alias="Vendor")
    application: str = Field(alias="Application")
    version: str = Field(alias="Version")


class Header(_ModelType):
    """Header."""

    creation_date: str = Field(alias="CreationDate")


class ProjectId(_ModelType):
    """Project ID."""

    project_id: str = Field(alias="ProjectId")


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

    def model_post_init(self, __context: Any) -> None:
        self.file_path = Path(__context["__file_path__"])
        return super().model_post_init(__context)

    @classmethod
    def load_gerber_job(cls, path: str | Path) -> GerberJobFile:
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
