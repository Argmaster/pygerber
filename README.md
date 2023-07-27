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

Supported Gerber X3 features:

- [x] G04 - Comment - A human readable comment, does not affect the image.
- [x] MO - Mode - Sets the unit to mm or inch.
- [x] FS - Format specification - Sets the coordinate format, e.g. the number of
      decimals.
- [x] FS (Deprecated modes)
- [x] AD - Aperture define - Defines a template-based aperture, assigns a D code to it.
- [x] AM - Aperture macro - Defines a macro aperture template.
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

**DEPRECATED** Gerber features:

- [ ] G54 - Select aperture - This historic code optionally precedes an aperture
      selection Dnn command. It has no effect. Sometimes used. Deprecated in 2012.
- [ ] G55 - Prepare for flash - This historic code optionally precedes D03 code. It has
      no effect. Very rarely used nowadays. Deprecated in 2012.
- [ ] G70 - Set the 'Unit' to inch - These historic codes perform a function handled by
      the MO command. See 4.2.1. Sometimes used. Deprecated in 2012.
- [ ] G71 - Set the 'Unit' to mm - This is part of the historic codes that perform a
      function handled by the MO command.
- [ ] G90 - Set the 'Coordinate format' to 'Absolute notation' - These historic codes
      perform a function handled by the FS command. Very rarely used nowadays.
      Deprecated in 2012.
- [ ] G91 - Set the 'Coordinate format' to 'Incremental notation' - Part of the historic
      codes handled by the FS command.
- [ ] G74 - Sets single quadrant mode - Rarely used, and then typically without effect.
      Deprecated in 2020. (Spec. 8.1.10)
- [ ] M00 - Program stop - This historic code has the same effect as M02. Very rarely,
      if ever, used nowadays. Deprecated in 2012.
- [ ] M01 - Optional stop - This historic code has no effect. Very rarely, if ever, used
      nowadays. Deprecated in 2012.
- [ ] IP - Sets the 'Image polarity' graphics state parameter - This command has no
      effect in CAD to CAM workflows. Sometimes used, and then usually as %IPPOS\*% to
      confirm the default and then it then has no effect. Deprecated in 2013. (Spec.
      8.1.4)
- [ ] AS - Sets the 'Axes correspondence' graphics state parameter - Deprecated in 2013.
      Rarely used nowadays. (Spec. 8.1.2)
- [ ] IR - Sets 'Image rotation' graphics state parameter - Deprecated in 2013. Rarely
      used nowadays. (Spec. 8.1.5)
- [ ] MI - Sets 'Image mirroring' graphics state parameter (Spec. 8.1.7)
- [ ] OF - Sets 'Image offset' graphics state parameter (Spec. 8.1.8)
- [ ] SF - Sets 'Scale factor' graphics state parameter (Spec. 8.1.9)
- [ ] IN - Sets the name of the file image. Has no effect. It is comment. Sometimes
      used. Deprecated in 2013. (Spec. 8.1.3)
- [ ] LN - Loads a name. Has no effect. It is a comment. Sometimes used. Deprecated
      in 2013. (Spec. 8.1.6)
- [ ] Combining G01/G02/G03 and D01 in a single command. (Spec 8.3.1)
- [ ] Coordinate Data without Operation Code. (Spec 8.3.2)
- [ ] Style Variations in Command Codes. (Spec 8.3.3)
- [ ] Deprecated usage of SR. (Spec 8.3.4)
- [ ] Deprecated Attribute Values. (Spec 8.4)
- [ ] Format Specification (FS) Options (Trailing Zero Omission, Incremental Notation).
      (Spec. 8.2)
- [ ] Rectangular Hole in Standard Apertures (Spec. 8.2.2)
- [ ] Draws and Arcs with Rectangular Apertures (Spec. 8.2.3)
- [ ] Macro Primitive Code 2, Vector Line (Spec. 8.2.4)
- [ ] Macro Primitive Code 22, Lower Left Line (Spec. 8.2.5)
- [ ] Macro Primitive Code 6, Moiré (Spec. 8.2.6)

## Parsing

Supported Gerber X3 features:

- [x] MO - Mode - Sets the unit to mm or inch.
- [x] FS - Format specification - Sets the coordinate format, e.g. the number of
      decimals.
- [ ] AD - Aperture define - Defines a template-based aperture, assigns a D code to it.
  - [x] Define circle.
  - [x] Define rectangle.
  - [x] Define obround.
  - [x] Define polygon.
  - [ ] Define macro.
- [ ] AM - Aperture macro - Defines a macro aperture template.
- [x] Dnn (nn≥10) - Sets the current aperture to D code nn.
- [x] D01 - Plot operation - Outside a region statement D01 creates a draw or arc object
      with the current aperture.
- [x] D01 - Plot operation - Inside region statement adds a draw/arc segment to the
      contour under construction. The current point is moved to draw/arc end point after
      the creation of the draw/arc.
- [x] D02 - Move operation - D02 moves the current point to the coordinate in the
      command. It does not create an object.
- [x] D03 - Flash operation - Creates a flash object with the current aperture. The
      current point is moved to the flash point.
