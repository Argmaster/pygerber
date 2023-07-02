# Example: Transparency of Holes

Example 4.4.6 from Ucamco's `The Gerber Layer Format Specification - Revision 2023.03`.

Standard apertures may have a round hole in them. When an aperture is flashed only the
solid part affects the image, the hole does not. Objects under a hole remain visible
through the hole. For image generation the area of the hole behaves exactly as the area
outside the aperture. The hole is not part of the aperture.

**Warning**: Make no mistake: holes do not clear the objects under them.

For all standard apertures the round hole is defined by specifying its diameter as the
last parameter: <Hole diameter>. If <Hole diameter> is omitted the aperture is solid. If
present the diameter must be > 0. The hole must strictly fit within the standard
aperture. It is centered on the aperture.

![circle with hole and line crossing](image.png)
