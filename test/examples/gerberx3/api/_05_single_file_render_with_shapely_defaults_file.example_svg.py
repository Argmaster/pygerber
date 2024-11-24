from pygerber.gerber.api import GerberFile, Style

from pygerber.examples import ExamplesEnum, get_example_path

path_to_gerber_file = get_example_path(ExamplesEnum.UCAMCO_2_11_2)

image = GerberFile.from_file(path_to_gerber_file).render_with_shapely(
    Style.presets.BLACK_WHITE
)
image.save("output.svg")
