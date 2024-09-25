from pygerber.gerber.api import GerberFile
from pathlib import Path

with (Path().cwd() / "example.grb").open() as text_io:
    gerber_file = GerberFile.from_buffer(text_io)
