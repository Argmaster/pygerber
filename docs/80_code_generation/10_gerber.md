# Gerber code generation

## Overview

This section describes how to generate Gerber code with use of the
[`pygerber.builder.gerber`](../reference/pygerber/builder/gerber.md) module.

All of the code building functionality is provided within
[`GerberX3Builder`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder)
class available in that module.

For reference of tools available in that module check out
[this](../reference/pygerber/builder/gerber.md) reference page.

## Creating pads

To generate Gerber code first you have to create an instance of
[`GerberX3Builder`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder)
class. Then you can use
[`PadCreator`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.PadCreator)
object returned by
[`new_pad()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder.new_pad)
method to create a pad brush / pad template (in Gerber format it is called aperture)
describing the shape of the pad. You can choose one of the predefined shapes (`circle`,
`rectangle`, `rounded_rectangle` , `polygon`) or create a custom shape composed from
predefined elements (with `custom()` method). To add actual pad to a image you have to
pass `Pad` object, representing pad brush, to the
[`add_pad()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder.add_pad)
method you can add actual pads to the image.

!!! info

    You can use same `Pad` object to create multiple pads in the image.
    To do that, simply pass it to multiple `add_pad()` calls.

In a example below, we create a circle aperture with `new_pad().circle()` call chain. It
returns a `Pad` object which we will store in a variable `d10`. Then we can pass this
variable to `add_pad()` method to add two pads to the image, first at location (1, 1),
second at (2, 1).

{{ include_code("test/examples/builder/gerber/_00_circle_pad.ex.py", "docspygerberlexer", title="example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_00_circle_pad.ex.py", "python example.py", "gerber") }}

Gerber code generated with the example above results in following image when rendered
with PyGerber:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_00_circle_pad.ex.py", 400) }}

---

!!! warning

    Do not use `Pad` objects created with one instance of `GerberX3Builder` with another
    instance of `GerberX3Builder`. This will result in an error or invalid Gerber code
    being generated.

For full reference of shapes available in `PadCreator` check out
[this reference page](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.PadCreator).

## Adding traces

[`GerberX3Builder`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder)
class also provides means to add traces to the Gerber image. You can use
[`new_trace()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder.add_trace)
and
[`add_arc_trace()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder.add_arc_trace)
methods to do that. Fist one creates a straight lines, second one creates arcs. You
don't need to create pads to add traces, but you have to provide width of the trace as
first argument.

!!! info

    New trace can, but doesn't have to be connected to previous trace or pad
    (differently than in Gerber format, there you have to explicitly change starting
    point of consecutive disconnected trace). It is recommended however that, if you have a
    series of traces that are starting from the end of previous trace, you should create
    them directly one after another, instead of jumping. This will result in smaller Gerber
    files.

{{ include_code("test/examples/builder/gerber/_10_circle_pad_and_trace.ex.py", "docspygerberlexer", title="example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_10_circle_pad_and_trace.ex.py", "python example.py", "gerber") }}

Gerber code generated with the example above results in following image when rendered
with PyGerber:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_10_circle_pad_and_trace.ex.py", 200) }}

---

## Using objects as locations

Commands creating graphical elements, like `add_pad()` or `add_trace()` return special
`Draw` objects (`PadDraw` or `TraceDraw` respectively) which can be used as locations
for `new_pad()` or `new_trace()` method calls. This way you don not have to retype
coordinates for draws which are connected to previous objects.

!!! warning

    When passing `TraceDraw` to `new_trace()` method, when you pass a trace as first parameter
    (begin) its end location will be used, but when you pass it as second parameter (end),
    its begin location will be used. So passing `TraceDraw` as both parameters will result
    in a trace going opposite direction than the original trace.

    This is helpful when starting a new trace from the end of the previous trace or
    connecting it to the end of existing trace, but can be confusing when you want to
    connect traces in different way.

{{ include_code("test/examples/builder/gerber/_11_circle_pad_and_trace_with_reuse.ex.py", "docspygerberlexer", title="example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_11_circle_pad_and_trace_with_reuse.ex.py", "python example.py", "gerber") }}

Gerber code generated with the example above results in following image when rendered
with PyGerber:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_11_circle_pad_and_trace_with_reuse.ex.py", 200) }}

---

## Creating custom pads

You can create custom pads shapes by using
[`custom()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.PadCreator.custom)
method of
[`PadCreator`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.PadCreator)
returned by `new_pad()` method. Custom pads are composed of predefined shapes added to
pad with use of methods available on
[`CustomPadCreator`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.CustomPadCreator)
returned by `custom()`. Method calls can (and should) be chained. When you are done
adding elements to the pad, you should call `create()` method to finish the modification
of custom pad and create concrete object representing it. After calling `create()`, you
cannot and new elements to that custom pad.

!!! warning

    Coordinates used during creation are local (relative to (0, 0) point of pad canvas),
    not global. During custom pad creation elements added to the pad are not placed in
    global image space. They are added to image (canvas) dedicated for that pad. When
    pad is added to the main image with `add_pad()` (0, 0) point of that "canvas" is placed
    at the location where the pad is added. All the pad elements are translated
    relatively to that point.

!!! tip

    You can add cutouts in different shapes to the custom pad by using `cut_*` methods.
    Those cutouts are made locally to the pad, but they will not create cutouts in the
    main image after adding the pad to it (they will not remove content below the pad),
    they will simply be transparent.

Custom pad is used in the same way as any other pad, to add it to the image you should
use `add_pad()` method.

{{ include_code("test/examples/builder/gerber/_20_custom_pad.ex.py", "docspygerberlexer", title="custom_pad_example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_20_custom_pad.ex.py", "python custom_pad_example.py", "gerber") }}

Gerber code generated with the example above results in following image when rendered
with PyGerber:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_20_custom_pad.ex.py", 100) }}

---

## Creating regions

Process of creating regions (copper pours / fills) is managed by
[`RegionCreator`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.RegionCreator)
class instances which can be obtained by calling `new_region()` method on
[`GerberX3Builder`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder).

Regions are defined by their outline made out of series of lines and / or arcs. Outline
starts at point specified in `new_region()` call and it is always continuous series of
lines / arcs. Each line / arc start at the end of previous arc / line. If end of last
line / arc does not overlap with first point, last and first point are connected with
straight line.

Region is added automatically to the image after calling `create()` method. After
`create()` method is called you can no longer modify the region.

{{ include_code("test/examples/builder/gerber/_40_region.ex.py", "docspygerberlexer", title="custom_pad_example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_40_region.ex.py", "python custom_pad_example.py", "gerber") }}

Gerber code generated with the example above results in following image when rendered
with PyGerber:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_40_region.ex.py", 100) }}

---

!!! warning

    Region outline can not self intersect and there must be at least 3 points in the
    outline.

    There are also few restrictions implied by Gerber format regarding regions with cut-ins:

    > Cut-ins are subject to strict requirements:
    >
    > - they must consist of two fully-coincident linear segments; a pair of linear segments are said to
    >   be fully coincident if the segments coincide, with the second segment starting where the
    >   first one ends
    >
    > - cut-ins must be either horizontal or vertical
    >
    > - all cut-ins in a contour must have the same direction, either horizontal or vertical;
    >
    > - cut-ins can only touch or overlap the contour in their start and end points.