- [x] G01 - Sets linear/circular mode to linear.
- [x] G02 - Sets linear/circular mode to clockwise circular.
- [x] G03 - Sets linear/circular mode to counterclockwise circular.
- [x] LP - Load polarity - Loads the polarity object transformation parameter.
- [x] LM - Load mirroring - Loads the mirror object transformation parameter.
- [x] LR - Load rotation - Loads the rotation object transformation parameter.
- [x] LS - Load scaling - Loads the scale object transformation parameter.
- [x] G36 - Starts a region statement which creates a region by defining its contours.
- [x] G37 - Ends the region statement.
- [ ] AB - Aperture block - Opens a block aperture statement and assigns its aperture
      number or closes a block aperture statement.
- [ ] SR - Step and repeat - Open or closes a step and repeat statement.
- [ ] TF - Attribute on file - Set a file attribute.
- [ ] TA - Attribute on aperture - Add an aperture attribute to the dictionary or modify
      it.
- [ ] TO - Attribute on object - Add an object attribute to the dictionary or modify it.
- [ ] TD - Attribute delete - Delete one or all attributes in the dictionary.
- [x] M02 - End of file.

Supported **DEPRECATED** Gerber features:

- [ ] G54 - Select aperture - This historic code optionally precedes an aperture
      selection Dnn command. It has no effect. Sometimes used. Deprecated in 2012.
- [ ] G55 - Prepare for flash - This historic code optionally precedes D03 code. It has
      no effect. Very rarely used nowadays. Deprecated in 2012.
- [ ] G70 - Set the 'Unit' to inch - These historic codes perform a function handled by
      the MO command. See 4.2.1. Sometimes used. Deprecated in 2012.
- [ ] G71 - Set the 'Unit' to mm - This is part of the historic codes that perform a
      function handled by the MO command.
- [ ] G90 - Set the 'Coordinate format' to 'Absolute notation' - These historic codes
      perform a function handled by the FS command. Very rarely used nowadays.
      Deprecated in 2012.
- [ ] G91 - Set the 'Coordinate format' to 'Incremental notation' - Part of the historic
      codes handled by the FS command.
- [ ] G74 - Sets single quadrant mode - Rarely used, and then typically without effect.
      Deprecated in 2020. (Spec. 8.1.10)
- [ ] M00 - Program stop - This historic code has the same effect as M02. Very rarely,
      if ever, used nowadays. Deprecated in 2012.
- [ ] M01 - Optional stop - This historic code has no effect. Very rarely, if ever, used
      nowadays. Deprecated in 2012.
- [ ] IP - Sets the 'Image polarity' graphics state parameter - This command has no
      effect in CAD to CAM workflows. Sometimes used, and then usually as %IPPOS\*% to
      confirm the default and then it then has no effect. Deprecated in 2013. (Spec.
      8.1.4)
- [ ] AS - Sets the 'Axes correspondence' graphics state parameter - Deprecated in 2013.
      Rarely used nowadays. (Spec. 8.1.2)
- [ ] IR - Sets 'Image rotation' graphics state parameter - Deprecated in 2013. Rarely
      used nowadays. (Spec. 8.1.5)
- [ ] MI - Sets 'Image mirroring' graphics state parameter (Spec. 8.1.7)
- [ ] OF - Sets 'Image offset' graphics state parameter (Spec. 8.1.8)
- [ ] SF - Sets 'Scale factor' graphics state parameter (Spec. 8.1.9)
- [ ] IN - Sets the name of the file image. Has no effect. It is comment. Sometimes
      used. Deprecated in 2013. (Spec. 8.1.3)
- [ ] LN - Loads a name. Has no effect. It is a comment. Sometimes used. Deprecated
      in 2013. (Spec. 8.1.6)
- [ ] Combining G01/G02/G03 and D01 in a single command. (Spec 8.3.1)
- [ ] Coordinate Data without Operation Code. (Spec 8.3.2)
- [ ] Style Variations in Command Codes. (Spec 8.3.3)
- [ ] Deprecated usage of SR. (Spec 8.3.4)
- [ ] Deprecated Attribute Values. (Spec 8.4)
- [ ] Format Specification (FS) Options (Trailing Zero Omission, Incremental Notation).
      (Spec. 8.2)
- [ ] Rectangular Hole in Standard Apertures (Spec. 8.2.2)
- [ ] Draws and Arcs with Rectangular Apertures (Spec. 8.2.3)
- [ ] Macro Primitive Code 2, Vector Line (Spec. 8.2.4)
- [ ] Macro Primitive Code 22, Lower Left Line (Spec. 8.2.5)
- [ ] Macro Primitive Code 6, Moiré (Spec. 8.2.6)

## Rasterized2DBackend feature support

- [x] Aperture definition with circle
- [x] Aperture definition with rectangle
- [x] Aperture definition with obround
- [x] Aperture definition with polygon
- [ ] Aperture definition with macro
- [ ] Block aperture definition
- [x] Draw flash
  - [x] circle aperture
  - [x] rectangle aperture
  - [x] obround aperture
  - [x] polygon aperture
  - [ ] macro aperture
  - [ ] block aperture
- [x] Draw line
- [x] Draw clockwise arc
- [x] Draw counterclockwise arc
- [ ] Global mirroring
- [ ] Global rotation
- [ ] Global scaling
- [ ] Create region
