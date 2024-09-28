from pygerber.examples import ExamplesEnum, load_example
from pygerber.gerber.api import Project, GerberFile, FileTypeEnum


project = Project(
    [
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Cu),
            FileTypeEnum.COPPER,
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Mask),
            FileTypeEnum.MASK,
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Paste),
            FileTypeEnum.PASTE,
        ),
        GerberFile.from_str(
            load_example(ExamplesEnum.simple_2layer_F_Silkscreen),
            FileTypeEnum.SILK,
        ),
    ],
)
print(project)
