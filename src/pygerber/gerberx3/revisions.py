"""Gerber format metadata."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pygerber.common.frozen_general_model import FrozenGeneralModel


class Gerber(Enum):
    """Gerber specification major versions."""

    X1 = 0x01FF
    X2 = 0x02FF
    X3 = 0x03FF


class RevisionData(FrozenGeneralModel):
    """Container for Gerber format revision metadata."""

    name: str
    spec: Gerber


class Revision(Enum):
    """List of known Gerber format revisions."""

    Revision_Legacy = RevisionData(name="Revision Legacy", spec=Gerber.X1)
    # Gerber X2
    Revision_2012_12 = RevisionData(name="Revision I1 (2012 12)", spec=Gerber.X2)
    Revision_2013_04 = RevisionData(name="Revision I2 (2013 04)", spec=Gerber.X2)
    Revision_2013_06 = RevisionData(name="Revision I3 (2013 06)", spec=Gerber.X2)
    Revision_2013_10 = RevisionData(name="Revision I4 (2013 10)", spec=Gerber.X2)
    Revision_2014_02 = RevisionData(name="Revision J1 (2014 02) - X2", spec=Gerber.X2)
    Revision_2014_07 = RevisionData(name="Revision J2 (2014 07)", spec=Gerber.X2)
    Revision_2014_10 = RevisionData(name="Revision J3 (2014 10)", spec=Gerber.X2)
    Revision_2015_02 = RevisionData(name="Revision J4 (2015 02)", spec=Gerber.X2)
    Revision_2015_06 = RevisionData(name="Revision 2015.06", spec=Gerber.X2)
    Revision_2015_07 = RevisionData(name="Revision 2015.07", spec=Gerber.X2)
    Revision_2015_10 = RevisionData(name="Revision 2015.10", spec=Gerber.X2)
    Revision_2016_01 = RevisionData(name="Revision 2016.01", spec=Gerber.X2)
    Revision_2016_04 = RevisionData(name="Revision 2016.04", spec=Gerber.X2)
    Revision_2016_06 = RevisionData(name="Revision 2016.06", spec=Gerber.X2)
    Revision_2016_09 = RevisionData(name="Revision 2016.09", spec=Gerber.X2)
    Revision_2016_11 = RevisionData(name="Revision 2016.11", spec=Gerber.X2)
    Revision_2016_12 = RevisionData(
        name="Revision 2016.12 - Nested step and repeat",
        spec=Gerber.X2,
    )
    Revision_2017_03 = RevisionData(name="Revision 2017.03", spec=Gerber.X2)
    Revision_2017_05 = RevisionData(name="Revision 2017.05", spec=Gerber.X2)
    Revision_2017_11 = RevisionData(name="Revision 2017.11", spec=Gerber.X2)
    Revision_2018_05 = RevisionData(name="Revision 2018.05", spec=Gerber.X2)
    Revision_2018_06 = RevisionData(name="Revision 2018.06", spec=Gerber.X2)
    Revision_2018_09 = RevisionData(name="Revision 2018.09", spec=Gerber.X2)
    Revision_2018_11 = RevisionData(name="Revision 2018.11", spec=Gerber.X2)
    Revision_2019_06 = RevisionData(name="Revision 2019.06", spec=Gerber.X2)
    Revision_2019_09 = RevisionData(name="Revision 2019.09", spec=Gerber.X2)
    # Gerber X3
    Revision_2020_09 = RevisionData(name="Revision 2020.09", spec=Gerber.X3)
    Revision_2021_02 = RevisionData(name="Revision 2021.02", spec=Gerber.X3)
    Revision_2021_04 = RevisionData(name="Revision 2021.04", spec=Gerber.X3)
    Revision_2021_11 = RevisionData(name="Revision 2021.11", spec=Gerber.X3)
    Revision_2022_02 = RevisionData(name="Revision 2022.02", spec=Gerber.X3)
    Revision_2023_03 = RevisionData(name="Revision 2023.03", spec=Gerber.X3)
    Revision_2023_08 = RevisionData(name="Revision 2023.08", spec=Gerber.X3)


@dataclass
class SpecSec:
    """Gerber specification section."""

    sec_id: str
    name: str
    page: int


REVISION_2023_08_SOURCE_URL: str = "https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2023-08_en.pdf"


class Revision202308(Enum):
    """Enumeration of all known sections in Gerber specification, revision 2023.08."""

    Contents = SpecSec("", "Contents", 2)
    Preface = SpecSec("", "Preface", 7)
    S_1 = SpecSec("1", "Introduction", 8)
    S_1_1 = SpecSec("1.1", "Scope and Target Audience", 8)
    S_1_2 = SpecSec("1.2", "Further Resources", 8)
    S_1_3 = SpecSec("1.3", "Reference Gerber Viewer", 8)
    S_1_4 = SpecSec("1.4", "Copyright and Intellectual Property", 9)
    S_2 = SpecSec("2", "Overview", 10)
    S_2_1 = SpecSec("2.1", "File Structure", 10)
    S_2_2 = SpecSec("2.2", "Apertures", 10)
    S_2_3 = SpecSec("2.3", "Graphical objects", 11)
    S_2_4 = SpecSec("2.4", "Draws and Arcs", 12)
    S_2_5 = SpecSec("2.5", "Operations (D01, D02, D03)", 13)
    S_2_6 = SpecSec("2.6", "Graphics State", 16)
    S_2_7 = SpecSec("2.7", "Polarity", 13)
    S_2_8 = SpecSec("2.8", "Blocks", 14)
    S_2_9 = SpecSec("2.9", "Attributes", 14)
    S_2_10 = SpecSec("2.10", "Commands Overview", 18)
    S_2_11 = SpecSec("2.11", "Processing a Gerber File", 19)
    S_2_12 = SpecSec("2.12", "Glossary", 21)
    S_2_13 = SpecSec("2.13", "Annotated Example Files", 24)
    S_2_13_1 = SpecSec("", "Example: Two Square Boxes", 24)
    S_2_13_2 = SpecSec("", "Example: Polarities and Apertures", 26)
    S_2_14 = SpecSec("2.14", "Conformance", 30)
    S_3 = SpecSec("3", "Syntax", 31)
    S_3_1 = SpecSec("3.1", "Character Set", 31)
    S_3_2 = SpecSec("3.2", "Grammar Syntax", 31)
    S_3_3 = SpecSec("3.3", "Commands", 33)
    S_3_4 = SpecSec("3.4", "Data Types", 35)
    S_3_4_1 = SpecSec("", "Integers", 35)
    S_3_4_2 = SpecSec("", "Decimals", 35)
    S_3_4_3 = SpecSec("", "Strings", 35)
    S_3_4_4 = SpecSec("", "Fields", 36)
    S_3_4_5 = SpecSec("", "Names", 36)
    S_3_5 = SpecSec("3.5", "Grammar of the Gerber Layer Format", 37)
    S_3_6 = SpecSec("3.6", "File Extension, MIME Type and UTI", 43)
    S_4 = SpecSec("4", "Graphics", 44)
    S_4_1 = SpecSec("4.1", "Comment (G04)", 44)
    S_4_2 = SpecSec("4.2", "Coordinate Commands", 45)
    S_4_2_1 = SpecSec("", "Unit (MO)", 46)
    S_4_2_2 = SpecSec("", "Format Specification (FS)", 47)
    S_4_3 = SpecSec("4.3", "Aperture Definition (AD)", 48)
    S_4_3_1 = SpecSec("", "AD Command", 48)
    S_4_3_2 = SpecSec("", "Zero-size Apertures", 48)
    S_4_3_3 = SpecSec("", "Examples", 49)
    S_4_4 = SpecSec("4.4", "Standard Aperture Templates", 50)
    S_4_4_1 = SpecSec("", "Overview", 50)
    S_4_4_2 = SpecSec("", "Circle", 50)
    S_4_4_3 = SpecSec("", "Rectangle", 52)
    S_4_4_4 = SpecSec("", "Obround", 53)
    S_4_4_5 = SpecSec("", "Polygon", 54)
    S_4_4_6 = SpecSec("", "Transparency of Holes", 55)
    S_4_5 = SpecSec("4.5", "Aperture Macro (AM)", 56)
    S_4_5_1 = SpecSec("", "Primitives", 58)
    S_4_5_2 = SpecSec("", "Exposure Parameter", 67)
    S_4_5_3 = SpecSec("", "Rotation Parameter", 68)
    S_4_5_4 = SpecSec("", "Macro Variables and Expressions", 70)
    S_4_5_5 = SpecSec("", "Examples", 72)
    S_4_6 = SpecSec("4.6", "Set Current Aperture (Dnn)", 75)
    S_4_7 = SpecSec("4.7", "Plot State Commands (G01,G02,G03,G75)", 76)
    S_4_7_1 = SpecSec("", "Linear Plotting (G01)", 76)
    S_4_7_2 = SpecSec("", "Circular Plotting (G02, G03, G75)", 77)
    S_4_8 = SpecSec("4.8", "Operations (D01/D02/D03)", 81)
    S_4_8_1 = SpecSec("", "Overview", 81)
    S_4_8_2 = SpecSec("", "Plot (D01)", 83)
    S_4_8_3 = SpecSec("", "Move (D02)", 83)
    S_4_8_4 = SpecSec("", "Flash (D03)", 83)
    S_4_8_5 = SpecSec("", "Example", 84)
    S_4_9 = SpecSec("4.9", "Aperture Transformations (LP, LM, LR, LS)", 85)
    S_4_9_1 = SpecSec("", "Overview", 85)
    S_4_9_2 = SpecSec("", "Load Polarity (LP)", 87)
    S_4_9_3 = SpecSec("", "Load Mirroring (LM)", 87)
    S_4_9_4 = SpecSec("", "Load Rotation (LR)", 87)
    S_4_9_5 = SpecSec("", "Load Scaling (LS)", 88)
    S_4_9_6 = SpecSec("", "Example", 88)
    S_4_10 = SpecSec("4.10", "Region Statement (G36/G37)", 90)
    S_4_10_1 = SpecSec("", "Region Overview", 90)
    S_4_10_2 = SpecSec("", "Region Statement Syntax", 90)
    S_4_10_3 = SpecSec("", "Valid Contours", 91)
    S_4_10_4 = SpecSec("", "Examples", 93)
    S_4_10_5 = SpecSec("", "Copper Pours, Power and Ground Planes", 108)
    S_4_11 = SpecSec("4.11", "Block Aperture (AB)", 111)
    S_4_11_1 = SpecSec("", "Overview of block apertures", 111)
    S_4_11_2 = SpecSec("", "AB Statement Syntax", 111)
    S_4_11_3 = SpecSec("", "Usage of Block Apertures", 113)
    S_4_11_4 = SpecSec("", "Example", 114)
    S_4_12 = SpecSec("4.12", "Step and Repeat (SR)", 116)
    S_4_13 = SpecSec("4.13", "End-of-file (M02)", 119)
    S_4_14 = SpecSec("4.14", "Numerical Accuracy", 120)
    S_4_14_1 = SpecSec("", "Visualization", 120)
    S_4_14_2 = SpecSec("", "Image Processing", 120)
    S_5 = SpecSec("5", "Attributes", 122)
    S_5_1 = SpecSec("5.1", "Attributes Overview", 122)
    S_5_2 = SpecSec("5.2", "File Attributes (TF)", 124)
    S_5_3 = SpecSec("5.3", "Aperture Attributes (TA)", 124)
    S_5_3_1 = SpecSec("", "Aperture Attributes on Regions", 125)
    S_5_4 = SpecSec("5.4", "Object Attributes (TO)", 125)
    S_5_5 = SpecSec("5.5", "Delete Attribute (TD)", 126)
    S_5_6 = SpecSec("5.6", "Standard Attributes", 127)
    S_5_6_1 = SpecSec("", "Overview", 127)
    S_5_6_2 = SpecSec("", ".Part", 129)
    S_5_6_3 = SpecSec("", ".FileFunction", 130)
    S_5_6_4 = SpecSec("", ".FilePolarity", 135)
    S_5_6_5 = SpecSec("", ".SameCoordinates", 136)
    S_5_6_6 = SpecSec("", ".CreationDate", 136)
    S_5_6_7 = SpecSec("", ".GenerationSoftware", 137)
    S_5_6_8 = SpecSec("", ".ProjectId", 137)
    S_5_6_9 = SpecSec("", ".MD5", 138)
    S_5_6_10 = SpecSec("", ".AperFunction", 139)
    S_5_6_11 = SpecSec("", ".DrillTolerance", 147)
    S_5_6_12 = SpecSec("", ".FlashText", 147)
    S_5_6_13 = SpecSec("", ".N (Net)", 149)
    S_5_6_14 = SpecSec("", ".P (Pin)", 151)
    S_5_6_15 = SpecSec("", ".C (Component Refdes)", 152)
    S_5_6_16 = SpecSec("", ".Cxxx (Component Characteristics)", 153)
    S_5_7 = SpecSec("5.7", "Text in the Image", 155)
    S_5_8 = SpecSec("5.8", "Examples", 156)
    S_6 = SpecSec("6", "PCB Fabrication and Assembly Data", 158)
    S_6_1 = SpecSec("6.1", "Structure", 158)
    S_6_2 = SpecSec("6.2", "Mandatory Attributes", 158)
    S_6_3 = SpecSec("6.3", "Alignment", 158)
    S_6_4 = SpecSec("6.4", "Pads", 158)
    S_6_5 = SpecSec("6.5", "The Profile", 158)
    S_6_6 = SpecSec("6.6", "Drill/rout files", 159)
    S_6_6_1 = SpecSec("", "Backdrilling", 159)
    S_6_6_2 = SpecSec("", "Example Drill File", 160)
    S_6_7 = SpecSec("6.7", "Drawings and Data", 163)
    S_6_8 = SpecSec("6.8", "The CAD Netlist", 164)
    S_6_8_1 = SpecSec("", "Benefits of Including the CAD Netlist", 164)
    S_6_8_2 = SpecSec("", "IP Considerations", 165)
    S_6_9 = SpecSec("6.9", "PCB Assembly Data", 166)
    S_6_9_1 = SpecSec("", "Overview", 166)
    S_6_9_2 = SpecSec("", "Assembly Data Set", 166)
    S_6_9_3 = SpecSec("", "Annotated Example Component Layer", 167)
    S_7 = SpecSec("7", "Errors and Bad Practices", 169)
    S_7_1 = SpecSec("7.1", "Errors", 169)
    S_7_2 = SpecSec("7.2", "Bad Practices", 171)
    S_8 = SpecSec("8", "Deprecated Format Elements", 173)
    S_8_1 = SpecSec("8.1", "Deprecated Commands", 173)
    S_8_1_1 = SpecSec("", "Overview", 173)
    S_8_1_2 = SpecSec("", "Axis Select (AS)", 175)
    S_8_1_3 = SpecSec("", "Image Name (IN)", 176)
    S_8_1_4 = SpecSec("", "Image Polarity (IP)", 177)
    S_8_1_5 = SpecSec("", "Image Rotation (IR)", 178)
    S_8_1_6 = SpecSec("", "Load Name (LN)", 179)
    S_8_1_7 = SpecSec("", "Mirror Image (MI)", 180)
    S_8_1_8 = SpecSec("", "Offset (OF)", 181)
    S_8_1_9 = SpecSec("", "Scale Factor (SF)", 182)
    S_8_1_10 = SpecSec("", "Single-quadrant arc mode (G74)", 183)
    S_8_2 = SpecSec("8.2", "Deprecated Command Options", 187)
    S_8_2_1 = SpecSec("", "Format Specification (FS) Options", 187)
    S_8_2_2 = SpecSec("", "Rectangular Hole in Standard Apertures", 188)
    S_8_2_3 = SpecSec("", "Draws and Arcs with Rectangular Apertures", 189)
    S_8_2_4 = SpecSec("", "Macro Primitive Code 2, Vector Line", 190)
    S_8_2_5 = SpecSec("", "Macro Primitive Code 22, Lower Left Line", 190)
    S_8_2_6 = SpecSec("", "Macro Primitive Code 6, Moiré", 191)
    S_8_3 = SpecSec("8.3", "Deprecated Syntax Variations", 192)
    S_8_3_1 = SpecSec("", "Combining G01/G02/G03 and D01 in a single command.", 192)
    S_8_3_2 = SpecSec("", "Coordinate Data without Operation Code", 192)
    S_8_3_3 = SpecSec("", "Style Variations in Command Codes", 192)
    S_8_3_4 = SpecSec("", "Deprecated usage of SR", 192)
    S_8_4 = SpecSec("8.4", "Deprecated Attribute Values", 193)
    S_8_5 = SpecSec("8.5", "Standard Gerber (RS-274-D)", 194)
    S_9 = SpecSec("9", "References", 195)
    S_10 = SpecSec("10", "History", 196)
    S_11 = SpecSec("11", "Revisions", 198)
    S_11_1 = SpecSec("11.1", "Revision 2023.08", 198)
    S_11_2 = SpecSec("11.2", "Revision 2023.03", 198)
    S_11_3 = SpecSec("11.3", "Revision 2022.02", 198)
    S_11_4 = SpecSec("11.4", "Revision 2021.11", 198)
    S_11_5 = SpecSec("11.5", "Revision 2021.04", 198)
    S_11_6 = SpecSec("11.6", "Revision 2021.02 - Formal grammar", 199)
    S_11_7 = SpecSec("11.7", "Revision 2020.09 - X3", 199)
    S_11_8 = SpecSec("11.8", "Revision 2019.09", 199)
    S_11_9 = SpecSec("11.9", "Revision 2019.06", 199)
    S_11_10 = SpecSec("11.10", "Revision 2018.11", 200)
    S_11_11 = SpecSec("11.11", "Revision 2018.09", 200)
    S_11_12 = SpecSec("11.12", "Revision 2018.06", 200)
    S_11_13 = SpecSec("11.13", "Revision 2018.05", 200)
    S_11_14 = SpecSec("11.14", "Revision 2017.11", 200)
    S_11_15 = SpecSec("11.15", "Revision 2017.05", 201)
    S_11_16 = SpecSec("11.16", "Revision 2017.03", 201)
    S_11_17 = SpecSec("11.17", "Revision 2016.12 - Nested step and repeat", 201)
    S_11_18 = SpecSec("11.18", "Revision 2016.11", 201)
    S_11_19 = SpecSec("11.19", "Revision 2016.09", 202)
    S_11_20 = SpecSec("11.20", "Revision 2016.06", 202)
    S_11_21 = SpecSec("11.21", "Revision 2016.04", 202)
    S_11_22 = SpecSec("11.22", "Revision 2016.01", 202)
    S_11_23 = SpecSec("11.23", "Revision 2015.10", 203)
    S_11_24 = SpecSec("11.24", "Revision 2015.07", 203)
    S_11_25 = SpecSec("11.25", "Revision 2015.06", 203)
    S_11_26 = SpecSec("11.26", "Revision J3 (2014 10)", 203)
    S_11_27 = SpecSec("11.27", "Revision J4 (2015 02)", 203)
    S_11_28 = SpecSec("11.28", "Revision J2 (2014 07)", 203)
    S_11_29 = SpecSec("11.29", "Revision J1 (2014 02) - X2", 204)
    S_11_30 = SpecSec("11.30", "Revision I4 (2013 10)", 204)
    S_11_31 = SpecSec("11.31", "Revision I3 (2013 06)", 204)
    S_11_32 = SpecSec("11.32", "Revision I2 (2013 04)", 204)
    S_11_33 = SpecSec("11.33", "Revision I1 (2012 12)", 204)

    def get_url(self) -> str:
        """Get url to this section."""
        return f"{REVISION_2023_08_SOURCE_URL}page={self.value.page}"

    def get_sec_id(self) -> str:
        """Get section id."""
        return self.value.sec_id or self.value.name
