# 🧭 Introduction

## Overview

Welcome to the documentation of the code generation feature of PyGerber library!
Considering that to develop PyGerber core functionality of parsing Gerber files it was
necessary to design a lot of tools to verify the correctness of the implementation, it
became apparent that is will be much easier to compliment existing tool set with a code
generation tools rather than develop separate package for that purpose. Therefore, the
decision was made to develop a code generation feature as a part of PyGerber library.

Currently, there are two code generation APIs, one for generation of Gerber code and the
second one for generation of RVMC code (internal geometry representation used by
PyGerber). Those APIs are available in the `pygerber.builder.gerber` and
`pygerber.builder.rvmc` respectively.
