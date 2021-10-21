# -*- coding: utf-8 -*-
from pygerber.API2D import render_from_spec

render_from_spec(
    {
        "dpi": 600,
        "image_padding": 0,
        "ignore_deprecated": True,
        "layers": [
            {
                "file_path": "tests/gerber/set/top_copper.grb",
                "colors": {
                    "dark": [40, 143, 40, 255],
                    "clear": [60, 181, 60, 255],
                },
            },
            {
                "file_path": "tests/gerber/set/top_solder_mask.grb",
                "colors": "solder_mask",
            },
            {"file_path": "tests/gerber/set/top_paste_mask.grb"},
            {
                "file_path": ".tests/gerber/set/top_silk.grb",
                "colors": "silk",
            },
        ],
    }
)
