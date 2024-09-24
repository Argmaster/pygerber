# Introduction

## Overview

This is a beginning of quick start guide for PyGerber. It uses a dedicated API which
exposes limited set of functionalities of PyGerber in very convenient way. It should
suite your needs if you are only looking for a quick way to render Gerber file(s) with
ability to choose basic options for parsing and rendering.

If you need to do something more complicated, you should check out **Advanced Guide** to
understand how PyGerber works and what can be achieved with its more complicated
interfaces.

## `pygerber.gerber.api` module

PyGerber exposes a simple API for accessing limited subset of its functionalities in
form of `pygerber.gerber.api` module. This interface is especially useful for one time
use, scripting and use from interactive shell.
