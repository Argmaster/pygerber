"""The `rev_2024_05` module contains selected fragments from The Gerber Layer Format
Specification - Revision 2024.05 used to provide information about gerber standard
in messages shown to users of PyGerber.
"""

from __future__ import annotations

from dataclasses import dataclass

from pygerber.common.namespace import Namespace


def spec_url() -> str:
    """Get the URL of the Gerber specification."""
    return "https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf"


def spec_title() -> str:
    """Get the title of the Gerber specification."""
    return "### The Gerber Layer Format Specification - Revision 2024.05"


@dataclass
class Page:
    """The `Page` class represents a page in the Gerber specification."""

    section: tuple[int, ...]
    page_number: int
    title: str

    @property
    def url(self) -> str:
        """Get the URL of the page."""
        return spec_url() + f"#page={self.page_number}"

    @property
    def pretty_title(self) -> str:
        """Get the pretty title of the page."""
        section_number = ".".join(map(str, self.section))
        return f"{section_number}. {self.title}"

    @property
    def markdown(self) -> str:
        """Get the markdown of the page."""
        return f"#### [{self.pretty_title}]({self.url})"


class Sections(Namespace):
    """The `Sections` class contains map of sections of Gerber specification."""

    s_1 = Page((1,), 9, "Introduction")
    s_1_1 = Page((1, 1), 9, "Scope and Target Audience")
    s_1_2 = Page((1, 2), 9, "Further Resources")
    s_1_3 = Page((1, 3), 9, "Reference Gerber Viewer")
    s_1_4 = Page((1, 4), 9, "Copyright and Intellectual Property")
    s_2 = Page((2,), 11, "Overview")
    s_2_1 = Page((2, 1), 11, "File Structure")
    s_2_2 = Page((2, 2), 11, "Apertures")
    s_2_3 = Page((2, 3), 12, "Graphical objects")
    s_2_3_1 = Page((2, 3, 1), 13, "Draws and Arcs")
    s_2_3_2 = Page((2, 3, 2), 14, "Polarity")
    s_2_4 = Page((2, 4), 15, "Blocks")
    s_2_5 = Page((2, 5), 15, "Attributes")
    s_2_6 = Page((2, 6), 16, "Operations (D01, D02, D03)")
    s_2_7 = Page((2, 7), 17, "Graphics State")
    s_2_8 = Page((2, 8), 19, "Commands Overview")
    s_2_9 = Page((2, 9), 20, "Processing a Gerber File")
    s_2_10 = Page((2, 10), 22, "Glossary")
    s_2_11 = Page((2, 11), 25, "Annotated Example Files")
    s_2_11_1 = Page((2, 11, 1), 25, "Example: Two Square Boxes")
    s_2_11_2 = Page((2, 11, 2), 27, "Example: Polarities and Apertures")
    s_2_12 = Page((2, 12), 31, "Conformance")
    s_3 = Page((3,), 32, "Syntax")
    s_3_1 = Page((3, 1), 32, "Character Set")
    s_3_2 = Page((3, 2), 32, "Formal Grammar")
    s_3_3 = Page((3, 3), 34, "Commands")
    s_3_4 = Page((3, 4), 36, "Data Types")
    s_3_4_1 = Page((3, 4, 1), 36, "Integers")
    s_3_4_2 = Page((3, 4, 2), 36, "Decimals")
    s_3_4_3 = Page((3, 4, 3), 36, "Strings")
    s_3_4_4 = Page((3, 4, 4), 37, "Fields")
    s_3_4_5 = Page((3, 4, 5), 37, "Names")
    s_3_5 = Page((3, 5), 38, "Grammar of the Gerber Layer Format")
    s_3_6 = Page((3, 6), 44, "File Extension, MIME Type and UTI")
    s_4 = Page((4,), 45, "Graphics")
    s_4_1 = Page((4, 1), 45, "Comment (G04)")
    s_4_2 = Page((4, 2), 46, "Coordinate Commands")
    s_4_2_1 = Page((4, 2, 1), 47, "Unit (MO)")
    s_4_2_2 = Page((4, 2, 2), 48, "Format Specification (FS)")
    s_4_3 = Page((4, 3), 49, "Aperture Definition (AD)")
    s_4_3_1 = Page((4, 3, 1), 49, "AD Command")
    s_4_3_2 = Page((4, 3, 2), 50, "Examples")
    s_4_3_3 = Page((4, 3, 3), 50, "Zero-size Apertures")
    s_4_4 = Page((4, 4), 51, "Standard Aperture Templates")
    s_4_4_1 = Page((4, 4, 1), 51, "Overview")
    s_4_4_2 = Page((4, 4, 2), 51, "Circle")
    s_4_4_3 = Page((4, 4, 3), 53, "Rectangle")
    s_4_4_4 = Page((4, 4, 4), 54, "Obround")
    s_4_4_5 = Page((4, 4, 5), 55, "Polygon")
    s_4_4_6 = Page((4, 4, 6), 56, "Transparency of Holes")
    s_4_5 = Page((4, 5), 57, "Aperture Macro (AM)")
    s_4_5_1 = Page((4, 5, 1), 59, "Primitives")
    s_4_5_1_1 = Page((4, 5, 1, 2), 59, "Overview")
    s_4_5_1_2 = Page((4, 5, 1, 2), 60, "Comment, Code 0")
    s_4_5_1_3 = Page((4, 5, 1, 3), 61, "Circle, Code 1")
    s_4_5_1_4 = Page((4, 5, 1, 4), 62, "Vector Line, Code 20")
    s_4_5_1_5 = Page((4, 5, 1, 5), 63, "Center Line, Code 21")
    s_4_5_1_6 = Page((4, 5, 1, 6), 64, "Outline, Code 4")
    s_4_5_1_7 = Page((4, 5, 1, 7), 66, "Polygon, Code 5")
    s_4_5_1_8 = Page((4, 5, 1, 8), 67, "Thermal, Code 7")
    s_4_5_2 = Page((4, 5, 2), 68, "Exposure Parameter")
    s_4_5_3 = Page((4, 5, 3), 69, "Rotation Parameter")
    s_4_5_4 = Page((4, 5, 4), 70, "Macro Variables and Expressions")
    s_4_5_5 = Page((4, 5, 5), 72, "Examples")
    s_4_6 = Page((4, 6), 75, "Set Current Aperture (Dnn)")
    s_4_7 = Page((4, 7), 76, "Plot State Commands (G01,G02,G03,G75)")
    s_4_7_1 = Page((4, 7, 1), 76, "Linear Plotting (G01)")
    s_4_7_2 = Page((4, 7, 2), 77, "Circular Plotting (G02, G03, G75)")
    s_4_8 = Page((4, 8), 81, "Operations (D01/D02/D03)")
    s_4_8_1 = Page((4, 8, 1), 81, "Overview")
    s_4_8_2 = Page((4, 8, 2), 83, "Plot (D01)")
    s_4_8_3 = Page((4, 8, 3), 83, "Move (D02)")
    s_4_8_4 = Page((4, 8, 4), 83, "Flash (D03)")
    s_4_8_5 = Page((4, 8, 5), 84, "Example")
    s_4_9 = Page((4, 9), 85, "Aperture Transformations (LP, LM, LR, LS)")
    s_4_9_1 = Page((4, 9, 1), 85, "Overview")
    s_4_9_2 = Page((4, 9, 2), 87, "Load Polarity (LP)")
    s_4_9_3 = Page((4, 9, 3), 87, "Load Mirroring (LM)")
    s_4_9_4 = Page((4, 9, 4), 87, "Load Rotation (LR)")
    s_4_9_5 = Page((4, 9, 5), 88, "Load Scaling (LS)")
    s_4_9_6 = Page((4, 9, 6), 88, "Example")
    s_4_10 = Page((4, 10), 90, "Region Statement (G36/G37)")
    s_4_10_1 = Page((4, 10, 1), 90, "Region Overview")
    s_4_10_2 = Page((4, 10, 2), 90, "Region Statement Syntax")
    s_4_10_3 = Page((4, 10, 3), 91, "Valid Contours")
    s_4_10_4 = Page((4, 10, 4), 93, "Examples")
    s_4_10_5 = Page((4, 10, 5), 108, "Copper Pours, Power and Ground Planes")
    s_4_11 = Page((4, 11), 111, "Block Aperture (AB)")
    s_4_11_1 = Page((4, 11, 1), 111, "Overview of block apertures")
    s_4_11_2 = Page((4, 11, 2), 111, "AB Statement Syntax")
    s_4_11_3 = Page((4, 11, 3), 113, "Usage of Block Apertures")
    s_4_11_4 = Page((4, 11, 4), 114, "Example")
    s_4_12 = Page((4, 12), 116, "Step and Repeat (SR)")
    s_4_13 = Page((4, 13), 119, "End-of-file (M02)")
    s_4_14 = Page((4, 14), 120, "Numerical Accuracy")
    s_4_14_1 = Page((4, 14, 1), 120, "Visualization")
    s_4_14_2 = Page((4, 14, 2), 120, "Image Processing")
    s_5 = Page((5,), 122, "Attributes")
    s_5_1 = Page((5, 1), 122, "Attributes Overview")
    s_5_2 = Page((5, 2), 125, "File Attributes (TF)")
    s_5_3 = Page((5, 3), 125, "Aperture Attributes (TA)")
    s_5_3_1 = Page((5, 3, 1), 126, "Aperture Attributes on Regions")
    s_5_4 = Page((5, 4), 126, "Object Attributes (TO)")
    s_5_5 = Page((5, 5), 127, "Delete Attribute (TD)")
    s_5_6 = Page((5, 6), 128, "Standard Attributes")
    s_5_6_1 = Page((5, 6, 1), 128, "Overview")
    s_5_6_2 = Page((5, 6, 2), 130, "Part")
    s_5_6_3 = Page((5, 6, 3), 131, "FileFunction")
    s_5_6_4 = Page((5, 6, 4), 136, "FilePolarity")
    s_5_6_5 = Page((5, 6, 5), 137, "SameCoordinates")
    s_5_6_6 = Page((5, 6, 6), 137, "CreationDate")
    s_5_6_7 = Page((5, 6, 7), 138, "GenerationSoftware")
    s_5_6_8 = Page((5, 6, 8), 138, "ProjectId")
    s_5_6_9 = Page((5, 6, 9), 139, "MD5")
    s_5_6_10 = Page((5, 6, 10), 140, "AperFunction")
    s_5_6_11 = Page((5, 6, 11), 148, "DrillTolerance")
    s_5_6_12 = Page((5, 6, 12), 148, "FlashText")
    s_5_6_13 = Page((5, 6, 13), 150, "N (Net)")
    s_5_6_14 = Page((5, 6, 14), 152, "P (Pin)")
    s_5_6_15 = Page((5, 6, 15), 153, "C (Component Refdes)")
    s_5_6_16 = Page((5, 6, 16), 154, "Cxxx (Component Characteristics)")
    s_5_7 = Page((5, 7), 156, "Text in the Image")
    s_5_8 = Page((5, 8), 157, "Examples")
    s_6 = Page((6,), 159, "PCB Fabrication and Assembly Data")
    s_6_1 = Page((6, 1), 159, "Structure")
    s_6_2 = Page((6, 2), 159, "Mandatory Attributes")
    s_6_3 = Page((6, 3), 159, "Alignment")
    s_6_4 = Page((6, 4), 159, "Pads")
    s_6_5 = Page((6, 5), 159, "The Profile")
    s_6_6 = Page((6, 6), 160, "Drill/rout files")
    s_6_6_1 = Page((6, 6, 1), 160, "Backdrilling")
    s_6_6_2 = Page((6, 6, 2), 161, "Example Drill File")
    s_6_7 = Page((6, 7), 164, "Drawings and Data")
    s_6_8 = Page((6, 8), 165, "The CAD Netlist")
    s_6_8_1 = Page((6, 8, 1), 165, "Benefits of Including the CAD Netlist")
    s_6_8_2 = Page((6, 8, 2), 166, "IP Considerations")
    s_6_9 = Page((6, 9), 167, "Component Data")
    s_6_9_1 = Page((6, 9, 1), 167, "Overview")
    s_6_9_2 = Page((6, 9, 2), 167, "Assembly Data Set")
    s_6_9_3 = Page((6, 9, 3), 168, "Annotated Example Component Layer")
    s_7 = Page((7,), 170, "Errors and Bad Practices")
    s_7_1 = Page((7, 1), 170, "Errors")
    s_7_2 = Page((7, 2), 172, "Bad Practices")
    s_8 = Page((8,), 174, "Deprecated Format Elements")
    s_8_1 = Page((8, 1), 174, "Deprecated Commands")
    s_8_1_1 = Page((8, 1, 1), 174, "Overview")
    s_8_1_2 = Page((8, 1, 2), 176, "Axis Select (AS)")
    s_8_1_3 = Page((8, 1, 3), 177, "Image Name (IN)")
    s_8_1_4 = Page((8, 1, 4), 178, "Image Polarity (IP)")
    s_8_1_5 = Page((8, 1, 5), 179, "Image Rotation (IR)")
    s_8_1_6 = Page((8, 1, 6), 180, "Load Name (LN)")
    s_8_1_7 = Page((8, 1, 7), 181, "Mirror Image (MI)")
    s_8_1_8 = Page((8, 1, 8), 182, "Offset (OF)")
    s_8_1_9 = Page((8, 1, 9), 183, "Scale Factor (SF)")
    s_8_1_10 = Page((8, 1, 10), 184, "Single-quadrant arc mode (G74)")
    s_8_2 = Page((8, 2), 188, "Deprecated Command Options")
    s_8_2_1 = Page((8, 2, 1), 188, "Format Specification (FS) Options")
    s_8_2_2 = Page((8, 2, 2), 189, "Rectangular Hole in Standard Apertures")
    s_8_2_3 = Page((8, 2, 3), 190, "Draws and Arcs with Rectangular Apertures")
    s_8_2_4 = Page((8, 2, 4), 191, "Macro Primitive Code 2, Vector Line")
    s_8_2_5 = Page((8, 2, 5), 191, "Macro Primitive Code 22, Lower Left Line")
    s_8_2_6 = Page((8, 2, 6), 192, "Macro Primitive Code 6, Moiré")
    s_8_3 = Page((8, 3), 193, "Deprecated Syntax Variations")
    s_8_3_1 = Page((8, 3, 1), 193, "Combining G01/G02/G03 and D01 in a single command.")
    s_8_3_2 = Page((8, 3, 2), 193, "Coordinate Data without Operation Code")
    s_8_3_3 = Page((8, 3, 3), 193, "Style Variations in Command Codes")
    s_8_3_4 = Page((8, 3, 4), 194, "Deprecated usage of SR")
    s_8_4 = Page((8, 4), 194, "Deprecated Attribute Values")
    s_8_5 = Page((8, 5), 195, "Standard Gerber (RS-274-D)")
    s_9 = Page((9,), 196, "References")
    s_10 = Page((10,), 197, "History")
    s_11 = Page((11,), 199, "Revisions")
    s_11_1 = Page((11, 1), 199, "Revision xxxx.xx")
    s_11_2 = Page((11, 2), 199, "Revision 2023.08")
    s_11_3 = Page((11, 3), 199, "Revision 2023.03")
    s_11_4 = Page((11, 4), 199, "Revision 2022.02")
    s_11_5 = Page((11, 5), 199, "Revision 2021.11")
    s_11_6 = Page((11, 6), 200, "Revision 2021.04")
    s_11_7 = Page((11, 7), 200, "Revision 2021.02 - Formal grammar")
    s_11_8 = Page((11, 8), 200, "Revision 2020.09 - X3")
    s_11_9 = Page((11, 9), 200, "Revision 2019.09")
    s_11_10 = Page((11, 10), 201, "Revision 2019.06")
    s_11_11 = Page((11, 11), 201, "Revision 2018.11")
    s_11_12 = Page((11, 12), 201, "Revision 2018.09")
    s_11_13 = Page((11, 13), 201, "Revision 2018.06")
    s_11_14 = Page((11, 14), 201, "Revision 2018.05")
    s_11_15 = Page((11, 15), 202, "Revision 2017.11")
    s_11_16 = Page((11, 16), 202, "Revision 2017.05")
    s_11_17 = Page((11, 17), 202, "Revision 2017.03")
    s_11_18 = Page((11, 18), 202, "Revision 2016.12 - Nested step and repeat")
    s_11_19 = Page((11, 19), 203, "Revision 2016.11")
    s_11_20 = Page((11, 20), 203, "Revision 2016.09")
    s_11_21 = Page((11, 21), 203, "Revision 2016.06")
    s_11_22 = Page((11, 22), 203, "Revision 2016.04")
    s_11_23 = Page((11, 23), 204, "Revision 2016.01")
    s_11_24 = Page((11, 24), 204, "Revision 2015.10")
    s_11_25 = Page((11, 25), 204, "Revision 2015.07")
    s_11_26 = Page((11, 26), 204, "Revision 2015.06")
    s_11_27 = Page((11, 27), 204, "Revision J4 (2015 02)")
    s_11_28 = Page((11, 28), 205, "Revision J3 (2014 10)")
    s_11_29 = Page((11, 29), 205, "Revision J2 (2014 07)")
    s_11_30 = Page((11, 30), 205, "Revision J1 (2014 02) - X2")
    s_11_31 = Page((11, 31), 205, "Revision I4 (2013 10)")
    s_11_32 = Page((11, 32), 205, "Revision I3 (2013 06)")
    s_11_33 = Page((11, 33), 205, "Revision I2 (2013 04)")
    s_11_34 = Page((11, 34), 205, "Revision I1 (2012 12)")


