from math import cos, radians, sin

from scanner.geometry.primitives import Point


def to_cartesian(range_mm: float, yaw_deg: float, pitch_deg: float) -> Point:
    """Convert spherical coordinates to Cartesian coordinates.

    Args:
        range_mm: Distance from the origin in millimetres.
        yaw_deg: Angle from +X towards +Y, in degrees.
        pitch_deg: Elevation from horizontal towards +Z, in degrees.

    Returns:
        Point in Cartesian coordinates.
    """
    yaw_rads = radians(yaw_deg)
    pitch_rads = radians(pitch_deg)

    horizontal = range_mm * cos(pitch_rads)

    return Point(
        x=horizontal * cos(yaw_rads),
        y=horizontal * sin(yaw_rads),
        z=range_mm * sin(pitch_rads),
    )
