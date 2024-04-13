from __future__ import annotations

import os

from mkdocs_macros.plugin import MacrosPlugin


def define_env(env: MacrosPlugin) -> None:
    """This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """

    @env.macro
    def include_file(filename, start_line=0, end_line=None):  # type: ignore[no-untyped-def]
        """Include a file, optionally indicating start_line and end_line
        (start counting from 0)
        The path is relative to the top directory of the documentation
        project.
        """
        full_filename = os.path.join(env.project_dir, filename)
        with open(full_filename) as f:
            lines = f.readlines()
        line_range = lines[start_line:end_line]
        return "".join(line_range)
