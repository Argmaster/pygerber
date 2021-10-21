# -*- coding: utf-8 -*-
from pygerber.API3D import render_from_spec

render_from_spec(
    {
        "ignore_deprecated": True,
        "layers": [
            {
                "file_path": "./tests/gerber/set/top_copper.grb",
                "structure": {
                    "material": {
                        "color": [40, 143, 40, 255],
                        "metallic": 1.0,
                        "roughness": 0.8,
                    },
                    "thickness": 0.78,
                },
            },
            {
                "file_path": "./tests/gerber/set/top_solder_mask.grb",
                "structure": "solder_mask",
            },
            {"file_path": "./tests/gerber/set/top_paste_mask.grb"},
            {
                "file_path": "./tests/gerber/set/top_silk.grb",
                "structure": "silk",
            },
        ],
    }
)
