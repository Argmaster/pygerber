"""The `rev_2024_05` module contains selected fragments from The Gerber Layer Format
Specification - Revision 2024.05 used to provide information about gerber standard
in messages shown to users of PyGerber.
"""

from __future__ import annotations


def d01() -> str:
    """Get doc about D01 command."""
    return """### 4.8.2 Plot (D01)

Performs a plotting operation, creating a draw or an arc segment. The plot state defines
which type of segment is created, see 4.7. The syntax depends on the required
parameters, and, hence, on the plot state.

---

| **Syntax**     | **Comments**                                                                                                                                                       |
|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| _x_coordinate_ | Coordinate is coordinate data - see section 4.2.2. It defines the X coordinate of the new current point. The default is the X coordinate of the old current point. |
| _y_coordinate_ | As above, but for the Y coordinate                                                                                                                                 |
| _i_offset_     | Offset is the offset in X - see section 0. It defines the X coordinate the center of the circle. It is of the coordinate type. There is no default offset.         |
| _j_offset_     | As above, but for the Y axis.                                                                                                                                      |
| _D01_          | Move operation code                                                                                                                                                |

---

After the plotting operation the current point is set to X,Y.

"""
