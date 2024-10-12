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

PyGerber is a collection of tools aimed at simplifying the use of the Gerber X3 format.
It is based on Ucamco's `The Gerber Layer Format Specification. Revision 2024.05`
(Available on
[Ucamco's webpage](https://www.ucamco.com/files/downloads/file_en/456/gerber-layer-format-specification-revision-2024-05_en.pdf).

PyGerber can be used both as a executable (with command line interface) and as a Python
library.

PyGerber supports modern features available in the latest version of the standard
(2024.05). At the same time, it includes the implementation of many of outdated and
removed functionalities for backwards compatibility. This allows it to be used not only
with files compliant with the X3 standard but also with those compliant with X2,
RS-274X, and RS-274D. Due to limited access to files in older standards and ambiguities
within them, there is a risk that some older functionalities may behave incorrectly.

If you have found a bug in the PyGerber library, please file a bug report with use of
one of issue templates available on
[Create new issue](https://github.com/Argmaster/pygerber/issues/new/choose) page in
PyGerber repository. We will be glad to examine your report and possibly fix the
problem.

If you have any questions or suggestions, please open a new discussion thread in the
[Discussions](https://github.com/Argmaster/pygerber/discussions) section of our
repository. We will be happy to help you and discuss your ideas.

### 📦 Installation

PyGerber can be installed with `pip` from PyPI:

```
pip install pygerber
```

This way only the core of PyGerber features will be installed. It will not include
language server, SVG rendering support and other optional features. If you want to
install all available features, include `all` extras set in installation request, like
this:

```
pip install pygerber[all]
```

To install latest development version of PyGerber, you can use URL of the Github
repository with `git+` prefix:

```
pip install git+https://github.com/Argmaster/pygerber
```

## 📚 Documentation

PyGerber has a online documentation hosted on Github Pages. It will be a great starting
point for your journey with PyGerber.
[You can it here](https://argmaster.github.io/pygerber/latest). If you are looking for
documentation of older version of PyGerber, please use version selector dropdown
available next to the title in top bar menu.

### 📜 License

PyGerber is licensed under MIT license. You can find full text of the license in the
[LICENSE](https://github.com/Argmaster/pygerber/blob/main/LICENSE.md) file in the root
directory of the repository.

Some of the testing assets may be licensed under different licenses. License files for
those assets are available alongside those files.

Some of the example files shipped with PyGerber may be licensed under different
licenses. In particular, files from KiCad demo projects are licensed under
`CC BY-SA 4.0` license. Copy of the license file is provided alongside those files.

## 🛠 Tools

Collection of tools available in PyGerber constantly grows. Some of the tools can be
accessed only with API, others provide command line interface too. Below you can find
list of all currently available ones:

- Image renderer (PNG/JPEG) `[API]` `[CLI]`
- Code formatter `[API]` `[CLI]`
- Code generation `[API]`
- Language server (requires `language_server` extras)
  ([Visual Studio Code extension available](https://marketplace.visualstudio.com/items?itemName=argmaster.gerber-x3-x2-format-support))
  `[CLI]`
- Pygments Gerber syntax lexer plugin (requires `pygments` extras) `[CLI]`

### 🖮 PyGerber APIs

PyGerber provides APIs for accessing most of its functionalities. There are selected
modules designed to be used as libraries, they reexport public parts of implementation
in a convenient way. Avoid importing stuff from modules not listed below and not
mentioned in documentation, as this may inflict suffering and damnation upon you 💀
(Just joking, but they may get deleted/moved at any time, so you know 😼).

Below you can find list of available APIs:

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

If you need a symbol that is not reexported from those modules, eg. some exception class
you need to catch, please open an issue with corresponding `open issue` link so we can
evaluate that issue and possibly add missing reexport. Don't worry about template being
for bugs, we will figure that out in the process, just fill the fields in template
according to guidelines contained in it.

If you have found a bug in a particular part of PyGerber, please use `open issue` link
next to module name above to open issue submission form. Alternatively you can choose
one of the issue templates on
[Create new issue](https://github.com/Argmaster/pygerber/issues/new/choose) page in
PyGerber repository. Please fill the template according to guidelines contained in it to
simplify process of reproducing the issue for maintainers. If there is no dedicated
template, use
[PyGerber Bug Report](https://github.com/Argmaster/pygerber/issues/new?assignees=Argmaster&labels=bug%2Cwaiting-for-checkboxes&projects=&template=pygerber_generic_bug.md&title=%5BPyGerber%5D%3A+%3Cwhen-i-am-doing-something-then-something-fails%3E)
template.

### 💻 PyGerber CLI

PyGerber provides non-interactive command line interface which provides means to access
some of its features. `pygerber` command is available after installation and can be used
to access tools with use of subcommands.

To check version of PyGerber available in your environment, you can use:

```bash
pygerber --version
```

To access PyGerbers image rendering feature, you can use `render` subcommand. Assuming
that your Gerber file is named `source.gbr` and you want to render a PNG image of it,
you can use following command:

```bash
pygerber render raster source.gbr -o output.png
```

This will create `output.png` file in current working directory. Depending on your image
size you may need to adjust `--dpmm` parameter to raise or lower the resolution of
image.

![example_pcb_image](https://github.com/Argmaster/pygerber/assets/56170852/9bca28bf-8aa6-4215-aac1-62c386490485)

PyGerber has also a lot more options related to rendering available. For extensible
guide on how to use PyGerber CLI, please refer to documentation.

## § Language Server

PyGerber provides Gerber X3/X2 Language Server conforming to
[Language Servere Protocol](https://microsoft.github.io/language-server-protocol/)
defined by Microsoft. It can be enabled by installing PyGerber extras set
`language-server` with following command:

```
pip install pygerber[language-server]
```

Afterwards you can use following command to check if PyGerber correctly recognized that
language server feature should be enabled:

```
pygerber is-language-server-available
```

If you have encountered a problem with language server please report it in the
[Issues](https://github.com/Argmaster/pygerber/issues/new/choose) section of Github
repository of this project.

If you have a suggestion for improvement, please open a new discussion thread in the
[Discussions](https://github.com/Agrmaster/pygerber/discussions) section of our
repository.

To fully utilize power of this language server you can use Visual Studio Code extension
[Gerber X3/X2 Format Support](https://marketplace.visualstudio.com/items?itemName=argmaster.gerber-x3-x2-format-support)
(`argmaster.gerber-x3-x2-format-support`). Repository of this extension is available
[here](https://github.com/Argmaster/vscode-gerber-format-support). If you encounter any
problems with that extension, please report them in the
[Issues](https://github.com/Argmaster/vscode-gerber-format-support/issues/new) section
of its repository. If you are not sure whether the problem is caused by extension or by
language server, please report it in the
[Issues](https://github.com/Argmaster/vscode-gerber-format-support/issues/new) section
of the extension, we will move it to PyGerber repository if necessary.

## Development

For development guidelines please visit documentation `Development` section
[here](https://argmaster.github.io/pygerber/latest).

## Acknowledgments

I would like to thank Professor Janusz Młodzianowski from the University of Gdańsk, who
inspired me with the idea to implement the Gerber format at the beginning of my
bachelor's degree. I would like to also express my gratitude to Karel Tavernier, the
long-time steward of the Gerber format, for his support and expert guidance during my
work on this project. Without them, this project would have never come to life. Finally,
I would like to thank all the people who have contributed, are contributing and will
contribute to PyGerber. Your help is invaluable and I am grateful for it.
