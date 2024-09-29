# Multi file project guide

This guide shows how to use `Project` class in par with `GerberFile` class to render
multiple Gerber files into single, aligned image. Both classes can be imported from
`pygerber.gerber.api`. For overview of `pygerber.gerber.api` module check out
[Introduction](./00_introduction.md). For guide on how to operate on individual Gerber
files and create `GerberFile` class instances, check out
[Single file guide](./01_single_file.md).

For full reference of `pygerber.gerber.api` module check out
[Reference](./20_pygerber_gerber_api_reference.md)

## Creating Project instance

{{ include_definition("pygerber.gerber.api.Project", members="False", show_docstring_description="False", show_source="False", show_docstring_parameters="False", show_docstring_returns="False", heading_level="3") }}

`Project` class is a simple wrapper around multiple `GerberFile` objects. It
automatically aligns all images and determines how big final image has to be to fit all
images and merges them into single image. It is still possible to retrieve individual
images from result returned by rendering methods.

To create `Project` object you can use `Project` constructor. It accepts list of
`GerberFile` objects as its only parameter. You can add more files to project by using
`add_file()` method.

{{ include_code("test/examples/gerberx3/api/_70_project_constructor_showcase.project.py", "python", title="create_project.py", linenums="1") }}

{{ run_capture_stdout("python test/examples/gerberx3/api/_70_project_constructor_showcase.project.py", "python create_project.py") }}

## Rendering Project

{{ include_code("test/examples/gerberx3/api/_71_project_render_with_pillow.example.py", "python", title="render_project.py", linenums="1") }}

<p align="center">
    <img src="render_project.png" alt="render_project" width="300" />
</p>