def d01() -> str:
    """Get doc about D01 command."""
    return f"""
- {Sections.s_2_6.markdown}
- {Sections.s_4_8_2.markdown}
"""


def d02() -> str:
    """Get doc about D02 command."""
    return f"""
- {Sections.s_2_6.markdown}
- {Sections.s_4_8_3.markdown}
"""


def d03() -> str:
    """Get doc about D03 command."""
    return f"""
- {Sections.s_2_6.markdown}
- {Sections.s_4_8_4.markdown}
"""


def to() -> str:
    """Get doc about TO command."""
    return f"""
- {Sections.s_5_4.markdown}
"""


def ta() -> str:
    """Get doc about TA command."""
    return f"""
- {Sections.s_5_3.markdown}
"""


def tf() -> str:
    """Get doc about TF command."""
    return f"""
- {Sections.s_5_2.markdown}
"""


def td() -> str:
    """Get doc about TD command."""
    return f"""
- {Sections.s_5_5.markdown}
"""


def dnn() -> str:
    """Get doc about Dnn command."""
    return f"""
- {Sections.s_4_6.markdown}
"""


def adc() -> str:
    """Get doc about AD command."""
    return f"""
- {Sections.s_4_3.markdown}
- {Sections.s_4_4_2.markdown}
"""


def adr() -> str:
    """Get doc about AD command."""
    return f"""
- {Sections.s_4_3.markdown}
- {Sections.s_4_4_3.markdown}
"""


def ado() -> str:
    """Get doc about AD command."""
    return f"""
- {Sections.s_4_3.markdown}
- {Sections.s_4_4_4.markdown}
"""


def adp() -> str:
    """Get doc about AD command."""
    return f"""
- {Sections.s_4_3.markdown}
- {Sections.s_4_4_5.markdown}
"""


def ad_macro() -> str:
    """Get doc about AD command."""
    return f"""
- {Sections.s_4_3.markdown}
- {Sections.s_4_5.markdown}
"""


def code_1() -> str:
    """Get doc about Code 1 primitive."""
    return f"""
- {Sections.s_4_5.markdown}
- {Sections.s_4_5_1_2.markdown}
- {Sections.s_4_5_1.markdown}
- {Sections.s_4_5_2.markdown}
- {Sections.s_4_5_3.markdown}
- {Sections.s_4_5_4.markdown}
"""
