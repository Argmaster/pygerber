from pathlib import Path
from pygerber.gerber.parser import parse
from pygerber.gerber.formatter import format, Options, MacroSplitMode
from pygerber.examples import ExamplesEnum, load_example

gerber_source_code = load_example(ExamplesEnum.UCAMCO_2_11_2)

ast = parse(gerber_source_code)

with Path("output.formatted.gbr").open("w") as output:
    format(
        ast,
        output,
        options=Options(
            indent_character="\t",
            macro_split_mode=MacroSplitMode.NoSplit,
        ),
    )
