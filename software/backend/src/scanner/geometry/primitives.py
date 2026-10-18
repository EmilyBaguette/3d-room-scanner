from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    """A 3D point in millimetres."""

    x: float
    y: float
    z: float
