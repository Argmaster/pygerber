from pygerber.gerberx3.api import GerberFile, Project

from pygerber.examples import ExamplesEnum, load_example

gerber_source_code = load_example(ExamplesEnum.UCAMCO_2_11_2)

project = Project(
    [
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Cu),
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Mask),
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Paste),
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Silkscreen),
        ),
    ],
)
image = project.render_with_pillow(dpmm=40)
image.get_image().save("output.png")
