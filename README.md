# PyGerber

PyGerber is a Python implementation of Gerber X3 and partially X2 format. Main goal of
this project is to support widest range of Gerber-like formats possible.

Currently all systems are under active development.

You can view progress of development in Support section down below. All Gerber source
files which can be redistributed under MIT license and included in this repository for
testing purposes will be greatly appreciated.

All deprecated features (Mainly those from X2 format) are considered optional and
priority to implement them will be assigned based on number of requests for supporting
them and testing resources which can be used to validate them. If your program is
outputting code which is not Gerber spec compliant (ie. contains additional features
incompatible with standard Gerber X3 parsers) and this feature is not already listed in
Support paragraph, please create issue with detailed description how this feature works
and include code samples with reference images showing how output should look like (if
this feature causes changes to output image, otherwise image can be omitted).

# Development

To quickly set up development environment, first you have to install `poetry` globally:

```
pip install poetry
```

Afterwards you will be able to create development virtual environment:

```
poetry shell
```

Then You have to install dependencies:

```
poetry install
```

Last thing is installation of pre-commit hooks:

```
poe install-hooks
```

Now you are good to go. Whenever you commit changes, pre-commit hooks will be invoked.
If they fail or change files, you will have to re-add changes and commit again.

# Support

## Tokenizer:

- [x] G04 - Comment - A human readable comment, does not affect the image.
- [x] MO - Mode - Sets the unit to mm or inch.
- [x] FS - Format specification - Sets the coordinate format, e.g. the number of
      decimals.
- [x] FS (Deprecated modes)
- [x] AD - Aperture define - Defines a template-based aperture, assigns a D code to it.
- [x] AM - Aperture macro - Defines a macro aperture template.
- [ ] AM - **DEPRECATED** primitive Moiré
- [x] Dnn (nn≥10) - Sets the current aperture to D code nn.
- [x] D01 - Plot operation - Outside a region statement D01 creates a draw or arc object
      with the current aperture. Inside it adds a draw/arc segment to the contour under
      construction. The current point is moved to draw/arc end point after the creation
      of the draw/arc.
- [x] D02 - Move operation - D02 moves the current point to the coordinate in the
      command. It does not create an object.
- [x] D03 - Flash operation - Creates a flash object with the current aperture. The
      current point is moved to the flash point.
- [x] G01 - Sets linear/circular mode to linear.
- [x] G02 - Sets linear/circular mode to clockwise circular.
- [x] G03 - Sets linear/circular mode to counterclockwise circular.
- [x] G75 - A G75 must be called before creating the first arc.
- [x] LP - Load polarity - Loads the polarity object transformation parameter.
- [x] LM - Load mirroring - Loads the mirror object transformation parameter.
- [x] LR - Load rotation - Loads the rotation object transformation parameter.
- [x] LS - Load scaling - Loads the scale object transformation parameter.
- [x] G36 - Starts a region statement which creates a region by defining its contours.
- [x] G37 - Ends the region statement.
- [x] AB - Aperture block - Opens a block aperture statement and assigns its aperture
      number or closes a block aperture statement.
- [x] SR - Step and repeat - Open or closes a step and repeat statement.
- [x] TF - Attribute on file - Set a file attribute.
- [x] TA - Attribute on aperture - Add an aperture attribute to the dictionary or modify
      it.
- [x] TO - Attribute on object - Add an object attribute to the dictionary or modify it.
- [x] TD - Attribute delete - Delete one or all attributes in the dictionary.
- [x] M02 - End of file.
- [ ] G54 - **DEPRECATED** Select aperture - This historic code optionally precedes an
      aperture selection Dnn command. It has no effect. Sometimes used. Deprecated
      in 2012.
- [ ] G55 - **DEPRECATED** Prepare for flash - This historic code optionally precedes
      D03 code. It has no effect. Very rarely used nowadays. Deprecated in 2012.
- [ ] G70 - **DEPRECATED** Set the 'Unit' to inch - These historic codes perform a
      function handled by the MO command. See 4.2.1. Sometimes used. Deprecated in 2012.
