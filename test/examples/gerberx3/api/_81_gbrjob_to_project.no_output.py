from pygerber.examples import ExamplesEnum, get_example_path
from pygerber.gerber.api._gerber_job_file import GerberJobFile


gerber_job = GerberJobFile.from_file(
    get_example_path(ExamplesEnum.carte_test_gbrjob),
)
project = gerber_job.to_project()

print("top:")
for file in project.top.files:
    print(f"  {file}")

for i, inner in enumerate(project.inner):
    print(f"inner {i}:")
    for file in inner.files:
        print(f"  {file}")

print("bottom:")
for file in project.bottom.files:
    print(f"  {file}")

project.bottom.render_with_pillow().get_image().save("output.png")
