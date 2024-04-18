"""Attribute dictionaries for Gerber X3 parser."""

from __future__ import annotations

import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.parser2.errors2 import (
    MissingGuidFieldError,
)

if TYPE_CHECKING:
    from typing_extensions import Self


class AttributesDictionary(ImmutableMapping[str, Optional[str]]):
    """Base class for container holding attributes."""

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}({self.mapping})"


class StandardAttributeBase(FrozenGeneralModel):
    """Class for wrapping standard attribute content."""

    @classmethod
    def parse(cls, content: str) -> Self:
        """Parse attribute content."""
        raise NotImplementedError


class PartAttribute(StandardAttributeBase):
    """The value of the .Part file attribute identifies which part is described. The
    attribute - if present - must be defined in the header.
    """

    class Part(Enum):
        """Enumerate supported part types."""

        Single = "Single"
        Array = "Array"
        FabricationPanel = "FabricationPanel"
        Coupon = "Coupon"
        Other = "Other"

    part: PartAttribute.Part
    field: str = Field(default="")

    @classmethod
    def parse(cls, content: str) -> Self:
        """Return original content."""
        parts = dict(enumerate(content.split(",", 1)))
        return cls(
            part=cls.Part(parts[0]),
            field=parts.get(1, ""),
        )


class GenerationSoftwareAttribute(StandardAttributeBase):
    """Usually a Gerber file is part of a PCB project with a sequence of revisions.
    The purpose of the .ProjectId file attribute is to uniquely identify project and
    revision.This is especially important to check whether all files belong to the same
    revision. By its nature, these values can only be defined by the creator of the
    project and revision. The attribute - if present - must be defined in the header.

    The syntax is as follows:

    ```
    %TF.ProjectId,<Name>,<GUID>,<Revision>*%
    ```
    """

    name: str
    guid: str
    revision: str

    @classmethod
    def parse(cls, content: str) -> Self:
        """Return original content."""
        items = dict(enumerate(content.split(",")))

        if (name := items.get(0)) is None:
            msg = "Missing name field for .GenerationSoftware attribute."
            raise MissingGuidFieldError(msg)

        if (guid := items.get(1)) is None:
            msg = "Missing guid field for .GenerationSoftware attribute."
            raise MissingGuidFieldError(msg)

        if (revision := items.get(2)) is None:
            msg = "Missing revision field for .GenerationSoftware attribute."
            raise MissingGuidFieldError(msg)

        return cls(
            name=name,
            guid=guid,
            revision=revision,
        )


class FileAttributes(AttributesDictionary):
    """File attributes."""

    @property
    def Part(self) -> Optional[str]:  # noqa: N802
        """Identifies the part the file represents, e.g. a single PCB.

        Standard file attribute.
        """
        return self.get(".Part")

    @property
    def FileFunction(self) -> Optional[str]:  # noqa: N802
        """Identifies the file's function in the PCB, e.g. top copper layer.

        Standard file attribute.
        """
        return self.get(".FileFunction")

    @property
    def FilePolarity(self) -> Optional[str]:  # noqa: N802
        """Positive or Negative. This defines whether the image represents the presence
        or absence of material.

        Standard file attribute.
        """
        return self.get(".FilePolarity")

    @property
    def SameCoordinates(self) -> Optional[str]:  # noqa: N802
        """All files in a fabrication data set with this attribute use the same
        coordinates. In other words, they align.

        Standard file attribute.
        """
        return self.get(".SameCoordinates")

    @property
    def CreationDate(self) -> Optional[datetime.datetime]:  # noqa: N802
        """Defines the creation date and time of the file.

        Standard file attribute.
        """
        if (val := self.get(".CreationDate")) is not None:
            return datetime.datetime.fromisoformat(val)
        return None

    @property
    def GenerationSoftware(self) -> Optional[GenerationSoftwareAttribute]:  # noqa: N802
        """Identifies the software creating the file.

        Standard file attribute.
        """
        if (val := self.get(".GenerationSoftware")) is not None:
            return GenerationSoftwareAttribute.parse(val)
        return None

    @property
    def ProjectId(self) -> Optional[str]:  # noqa: N802
        """Defines project and revisions.

        Standard file attribute.
        """
        return self.get(".ProjectId")

    @property
    def MD5(self) -> Optional[str]:  # noqa: N802
        """Sets the MD5 file signature or checksum.

        Standard file attribute.
        """
        return self.get(".MD5")


