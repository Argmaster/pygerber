# PyGerber

PyGerber is a Python implementation of GerberX3 format. It contains full parser, pretty
printer and rendering system. Currently all systems are under active development.

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
