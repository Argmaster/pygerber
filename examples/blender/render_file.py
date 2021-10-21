# -*- coding: utf-8 -*-
from PyR3.shortcut.io import export_to

from pygerber.API3D import render_file

render_file("tests/gerber/s5.grb")
export_to("render.glb")
