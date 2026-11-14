from dataclasses import dataclass

BOUNDARY_TOLERANCE_MM = 1e-6


@dataclass(frozen=True)
class Point:
    """A 3D point in millimetres."""

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Direction:
    """A 3D vector without units."""

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Ray:
    """A half-line starting at origin and extending along direction."""

    origin: Point
    direction: Direction


@dataclass(frozen=True)
class Plane:
    """An infinite plane through point, perpendicular to normal."""

    point: Point
    normal: Direction


@dataclass(frozen=True)
class Surface:
    """A constrained plane using a lower and upper point"""

    plane: Plane
    lower: Point
    upper: Point

    def contains(self, point: Point) -> bool:
        return all(
            low - BOUNDARY_TOLERANCE_MM <= value <= high + BOUNDARY_TOLERANCE_MM
            for low, value, high in (
                (self.lower.x, point.x, self.upper.x),
                (self.lower.y, point.y, self.upper.y),
                (self.lower.z, point.z, self.upper.z),
            )
        )
