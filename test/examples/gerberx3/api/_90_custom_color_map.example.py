from pygerber.gerber.api import GerberFile

from pygerber.examples import ExamplesEnum, load_example
from pygerber.gerber.api import FileTypeEnum, Color, Style


# Define a custom color map as a dictionary. We dont have to map all file types, only
# the ones we need. There is no fallback mechanism though, so if you miss a file type
# that you need during rendering, KeyError will be raised.
my_color_map = {
    FileTypeEnum.COPPER: Style(
        background=Color.from_rgba(0, 0, 0, 255),
        foreground=Color.from_rgba(200, 20, 20, 255),
    ),
    FileTypeEnum.MASK: Style(
        background=Color.from_rgba(0, 0, 0, 255),
        foreground=Color.from_rgba(117, 117, 117, 255),
    ),
    FileTypeEnum.PASTE: Style(
        background=Color.from_rgba(0, 0, 0, 255),
        foreground=Color.from_rgba(117, 117, 117, 255),
    ),
    FileTypeEnum.SILK: Style(
        background=Color.from_hex("#000000"),
        foreground=Color.from_hex("#FFFFFF"),
    ),
}

gerber_source_code = load_example(ExamplesEnum.carte_test_F_Cu)

file = GerberFile.from_str(gerber_source_code)
# Set the custom color map with the set_color_map method. If you don't do that,
# nothing will change.
file.set_color_map(my_color_map)

image = file.render_with_pillow()
image.get_image().save("output.png")
