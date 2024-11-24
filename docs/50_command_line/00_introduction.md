# Introduction

Welcome to the PyGerber command line interface documentation. This documentation is
intended to guide you through the usage of the command line interface of PyGerber.

PyGerber command line can be accessed via `pygerber` command:

```bash
pygerber --version
```

Alternatively, executing PyGerber package as main module will yield the same result:

```bash
python -m pygerber --version
```

Only root package supports direct execution. Features of subpackages, eg. formatter can
be accessed by subcommands:

```bash
pygerber gerber format --help
```

But they don't support direct execution as main module.
