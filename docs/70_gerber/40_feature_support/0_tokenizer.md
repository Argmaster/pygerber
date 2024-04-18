# Tokenizer feature support

## Introduction

Tokenizer class is responsible for converting input Gerber string into sequence of
tokens suitable for consumption by `Parser` class. Tokenizer class is compatible with
both `Parser` and `Parser2` classes.

!!! tip "Contributing"

    Community contributions are always welcome.

| Symbol | Meaning                                    |
| ------ | ------------------------------------------ |
| ✅     | Feature implemented and usable.            |
| 🚧     | Work in progress. Related APIs can change. |
| 🚫     | Not planned, unless contributed or needed. |
| ❌     | Not implemented, but planned.              |
| 👽     | Partially implemented.                     |
| 👾     | Bugged.                                    |
| -      | -                                          |

| Symbol | Count |
| ------ | ----- |
| ✅     | 170   |
| 🚧     | 0     |
| 🚫     | 2     |
| ❌     | 7     |
| 👽     | 1     |
| 👾     | 0     |
| total  | 186   |

## Supported Gerber X3 features

### General

-   ✅ MO - Mode - Sets the unit to mm or inch.
-   ✅ FS - Format specification:
    -   ✅ absolute coordinates.
    -   ✅ incremental coordinates
    -   ✅ trailing zeros omission.
    -   ✅ leading zeros omission.
-   ✅ AD - Aperture define - Defines a template-based aperture, assigns a D code to it.
    -   ✅ circle.
    -   ✅ rectangle.
    -   ✅ obround.
    -   ✅ polygon.
    -   ✅ Define macro.
-   ✅ AM - Aperture macro - Defines a macro aperture template.
-   ✅ Dnn (nn≥10) - Sets the current aperture to D code nn.
-   ✅ G01 - Sets draw mode to linear.
    -   ✅ Variable zero padding variants allowed.
-   ✅ G02 - Sets draw mode to clockwise circular.
    -   ✅ Variable zero padding variants allowed.
-   ✅ G03 - Sets draw mode to counterclockwise circular.
    -   ✅ Variable zero padding variants allowed.
-   ✅ LP - Load polarity (changes flag, not fully implemented).
-   ✅ LM - Load mirroring (changes flag, not fully implemented).
-   ✅ LR - Load rotation (changes flag, not fully implemented).
-   ✅ LS - Load scaling (changes flag, not fully implemented).
-   ✅ TF - Attribute on file.
-   ✅ TA - Attribute on aperture.
-   ✅ TO - Attribute on object.
-   ✅ TD - Attribute delete.
-   ✅ M02 - End of file.

### D01, D02, D03

-   ✅ D01 - Plot operation, mode
    -   ✅ Line, with:
        -   ✅ circle,
        -   ✅ rectangle,
        -   ✅ obround,
        -   ✅ polygon,
        -   ✅ macro.
    -   ✅ Arc, with:
        -   ✅ circle,
        -   ✅ rectangle,
        -   ✅ obround,
        -   ✅ polygon,
        -   ✅ macro.
    -   ✅ Counter clockwise arc, with:
        -   ✅ circle,
        -   ✅ rectangle,
        -   ✅ obround,
        -   ✅ polygon,
        -   ✅ macro.
    -   ✅ Variable zero padding variants allowed.
-   ✅ D02 - Move operation
    -   ✅ Variable zero padding variants allowed.
-   ✅ D03 - Flash operation, with
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
    -   ✅ Variable zero padding variants allowed.

### Regions

-   ✅ G36 - Starts a region statement.
-   ✅ G37 - Ends the region statement.
-   ✅ Regions, with:
    -   ✅ Line, aperture:
        -   ✅ circle,
        -   ✅ rectangle,
        -   ✅ obround,
        -   ✅ polygon,
        -   ✅ macro.
    -   ✅ Arc, aperture:
        -   ✅ circle,
        -   ✅ rectangle,
        -   ✅ obround,
        -   ✅ polygon,
        -   ✅ macro.
    -   ✅ Counter clockwise arc, aperture:
        -   ✅ circle,
        -   ✅ rectangle,
        -   ✅ obround,
        -   ✅ polygon,
        -   ✅ macro.

### Macros

