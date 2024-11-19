# Environment setup

## Development virtual environment

This project uses `Python` programming language and requires at least python `3.8` in
development and production environment to function. During development, PyGerber relies
on [poetr](https://pypi.org/project/poetry/) for dependency management, creation of
development virtual environment and packaging. To work on PyGerber, you will need to
install poetry on your system. You can find official poetry installation guidelines
[here](https://python-poetry.org/docs/#installation). We recommend installing poetry
globally, unless on linux distribution, in such case distribution native approach should
be taken, usually with distribution specific package manager.

To install poetry globally you can use `pip` (or any other PyPI compatible package
manager) in terminal:

```
pip install poetry
```

!!! warning

    Make sure you are installing latest version of poetry, or at least `>=1.8` as in the
    past poetry had minor issues with stability during installation of dependencies.

After installing poetry, if you haven't already, clone the repository with

```
git clone https://github.com/Argmaster/pygerber
```

and navigate to project root directory. Once there, use:

```
poetry shell
```

to create a development virtual environment and enter a shell with virtual environment
activated. Virtual environment will be indicated by terminal prompt prefix
`(pygerber-pyX.Y)`, (where `X.Y` is python version).

Afterwards you can start process of installation of development dependencies. Use:

```
poetry install --sync --extras=all --with=docs,style
```

To install all dependencies, including optional ones. Every time you perform a
`git pull` or change a branch, you should run this command again to make sure you have
the correct versions of dependencies.

## Git hooks

PyGerber project uses [pre-commit](https://pypi.org/project/pre-commit/) to run git
hooks to ensure high quality of code committed to the repository. You can skip
installation of hooks if you want, but you will still have to meet their requirements
after they are run by CI/CD pipeline. Preferably, you should install them locally and
keep an eye on their status:

```
poe install-hooks
```

!!! warning

    Don't confuse `poe` with `poetry`, `poe` is a command line tool for running simple
    sequences of commands while `poetry` is a package manager and virtual environment
    manager.

You can check if your hooks were setup correctly by running:

```
poe test-style
```

Here is reference output of `poe test-style`:

> ```
> Poe => poetry run pre-commit run --all-files -v
> prettier.................................................................Passed
> - hook id: prettier
> - duration: 0.83s
> check illegal windows names..........................(no files to check)Skipped
> - hook id: check-illegal-windows-names
> check for case conflicts.................................................Passed
> - hook id: check-case-conflict
> - duration: 0.5s
> check for merge conflicts................................................Passed
> - hook id: check-merge-conflict
> - duration: 0.38s
> check for case conflicts.................................................Passed
> - hook id: check-case-conflict
> - duration: 0.48s
> trim trailing whitespace.................................................Passed
> - hook id: trailing-whitespace
> - duration: 0.23s
> debug statements (python)................................................Passed
> - hook id: debug-statements
> - duration: 0.23s
> fix end of files.........................................................Passed
> - hook id: end-of-file-fixer
> - duration: 0.2s
> fix utf-8 byte order marker..............................................Passed
> - hook id: fix-byte-order-marker
> - duration: 0.22s
> check for added large files..............................................Passed
> - hook id: check-added-large-files
> - duration: 0.52s
> check toml...............................................................Passed
> - hook id: check-toml
> - duration: 0.09s
> mixed line ending........................................................Passed
> - hook id: mixed-line-ending
> - duration: 0.22s
> trim trailing whitespace.................................................Passed
> - hook id: trailing-whitespace
> - duration: 0.22s
> debug statements (python)................................................Passed
> - hook id: debug-statements
> - duration: 0.22s
> ruff.....................................................................Passed
> - hook id: ruff
> - duration: 0.11s
>
> All checks passed!
>
> ruff-format..............................................................Passed
> - hook id: ruff-format
> - duration: 0.11s
>
> 284 files left unchanged
>
> mypy.....................................................................Passed
> - hook id: mypy
> - duration: 15.95s
>
> Poe => poetry run mypy --config-file=pyproject.toml src/pygerber/ test/
> Success: no issues found in 279 source files
> ```
