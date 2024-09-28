# Introduction

## Overview

This is a beginning of quick start guide for PyGerber. It uses a dedicated API which
exposes limited set of functionalities of PyGerber in very convenient way. It should
suite your needs if you are only looking for a quick way to render or format Gerber
file(s) with basic customization.

If you need to do something more complicated, you should check out **Advanced Guide** to
understand how PyGerber works and what can be achieved with its more complicated
interfaces.

## `pygerber.gerber.api` module

PyGerber exposes a simple API for accessing limited subset of its functionalities in
form of `pygerber.gerber.api` module. This interface is especially useful for one time
use, scripting and use from interactive shell. Most of the functionality has been
included in the `GerberFile` class and `Project` class. Additionally, there is a
`FileTypeEnum` containing recognized file types and some less important utility objects.

{{ pformat_variable("pygerber.gerber.api", "__all__") }}

For guide on how to use `GerberFile` class, check out
[Single file guide](./01_single_file.md).

For guide on how to use `Project` class, check out
[Multi file project guide](./02_multi_file_project.md).

Most of code examples (those with file name at the top of code frame) can be directly
copied and pasted into Python file, interactive shell or Jupyter notebook and executed.
