from pygerber.gerber.api import GerberFile

from pygerber.examples import ExamplesEnum, load_example

gerber_source_code = load_example(ExamplesEnum.UCAMCO_2_11_2)

image = GerberFile.from_str(gerber_source_code).render_with_pillow()
image.get_image().save("output.png")