-   ✅ Parameters.
-   ✅ Primitives:
    -   ✅ Code 0, Comment
    -   ✅ Code 1, Circle
    -   ✅ Code 20, Vector line
    -   ✅ Code 21, Center Line
    -   ✅ Code 4, Outline
    -   ✅ Code 5, Polygon
    -   ✅ Code 7, Thermal
-   ✅ Rotation around macro origin:
    -   ✅ Code 0, Comment
    -   ✅ Code 1, Circle
    -   ✅ Code 20, Vector line
    -   ✅ Code 21, Center Line
    -   ✅ Code 4, Outline
    -   ✅ Code 5, Polygon
    -   ✅ Code 7, Thermal
-   ✅ Constants.
-   ✅ Variables.
-   ✅ Variable definitions.

### Aperture blocks

-   ✅ Nested Line, aperture:
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
-   ✅ Nested Arc, aperture:
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
-   ✅ Nested Counter clockwise arc, aperture:
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
-   ✅ Nested Flash:
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
-   ✅ Nested regions (missing macro support).

### Step and repeat

-   ✅ Nested Line, aperture:
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
-   ✅ Nested Arc, aperture:
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
-   ✅ Nested Counter clockwise arc, aperture:
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
-   ✅ Nested Flash:
    -   ✅ circle,
    -   ✅ rectangle,
    -   ✅ obround,
    -   ✅ polygon,
    -   ✅ macro.
-   ✅ Nested regions (missing macro support).
-   ✅ Nested blocks (missing macro support).

## Supported DEPRECATED Gerber features

-   ✅ G54 - Select aperture. (Spec. 8.1.1)
-   ✅ G55 - Prepare for flash. (Spec. 8.1.1)
-   ✅ G70 - Set the 'Unit' to inch. (Spec. 8.1.1)
-   ✅ G71 - Set the 'Unit' to mm. (Spec. 8.1.1)
-   ✅ G90 - Set the 'Coordinate format' to 'Absolute notation'. (Spec. 8.1.1)
-   ✅ G91 - Set the 'Coordinate format' to 'Incremental notation'. (Spec. 8.1.1)

    -   **Important**: _Incremental notation itself is not supported and is not planned
        due to lack of test assets and expected complications during implementation._

-   ✅ M00 - Program stop. (Spec. 8.1.1)
-   ✅ M01 - Optional stop. (Spec. 8.1.1)
-   ✅ AS - Sets the 'Axes correspondence'. (Spec. 8.1.2)
-   ✅ IN - Sets the name of the file image. (Spec. 8.1.3)
-   ✅ IP - Sets the 'Image polarity'. (Spec. 8.1.4)
-   ✅ IR - Sets 'Image rotation' graphics state parameter. (Spec. 8.1.5)
-   ✅ LN - Loads a name. (Spec. 8.1.6)
-   ❌ MI - Sets 'Image mirroring' graphics state parameter (Spec. 8.1.7)
-   👽 OF - Sets 'Image offset' graphics state parameter (Spec. 8.1.8)
-   ❌ SF - Sets 'Scale factor' graphics state parameter (Spec. 8.1.9)
-   ✅ G74 - Sets single quadrant mode. (Spec. 8.1.10)
-   🚫 Format Specification (FS) Options. (Spec. 8.2.1)
-   🚫 Rectangular aperture hole in standard apertures. (Spec. 8.2.2)
-   ✅ Draws and arcs wit rectangular apertures. (Spec. 8.2.3)
-   ❌ Macro Primitive Code 2, Vector Line. (Spec 8.2.4)
-   ❌ Macro Primitive Code 22, Lower Left Line. (Spec 8.2.5)
-   ❌ Macro Primitive Code 6, Moiré. (Spec 8.2.6)
-   ✅ Combining G01/G02/G03/G70/G71 and D01 in a single command. (Spec 8.3.1)
-   ✅ Combining G01/G02/G03/G70/G71 and D02 in a single command. (Spec 8.3.1)
-   ✅ Combining G01/G02/G03/G70/G71 and D03 in a single command. (Spec 8.3.1)
-   ✅ Coordinate Data without Operation Code. (Spec 8.3.2)
-   ✅ Style Variations in Command Codes. (Spec 8.3.3)
-   ❌ Deprecated usage of SR. (Spec 8.3.4)
-   ❌ Deprecated Attribute Values. (Spec 8.4)

    -   **Important**: _Incremental notation itself is not supported and is not planned
        due to lack of test assets and expected complications during implementation._

> PS. I had great time adding emoji to this table.
