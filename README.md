<p align="center">
   <img width="400" src="https://github.com/Argmaster/pygerber/assets/56170852/b7aeb3e1-cd59-4f5b-b078-c01272461367" alt="" />
</p>

<h1 align="center"> PyGerber </h1>

<p align="center">
  <a href="https://github.com/Argmaster/pygerber/releases/"><img src="https://img.shields.io/github/v/release/Argmaster/pygerber?style=flat" alt="GitHub release"></a>
  <a href="https://github.com/Argmaster/pygerber/releases"><img src="https://img.shields.io/github/release-date/Argmaster/pygerber" alt="GitHub Release Date - Published_At"></a>
  <a href="https://pypi.org/project/pygerber"><img src="https://img.shields.io/pypi/v/pygerber?style=flat" alt="PyPI release"></a>
  <a href="https://pypi.org/project/pygerber/"><img src="https://img.shields.io/pypi/dm/pygerber.svg?label=PyPI%20downloads" alt="PyPI Downloads"></a>
  <a href="https://pypi.org/project/pygerber"><img src="https://img.shields.io/pypi/pyversions/pygerber?style=flat" alt="Supported Python versions"></a>
  <a href="https://pypi.org/project/pygerber"><img src="https://img.shields.io/pypi/implementation/pygerber?style=flat" alt="Supported Python implementations"></a>
  <a href="https://github.com/argmaster/pygerber/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Argmaster/pygerber" alt="license_mit"></a>
  <a href="https://codecov.io/gh/Argmaster/pygerber"><img src="https://codecov.io/gh/Argmaster/pygerber/branch/main/graph/badge.svg?token=VM09IHO13U" alt="coverage"></a>
  <a href="https://img.shields.io/github/checks-status/Argmaster/pygerber/main"><img src="https://img.shields.io/github/checks-status/Argmaster/pygerber/main" alt="GitHub tag checks state"></a>
  <a href="https://github.com/Argmaster/pygerber/pulls"><img src="https://img.shields.io/github/issues-pr/Argmaster/pygerber?style=flat" alt="Pull requests"></a>
  <a href="https://github.com/Argmaster/pygerber/issues"><img src="https://img.shields.io/github/issues-raw/Argmaster/pygerber?style=flat" alt="Open issues"></a>
  <a href="https://github.com/Argmaster/pygerber"><img src="https://img.shields.io/github/repo-size/Argmaster/pygerber" alt="GitHub repo size"></a>
  <a href="https://github.com/Argmaster/pygerber"><img src="https://img.shields.io/github/languages/code-size/Argmaster/pygerber" alt="GitHub code size in bytes"></a>
  <a href="https://github.com/Argmaster/pygerber"><img src="https://img.shields.io/github/stars/Argmaster/pygerber" alt="GitHub Repo stars"></a>
  <a href="https://python-poetry.org/"><img src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" alt="Poetry"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style"></a>
</p>

## 📖 Overview