- [ ] G71 - **DEPRECATED** Set the 'Unit' to mm - This is part of the historic codes
      that perform a function handled by the MO command.
- [ ] G90 - **DEPRECATED** Set the 'Coordinate format' to 'Absolute notation' - These
      historic codes perform a function handled by the FS command. Very rarely used
      nowadays. Deprecated in 2012.
- [ ] G91 - **DEPRECATED** Set the 'Coordinate format' to 'Incremental notation' - Part
      of the historic codes handled by the FS command.
- [ ] G74 - **DEPRECATED** Sets single quadrant mode - Rarely used, and then typically
      without effect. Deprecated in 2020.
- [ ] M00 - **DEPRECATED** Program stop - This historic code has the same effect as M02.
      Very rarely, if ever, used nowadays. Deprecated in 2012.
- [ ] M01 - **DEPRECATED** Optional stop - This historic code has no effect. Very
      rarely, if ever, used nowadays. Deprecated in 2012.
- [ ] IP - **DEPRECATED** Sets the 'Image polarity' graphics state parameter - This
      command has no effect in CAD to CAM workflows. Sometimes used, and then usually as
      %IPPOS\*% to confirm the default and then it then has no effect. Deprecated
      in 2013.
- [ ] AS - **DEPRECATED** Sets the 'Axes correspondence' graphics state parameter -
      Deprecated in 2013. Rarely used nowadays.
- [ ] IR - **DEPRECATED** Sets 'Image rotation' graphics state parameter - Deprecated
      in 2013. Rarely used nowadays.
- [ ] MI - **DEPRECATED** Sets 'Image mirroring' graphics state parameter
- [ ] OF - **DEPRECATED** Sets 'Image offset' graphics state parameter
- [ ] SF - **DEPRECATED** Sets 'Scale factor' graphics state parameter
- [ ] IN - **DEPRECATED** Sets the name of the file image. Has no effect. It is comment.
      Sometimes used. Deprecated in 2013.
- [ ] LN - **DEPRECATED** Loads a name. Has no effect. It is a comment. Sometimes used.
      Deprecated in 2013.

## Parsing

- [ ] G04 - Comment - A human readable comment, does not affect the image.
- [ ] MO - Mode - Sets the unit to mm or inch.
- [ ] FS - Format specification - Sets the coordinate format, e.g. the number of
      decimals.
- [ ] FS (Deprecated modes)
- [ ] AD - Aperture define - Defines a template-based aperture, assigns a D code to it.
- [ ] AM - Aperture macro - Defines a macro aperture template.
- [ ] Dnn (nn≥10) - Sets the current aperture to D code nn.
- [ ] D01 - Plot operation - Outside a region statement D01 creates a draw or arc object
      with the current aperture. Inside it adds a draw/arc segment to the contour under
      construction. The current point is moved to draw/arc end point after the creation
      of the draw/arc.
- [ ] D02 - Move operation - D02 moves the current point to the coordinate in the
      command. It does not create an object.
- [ ] D03 - Flash operation - Creates a flash object with the current aperture. The
      current point is moved to the flash point.
- [ ] G01 - Sets linear/circular mode to linear.
- [ ] G02 - Sets linear/circular mode to clockwise circular.
- [ ] G03 - Sets linear/circular mode to counterclockwise circular.
- [ ] G75 - A G75 must be called before creating the first arc.
- [ ] LP - Load polarity - Loads the polarity object transformation parameter.
- [ ] LM - Load mirroring - Loads the mirror object transformation parameter.
- [ ] LR - Load rotation - Loads the rotation object transformation parameter.
- [ ] LS - Load scaling - Loads the scale object transformation parameter.
- [ ] G36 - Starts a region statement which creates a region by defining its contours.
- [ ] G37 - Ends the region statement.
- [ ] AB - Aperture block - Opens a block aperture statement and assigns its aperture
      number or closes a block aperture statement.
- [ ] SR - Step and repeat - Open or closes a step and repeat statement.
- [ ] TF - Attribute on file - Set a file attribute.
- [ ] TA - Attribute on aperture - Add an aperture attribute to the dictionary or modify
      it.
