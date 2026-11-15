from collections.abc import Iterable, Iterator

from scanner.geometry.conversion import to_cartesian
from scanner.geometry.primitives import Point
from scanner.models.measurement import ScanMeasurement


def measurements_to_points(
    measurements: Iterable[ScanMeasurement], origin: Point
) -> Iterator[Point]:
    for measurement in measurements:
        if measurement.distance_mm is None:
            continue

        offset = to_cartesian(
            measurement.distance_mm,
            measurement.yaw_deg,
            measurement.pitch_deg,
        )
        yield Point(
            x=origin.x + offset.x,
            y=origin.y + offset.y,
            z=origin.z + offset.z,
        )