class AperFunctionAttribute(StandardAttributeBase):
    """Function of objects created with the apertures, e.g. SMD pad."""

    class Function(Enum):
        """Type of drilling."""

        ViaDrill = "ViaDrill"
        BackDrill = "BackDrill"
        ComponentDrill = "ComponentDrill"
        MechanicalDrill = "MechanicalDrill"
        CastellatedDrill = "CastellatedDrill"
        OtherDrill = "OtherDrill"
        ComponentPad = "ComponentPad"
        SMDPad = "SMDPad"
        BGAPad = "BGAPad"
        ConnectorPad = "ConnectorPad"
        HeatsinkPad = "HeatsinkPad"
        ViaPad = "ViaPad"
        TestPad = "TestPad"
        CastellatedPad = "CastellatedPad"
        FiducialPad = "FiducialPad"
        ThermalReliefPad = "ThermalReliefPad"
        WasherPad = "WasherPad"
        AntiPad = "AntiPad"
        OtherPad = "OtherPad"
        Conductor = "Conductor"
        EtchedComponent = "EtchedComponent"
        NonConductor = "NonConductor"
        CopperBalancing = "CopperBalancing"
        Border = "Border"
        OtherCopper = "OtherCopper"
        ComponentMain = "ComponentMain"
        ComponentOutline = "ComponentOutline"
        ComponentPin = "ComponentPin"
        Profile = "Profile"
        Material = "Material"
        NonMaterial = "NonMaterial"
        Other = "Other"

    function: Optional[AperFunctionAttribute.Function]
    field: str = Field(default="")

    @classmethod
    def parse(cls, content: str) -> Self:
        """Return original content."""
        parts = dict(enumerate(content.split(",", 1)))
        return cls(
            function=cls.Function(parts[0]),
            field=parts.get(1, ""),
        )


class ApertureAttributes(AttributesDictionary):
    """Aperture attributes."""

    @property
    def AperFunction(self) -> Optional[AperFunctionAttribute]:  # noqa: N802
        """Function of objects created with the apertures, e.g. SMD pad."""
        if (val := self.get(".AperFunction")) is not None:
            return AperFunctionAttribute.parse(val)
        return None

    @property
    def DrillTolerance(self) -> Optional[str]:  # noqa: N802
        """Tolerance of drill holes."""
        return self.get(".DrillTolerance")

    @property
    def FlashText(self) -> Optional[str]:  # noqa: N802
        """Provides the source text and font for flashes representing text."""
        return self.get(".FlashText")


class PAttribute(StandardAttributeBase):
    """The .P object attribute attaches the reference descriptor and pin number of a
    component pin to a pad on an outer copper layer or a ComponentPin in a component
    layer.

    The syntax is:
    ```
    <.P Attribute> = .P,<refdes>,<number>[,<function>]
    ```
    """

    refdes: str
    number: str
    function: Optional[str]

    @classmethod
    def parse(cls, content: str) -> Self:
        """Return original content."""
        parts = dict(enumerate(content.split(",")))
        return cls(refdes=parts[0], number=parts[1], function=parts.get(2))


class ObjectAttributes(AttributesDictionary):
    """Object attributes."""

    @property
    def N(self) -> Optional[str]:  # noqa: N802
        """The CAD net name of a conducting object, e.g. Clk13."""
        return self.get(".N")

    @property
    def P(self) -> Optional[PAttribute]:  # noqa: N802
        """The pin number (or name) and reference descriptor of a component pad on an
        outer layer, e.g. IC3,7.
        """
        if (val := self.get(".P")) is not None:
            return PAttribute.parse(val)
        return None

    @property
    def C(self) -> Optional[str]:  # noqa: N802
        """The component reference designator linked to an object, e.g. C2."""
        return self.get(".C")