- [ ] TO - Attribute on object - Add an object attribute to the dictionary or modify it.
- [ ] TD - Attribute delete - Delete one or all attributes in the dictionary.
- [ ] M02 - End of file.
- [ ] G54 - **DEPRECATED** Select aperture - This historic code optionally precedes an
      aperture selection Dnn command. It has no effect. Sometimes used. Deprecated
      in 2012.
- [ ] G55 - **DEPRECATED** Prepare for flash - This historic code optionally precedes
      D03 code. It has no effect. Very rarely used nowadays. Deprecated in 2012.
- [ ] G70 - **DEPRECATED** Set the 'Unit' to inch - These historic codes perform a
      function handled by the MO command. See 4.2.1. Sometimes used. Deprecated in 2012.
- [ ] G71 - **DEPRECATED** Set the 'Unit' to mm - This is part of the historic codes
      that perform a function handled by the MO command.
- [ ] G90 - **DEPRECATED** Set the 'Coordinate format' to 'Absolute notation' - These
      historic codes perform a function handled by the FS command. Very rarely used
      nowadays. Deprecated in 2012.
- [ ] G91 - **DEPRECATED** Set the 'Coordinate format' to 'Incremental notation' - Part
      of the historic codes handled by the FS command.
- [ ] G74 - **DEPRECATED** Sets single quadrant mode - Rarely used, and then typically
      without effect. Deprecated in 2020.
- [ ] M00 - **DEPRECATED** Program stop - This historic code has the same effect as M02.
      Very rarely, if ever, used nowadays. Deprecated in 2012.
- [ ] M01 - **DEPRECATED** Optional stop - This historic code has no effect. Very
      rarely, if ever, used nowadays. Deprecated in 2012.
- [ ] IP - **DEPRECATED** Sets the 'Image polarity' graphics state parameter - This
      command has no effect in CAD to CAM workflows. Sometimes used, and then usually as
      %IPPOS\*% to confirm the default and then it then has no effect. Deprecated
      in 2013.
- [ ] AS - **DEPRECATED** Sets the 'Axes correspondence' graphics state parameter -
      Deprecated in 2013. Rarely used nowadays.
- [ ] IR - **DEPRECATED** Sets 'Image rotation' graphics state parameter - Deprecated
      in 2013. Rarely used nowadays.
- [ ] MI - **DEPRECATED** Sets 'Image mirroring' graphics state parameter
- [ ] OF - **DEPRECATED** Sets 'Image offset' graphics state parameter
- [ ] SF - **DEPRECATED** Sets 'Scale factor' graphics state parameter
- [ ] IN - **DEPRECATED** Sets the name of the file image. Has no effect. It is comment.
      Sometimes used. Deprecated in 2013.
- [ ] LN - **DEPRECATED** Loads a name. Has no effect. It is a comment. Sometimes used.
      Deprecated in 2013.

## Drawing

- [ ] Flashes with circles
- [ ] Flashes with rectangles
- [ ] Flashes with obrounds
- [ ] Flashes with polygons
- [ ] Flashes with macros
- [ ] Lines with circles
- [ ] Lines with rectangles
- [ ] Lines with obrounds
- [ ] Lines with polygons
- [ ] Lines with macros
- [ ] Clockwise arcs with circles
- [ ] Clockwise arcs with rectangles
- [ ] Clockwise arcs with obrounds
- [ ] Clockwise arcs with polygons
- [ ] Clockwise arcs with macros
- [ ] Counterclockwise arcs with circles
- [ ] Counterclockwise arcs with rectangles
- [ ] Counterclockwise arcs with obrounds
- [ ] Counterclockwise arcs with polygons
- [ ] Counterclockwise arcs with macros
- [ ] Aperture macros with circles
- [ ] Aperture macros with vector lines
- [ ] Aperture macros with center lines
- [ ] Aperture macros with outlines
- [ ] Aperture macros with polygons
- [ ] Aperture macros with thermals
- [ ] Aperture macros with moiré
- [ ] Step and repeat
- [ ] Aperture blocks
