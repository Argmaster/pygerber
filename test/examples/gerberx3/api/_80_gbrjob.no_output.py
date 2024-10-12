from pygerber.examples import ExamplesEnum, get_example_path
from pygerber.gerber.api._gerber_job_file import GerberJobFile


gerber_job = GerberJobFile.from_file(
    get_example_path(ExamplesEnum.carte_test_gbrjob),
)
print(gerber_job.header.generation_software.vendor)
