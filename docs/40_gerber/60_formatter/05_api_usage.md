# ☕ API usage

The Gerber Formatter can be used as a library. The main entry point is the
`pygerber.gerber.formatter` module.

## API

The basic usage of the Gerber Formatter is to utilize `format` and `formats` functions
available in `pygerber.gerber.formatter` module. Please have look at the following
example:

{{ include_code("test/examples/gerberx3/formatter/_10_basic_format.py", "docspygerberlexer", title="format_example.py", linenums="1") }}

Please note that to format the code, we first had to parse it, and only then could the
abstract syntax tree be passed to the formatter. `format` function writes formatted code
directly to file-like object, while `formats` function returns formatted code as a
string.

## Configuration

The formatter can be configured using `Options` object. The object can be passed to
`format` and `formats` functions as a optional `options` argument. You can find full
option reference [here](../../reference/pygerber/gerber/formatter/options.md).

{{ include_code("test/examples/gerberx3/formatter/_20_format_with_options.py", "docspygerberlexer", title="options_example.py", linenums="1") }}
