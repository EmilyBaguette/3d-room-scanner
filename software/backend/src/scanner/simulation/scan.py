from collections.abc import Iterable, Iterator

from scanner.geometry.primitives import Point
from scanner.models.measurement import ScanMeasurement
from scanner.simulation.laser import simulate_range
from scanner.simulation.scenes import create_alcove


def simulate_scan(
    yaw_range: Iterable[int], pitch_range: Iterable[int]
) -> Iterator[ScanMeasurement]:
    surfaces = create_alcove()
    origin = Point(0, 0, 1000)

    for pitch_deg in pitch_range:
        for yaw_deg in yaw_range:
            distance_mm = simulate_range(origin, yaw_deg, pitch_deg, surfaces)
            yield ScanMeasurement(
                yaw_deg=yaw_deg, pitch_deg=pitch_deg, distance_mm=distance_mm
            )
