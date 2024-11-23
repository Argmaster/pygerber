from pygerber.gerber.parser import parse
from pygerber.gerber.formatter import formats
from pygerber.examples import ExamplesEnum, load_example

gerber_source_code = load_example(ExamplesEnum.UCAMCO_2_11_2)

ast = parse(gerber_source_code)

print(formats(ast))
