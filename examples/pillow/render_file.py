# -*- coding: utf-8 -*-
from pygerber.API2D import render_file

pillow_image = render_file("tests/gerber/s5.grb")
pillow_image.save("render.png")
