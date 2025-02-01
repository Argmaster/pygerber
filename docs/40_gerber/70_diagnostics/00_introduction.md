# 🧭 Introduction

## Overview

PyGerber provides a linter (diagnostic tool) for analyzing Gerber code. The linter is a
tool that focuses on checking the code itself, not the design of the PCB. Therefore it
includes checks for deprecated features, common deviations from Gerber standard and
other Gerber focused checks, but does not contain any check that verify the quality of
the PCB design, like connectivity, trace width, etc.

The Gerber linter is a tool that has limited usefulness for the average user, but can be
very handy for verifying the quality of generated Gerber code, especially while working
on solutions that modify or generate Gerber code, to ensure compliance with latest
Gerber standard.

## API

Gerber linter API is available in the `pygerber.gerber.linter` module. Simplified
interface consists of a single function `lint` that takes a Gerber AST as input and
returns a list of rule violations detected in AST.

Here is a simple example of how to use the linter:

{{ include_code("test/examples/gerberx3/linter/_00_linter.example.py", "docspygerberlexer", title="custom_color_map.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/gerberx3/linter/_00_linter.example.py", "python example.py") }}
