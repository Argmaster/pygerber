from pygerber.gerberx3.api import GerberFile

from pygerber.examples import ExamplesEnum, load_example

gerber_source_code = load_example(ExamplesEnum.UCAMCO_2_11_2)

image = (
    GerberFile.from_str(gerber_source_code)
    .set_parser_options(parser="pyparsing")
    .set_compiler_options(ignore_program_stop=False)
    .render_with_pillow()
)
info = image.get_image_space()
# 42.55 42.55 851 20 Units.Millimeters
print(info.max_x, info.max_x_mm, info.max_x_pixels, info.dpmm, info.units)

image.get_image().save("output.png")
