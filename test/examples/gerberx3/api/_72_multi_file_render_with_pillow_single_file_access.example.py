from pygerber.examples import ExamplesEnum, load_example
from pygerber.gerber.api import CompositeView, GerberFile


project = CompositeView(
    [
        GerberFile.from_str(load_example(ExamplesEnum.simple_2layer_F_Cu)),
        GerberFile.from_str(load_example(ExamplesEnum.simple_2layer_F_Mask)),
        GerberFile.from_str(load_example(ExamplesEnum.simple_2layer_F_Paste)),
        GerberFile.from_str(load_example(ExamplesEnum.simple_2layer_F_Silkscreen)),
    ],
)
image = project.render_with_pillow()
image.get_sub_images()[0].get_image().save("output.png")
