# Setup

This project uses `Python` programming language and requires at least python `3.8` for
development and distribution. Development dependencies
[`poetry`](https://pypi.org/project/poetry/) for managing dependencies and distribution
building. It is necessary to perform any operations in development environment.

To install poetry globally (preferred way) use `pip` in terminal:

```
pip install poetry
```

Then use

```
poetry shell
```

to spawn new shell with virtual environment activated. Virtual environment will be
indicated by terminal prompt prefix `(pygerber-py3.8)`, version indicated in prefix
depends on used version of Python interpreter.

Within shell with active virtual environment use:

```
poetry install --sync
```

To install all dependencies. Every time you perform a `git pull` or change a branch, you
should call this command to make sure you have the correct versions of dependencies.

Afterwards you will have to also setup pre-commit hooks to avoid problems with code
quality during review. To do so, use:

```
poe install-hooks
```

Hooks will run automatically before every commit. If you want to run them manually, use:

```
poe run-code-quality-checks
```

To run unit test suite, use:

```
poe run-unit-tests
```
