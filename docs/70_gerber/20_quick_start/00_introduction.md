# Introduction

## Overview

This is a beginning of quick start guide for PyGerber. It uses a dedicated API which
exposes limited set of functionalities of PyGerber in very convenient way. It should
suite your needs if you are only looking for a quick way to render Gerber file(s) with
ability to choose basic options for parsing and rendering.

If you need to do something more complicated, you should check out **Advanced Guide** to
understand how PyGerber works and what can be achieved with its more complicated
interfaces.

## `pygerber.gerber.api` module

PyGerber exposes a simple API for accessing limited subset of its functionalities in
form of `pygerber.gerber.api` module. This interface is especially useful for one time
use, scripting and use from interactive shell. Most of the functionality has been
included in the GerberFile class and Project class. Additionally, there is a
FileTypeEnum containing recognized file types and few error classes.

## Creating `GerberFile` object

To perform any operations on Gerber file, like rendering or formatting, you have to
create `GerberFile` object wrapping actual Gerber code. Recommended way is to use one of
3 factory methods provided by GerberFile class.

To create `GerberFile` from `str` object you can use
[`GerberFile.from_str`](./20_gerber_file.md#pygerber.gerber.api.GerberFile.from_str)
factory method. It accepts up to two arguments. First one is mandatory `source_code` and
you should pass Gerber code `str` object to it. Second one is optional and can be used
to manually set file type (eg. silk screen, copper, drill etc.). If second argument is
not provided, default behavior is to try to guess file type based on file extension or
file attributes. Method returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_90_quick_start_from_str.py", "python", title="example_from_str.py", linenums="1", hl_lines="12") }}

Alternatively you can create `GerberFile` object from file using
[`GerberFile.from_file`](./20_gerber_file.md#pygerber.gerber.api.GerberFile.from_file)
factory method. It accepts up to two arguments. First one is mandatory `file_path` which
has to be a path to existing file, either as `str` or `pathlib.Path` objec. Second one
is optional and can be used to manually set file type (eg. silk screen, copper, drill
etc.). If second argument is not provided, default behavior is to try to guess file type
based on file extension or file attributes. Method returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_91_quick_start_from_file.py", "python", title="example_from_file.py", linenums="1", hl_lines="6") }}

Last way to create `GerberFile` object is to use
[`GerberFile.from_buffer`](./20_gerber_file.md#pygerber.gerber.api.GerberFile.from_buffer)
factory method. It accepts up to two arguments. First one is mandatory `buffer` which
has to be a `StringIO`-like object supporting `read()` method. Second one is optional
and can be used to manually set file type (eg. silk screen, copper, drill etc.). If
second argument is not provided, default behavior is to try to guess file type based on
file extension or file attributes. Method returns `GerberFile` instance.

{{ include_code("test/examples/gerberx3/api/_92_quick_start_from_buffer.py", "python", title="example_from_buffer.py", linenums="1", hl_lines="5") }}
