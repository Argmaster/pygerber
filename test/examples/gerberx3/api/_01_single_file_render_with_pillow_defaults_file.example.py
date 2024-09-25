from pygerber.gerber.api import GerberFile

from pygerber.examples import ExamplesEnum, get_example_path

path_to_gerber_file = get_example_path(ExamplesEnum.UCAMCO_2_11_2)

image = GerberFile.from_file(path_to_gerber_file).render_with_pillow()
image.get_image().save("output.png")
