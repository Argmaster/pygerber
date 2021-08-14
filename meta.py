

from typing import Tuple


class Meta:

    coordinate_format: str
    unit: str
    current_point: Tuple[float, float]
    current_aperture: object
    interpolation: int
    polarity: int
    mirroring: bool
    rotation: float
    scaling: float