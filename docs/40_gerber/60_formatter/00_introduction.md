# Introduction

Welcome to the Gerber Formatter documentation. This documentation is intended to provide
a comprehensive overview of the Gerber Formatter including usage, options and examples.

!!! info

    Please note that this API is lower-level than one offered by the `GerberFile` object you
    can find [here](../20_quick_start/01_single_file.md). In many cases `GerberFile`
    interface will be more intuitive and easier to use, hence it is usually better to stick
    with it unless you have specific needs that are not covered by it.

## What is the Gerber Formatter?

The Gerber Formatter is a tool that can be used to format Gerber files. It can be used
to reformat Gerber files to make them more readable or the opposite, to compress them to
save precious disk space. Technically, formatter includes also minor code modernization
features although less powerful than the Optimizer.

## Why?

Gerber files are often used just as transfer format and rarely it is necessary to read
them directly. However, in those rare cases when you have to look into them, it would be
nice for them to be more readable than what your CAD software of choice happens to spit
out. This is where the Gerber Formatter comes in handy.

## How?

The Gerber Formatter can be used both as a command line tool and as a library. The
command line tool can be accessed via `pygerber gerber format` subcommand while library
API is available through `pygerber.gerber.formatter` module. Command line usage is
covered in [Gerber](../../25_command_line/20_gerber.md) command line documentation while
API usage and configuration options are covered in [API usage](./05_api_usage.md).