PyGerber is a collection of tools that simplify working with the Gerber X3 format in
Python. It is based on Ucamco's `The Gerber Layer Format Specification, Revision 2024.05`
(available on
[Ucamco's website](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf)).

PyGerber can be used both as an executable (via a command-line interface) and as a
Python library.

PyGerber supports modern features from the latest version of the standard (2024.05).
At the same time, it implements many older and removed functionalities for backwards
compatibility. This makes it usable with files compliant with X3 as well as with X2,
RS-274X, and RS-274D. Because access to files in older standards is limited and those
standards contain ambiguities, some legacy behaviors may be incorrect.

If you find a bug in the PyGerber library, please file a bug report using one of the
issue templates available on the [Create new issue](https://github.com/Argmaster/pygerber/issues/new/choose)
page in the PyGerber repository. We will examine reports and fix issues when possible.

If you have questions or suggestions, please open a discussion in the
[Discussions](https://github.com/Argmaster/pygerber/discussions) section of the
repository.

### 📦 Installation

Install PyGerber from PyPI with `pip`:

```
pip install pygerber
```

This installs the core features only. The language server, SVG rendering support,
and other optional features are available via extras. To install all extras use:

```
pip install pygerber[all]
```

To install the latest development version, use the GitHub repository URL with the
`git+` prefix:

```
pip install git+https://github.com/Argmaster/pygerber
```

## 📚 Documentation

PyGerber has online documentation hosted on GitHub Pages. It's a great starting point
for using PyGerber: [PyGerber documentation](https://argmaster.github.io/pygerber/stable).
For documentation of older versions, use the version selector next to the title in
the top bar.

### 📜 License

PyGerber is licensed under the MIT License. The full text is available in the
[LICENSE](https://github.com/Argmaster/pygerber/blob/main/LICENSE.md) file at the
root of the repository.

Some testing assets and example files are distributed under different licenses; their
license files are provided alongside the assets. For example, some files from KiCad
demo projects are licensed under `CC BY-SA 4.0`.

## 🛠 Tools

The collection of tools available in PyGerber constantly grows. Some tools are
exposed via the API, others include a command-line interface. Below is a list of
currently available tools:

- Image renderer (PNG/JPEG/SVG) `[API]` `[CLI]`
- Code formatter `[API]` `[CLI]`
- Gerber code generation `[API]`
- Language server (requires `language_server` extras)
  ([Visual Studio Code extension available](https://marketplace.visualstudio.com/items?itemName=argmaster.gerber-x3-x2-format-support))
  `[CLI]`
- Pygments Gerber syntax lexer plugin (requires `pygments` extras) `[CLI]`

### 🖮 PyGerber APIs

PyGerber provides APIs for accessing most of its functionality. The modules listed
below are intended for use as stable library APIs; they re-export public parts of the
implementation in a convenient way. Avoid importing from modules not listed here or
not documented, as those modules are not part of public APIs and may be changed or
removed at any time.

Below you can find a list of available APIs:

- `pygerber.gerber.api`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=bug%2Cwaiting-for-checkboxes&projects=&template=pygerber_generic_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.gerber.ast`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=bug%2Cwaiting-for-checkboxes&projects=&template=pygerber_generic_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.gerber.ast.nodes`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=bug%2Cwaiting-for-checkboxes&projects=&template=pygerber_generic_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.gerber.compiler`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=bug%2Cwaiting-for-checkboxes&projects=&template=pygerber_generic_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.gerber.parser`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=bug%2Cwaiting-for-checkboxes&projects=&template=pygerber_generic_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.gerber.formatter`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=gerber-formatter%2Cbug%2Cwaiting-for-checkboxes&projects=&template=gerber_formatter_bug.md&title=%5BGerber+Formatter%5D%3A+%3Cincorrect-formatting-of-such-and-such-structure%3E))
- `pygerber.builder.gerber`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=gerber-builder%2Cbug%2Cwaiting-for-checkboxes&projects=&template=builder_gerber.md&title=%5BGerber+Builder%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.builder.rvmc`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=gerber-formatter%2Cbug%2Cwaiting-for-checkboxes&projects=&template=gerber_formatter_bug.md&title=%5BGerber+Formatter%5D%3A+%3Cincorrect-formatting-of-such-and-such-structure%3E))
- `pygerber.vm`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=virtual-machine%2Cbug%2Cwaiting-for-checkboxes&projects=&template=pygerber_vm_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.vm.commands`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=virtual-machine%2Cbug%2Cwaiting-for-checkboxes&projects=&template=pygerber_vm_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.vm.types`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=virtual-machine%2Cbug%2Cwaiting-for-checkboxes&projects=&template=pygerber_vm_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.vm.pillow`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=virtual-machine%2Cbug%2Cwaiting-for-checkboxes&projects=&template=pygerber_vm_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))
- `pygerber.vm.shapely`
  ([open issue](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=virtual-machine%2Cbug%2Cwaiting-for-checkboxes&projects=&template=pygerber_vm_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E))

If you need a symbol that is not re-exported from these modules (for example, an
exception class you need to catch), please open an issue using the corresponding
"open issue" link so we can evaluate adding the missing re-export. If the provided
template doesn't match your case, fill the fields according to the template
guidelines and we will sort it out.

If you have found a bug in a particular part of PyGerber, please use the `open issue`
link next to the module name above to open an issue submission form. Alternatively,
choose one of the issue templates on the
[Create new issue](https://github.com/Argmaster/pygerber/issues/new/choose) page in
the PyGerber repository and follow the template guidelines to simplify reproducing
the issue for maintainers. If there is no dedicated template, use the
[PyGerber Bug Report](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=bug%2Cwaiting-for-checkboxes&projects=&template=pygerber_generic_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E)
template.

### 💻 PyGerber CLI

PyGerber provides a non-interactive command-line interface to access its tools. The
`pygerber` command is available after installation and exposes functionality via
subcommands.

To check the installed version, run:

```bash
pygerber --version
```

To convert a Gerber file to PNG, use the `pygerber gerber convert png` command. For
example, following command converts `source.gbr` (a copper layer) to a PNG at 600 DPMM
resolution:

```bash
pygerber gerber convert png source.gbr -o output.png -d 600 -s copper_alpha
```

This creates `output.png` in the current working directory. Depending on your image
size you may need to adjust `-d` (`--dpmm`) to increase or decrease the resolution.
Be careful with the resoultion, as choosing too low value may result in image being
empty.

Here is an example result of converting a Gerber file to PNG image:

![output](https://github.com/user-attachments/assets/0dfc4682-a284-4cb0-8a74-81136e213766)

There are more export target formats available, like JPEG, TIFF, or SVG. Use the
`--help` flag to list available conversion commands:

```bash
pygerber gerber convert --help
```

For more detailed command-line documentation, see the `Gerber` → `Command Line`
section in the [documentation](https://argmaster.github.io/pygerber/stable/).

## § Language Server

PyGerber provides a Gerber X3/X2 Language Server conforming to the
[Language Server Protocol](https://microsoft.github.io/language-server-protocol/).
To enable it, install the `language-server` extras:

```
pip install pygerber[language-server]
```

To check if the language server is available, run the following command:

```
pygerber is-language-server-available
```

If you encounter a problem with the language server, please report it using the
[Issues](https://github.com/Argmaster/pygerber/issues/new/choose) page of the
PyGerber repository.

To fully utilize the language server, use the Visual Studio Code extension
[Gerber X3/X2 Format Support](https://marketplace.visualstudio.com/items?itemName=argmaster.gerber-x3-x2-format-support)
(`argmaster.gerber-x3-x2-format-support`). The extension repository is available
[here](https://github.com/Argmaster/vscode-gerber-format-support). If you encounter
problems with the extension, report them on the extension's Issues page; if the
problem is caused by the language server we will move the report to the PyGerber
repository as needed.

## Development

For development guidelines please visit the documentation `Development` section
[here](https://argmaster.github.io/pygerber/stable).

## Acknowledgments

I would like to thank Professor Janusz Młodzianowski from the University of Gdańsk,
who inspired me with the idea to implement the Gerber format at the beginning of my
bachelor's degree. I would also like to express my gratitude to Karel Tavernier, the
long-time steward of the Gerber format, for his support and expert guidance during my
work on this project. Without them, this project would not have come to life. Finally,
I would like to thank all the people who have contributed, are contributing, and will
contribute to PyGerber. Your help is invaluable and I am grateful for it.
