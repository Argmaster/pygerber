# Documentation

PyGerber uses [MkDocs](https://pypi.org/project/mkdocs/) library and Markdown syntax to
write documentation. Documentation can be divided into two parts:

- manually written documentation
- automatically generated documentation

First one is stored in `docs` directory and is written in Markdown. Second one is
generated from docstrings in source code using
[mkdocstrings](https://pypi.org/project/mkdocstrings/) package and it is automatically
collected during documentation build.

Before building documentation, make sure that you have completed development environment
setup described in [Environment setup](./10_env_setup.md) section. After completing
initial setup you should be able to continue following this guide.

To generate HTML/CSS/JS files containing distribution of documentation, use following
command:

```
mkdocs build
```

This command will create `site` directory and place all necessary HTML/CSS/JS files
there.

MkDocs also offers a live preview of documentation with automatic reload on file change.
To start live preview, use following command:

```
mkdocs serve
```
