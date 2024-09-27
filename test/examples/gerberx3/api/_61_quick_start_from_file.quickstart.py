from pygerber.gerber.api import GerberFile
from pathlib import Path

path_to_my_gerber_file = Path().cwd() / "example.grb"

gerber_file = GerberFile.from_file(path_to_my_gerber_file)
