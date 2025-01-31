from pygerber.gerber.api import GerberFile

from pygerber.examples import ExamplesEnum, load_example
from pygerber.gerber.api import FileTypeEnum, Color, Style, DEFAULT_ALPHA_COLOR_MAP


# We can copy DEFAULT_ALPHA_COLOR_MAP and update it with our custom values to avoid
# missing any file type. The ones we don't override will keep the default values.
my_color_map = DEFAULT_ALPHA_COLOR_MAP.copy()
my_color_map.update(
    {
        FileTypeEnum.COPPER: Style(
            background=Color.from_rgba(0, 0, 0, 255),
            foreground=Color.from_rgba(20, 20, 200, 255),
        ),
    }
)

gerber_source_code = load_example(ExamplesEnum.carte_test_F_Cu)

file = GerberFile.from_str(gerber_source_code)
file.set_color_map(my_color_map)

image = file.render_with_pillow()
image.get_image().save("output.png")
