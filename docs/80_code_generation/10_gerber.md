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

To generate Gerber code you need to create an instance of
[`GerberX3Builder`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder)
class, afterwards you can use
[`new_pad()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder.new_pad)
method to create a new pad shape which can be added to the image with
[`add_pad()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder.add_pad)
method.

{{ include_code("test/examples/builder/gerber/_00_circle_pad.ex.py", "python", title="example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_00_circle_pad.ex.py", "python example.py", "gerber") }}

This is the rendered result of the example presented above:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_00_circle_pad.ex.py", 400) }}

---

## Adding traces

You can also add traces to the image with
[`new_trace()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder.add_trace)
method and
[`add_arc_trace()`](<(../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.GerberX3Builder.add_arc_trace)>)
method.

{{ include_code("test/examples/builder/gerber/_10_circle_pad_and_trace.ex.py", "python", title="example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_10_circle_pad_and_trace.ex.py", "python example.py", "gerber") }}

This is the rendered result of the example presented above:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_10_circle_pad_and_trace.ex.py", 200) }}

---

## Using objects as locations

Commands creating graphical elements, like `add_pad()` or `add_trace()` return special
`Draw` objects (`PadDraw` or `TraceDraw` respectively) which can be used as locations
for `new_pad()` or `new_trace()` methods. This way you don not have to retype
coordinates for draws which are connected to previous objects.

{{ include_code("test/examples/builder/gerber/_11_circle_pad_and_trace_with_reuse.ex.py", "python", title="example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_11_circle_pad_and_trace_with_reuse.ex.py", "python example.py", "gerber") }}

This is the rendered result of the example presented above:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_11_circle_pad_and_trace_with_reuse.ex.py", 200) }}

---

## Creating custom pads

You can create custom pads by using
[`custom()`](../reference/pygerber/builder/gerber.md#pygerber.builder.gerber.PadCreator.custom)
method of object returned by `new_pad()` method. Custom pads are built with use of
methods available on object returned by `custom()`. Method calls can (and should) be
chained. When you are done adding elements to the pad, you should call `create()` method
to finish the modification of custom pad and create concrete object representing it.
After calling `create()`, you cannot and new elements to that custom pad.

Custom pad is used in the same way as any other pad, to add it to the image you should
use `add_pad()` method.

{{ include_code("test/examples/builder/gerber/_20_custom_pad.ex.py", "python", title="custom_pad_example.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/builder/gerber/_20_custom_pad.ex.py", "python custom_pad_example.py", "gerber") }}

This is the rendered result of the example presented above:

---

{{ run_render_gerber_from_stdout("python test/examples/builder/gerber/_20_custom_pad.ex.py", 100) }}

---
