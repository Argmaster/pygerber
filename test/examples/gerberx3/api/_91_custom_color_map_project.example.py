from pygerber.examples import ExamplesEnum, load_example
from pygerber.gerber.api import CompositeView, GerberFile, FileTypeEnum, Color, Style


my_color_map = {
    FileTypeEnum.COPPER: Style(
        background=Color.from_rgba(0, 0, 0, 0),
        foreground=Color.from_rgba(200, 20, 20, 255),
    ),
    FileTypeEnum.SOLDERMASK: Style(
        background=Color.from_rgba(0, 0, 0, 0),
        foreground=Color.from_rgba(117, 117, 117, 255),
    ),
    FileTypeEnum.PASTE: Style(
        background=Color.from_rgba(0, 0, 0, 0),
        foreground=Color.from_rgba(117, 117, 117, 255),
    ),
    FileTypeEnum.LEGEND: Style(
        background=Color.from_hex("#00000000"),
        foreground=Color.from_hex("#FFFFFFFF"),
    ),
}


project = CompositeView(
    [
        GerberFile.from_str(load_example(ExamplesEnum.simple_2layer_F_Cu)),
        GerberFile.from_str(load_example(ExamplesEnum.simple_2layer_F_Mask)),
        GerberFile.from_str(load_example(ExamplesEnum.simple_2layer_F_Paste)),
        GerberFile.from_str(load_example(ExamplesEnum.simple_2layer_F_Silkscreen)),
    ],
)
# Calling `set_color_map` on `CompositeView` will propagate the color map to all
# `GerberFile` objects inside it.
project.set_color_map(my_color_map)

image = project.render_with_pillow()
image.get_image().save("output.png")
