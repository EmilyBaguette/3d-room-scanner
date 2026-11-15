import pytest

from scanner.geometry.primitives import Point
from scanner.models.measurement import ScanMeasurement
from scanner.processing.point_cloud import measurements_to_points


def test_converts_measurements_to_world_points() -> None:
    measurements = [
        ScanMeasurement(yaw_deg=0, pitch_deg=0, distance_mm=2000),
        ScanMeasurement(yaw_deg=90, pitch_deg=0, distance_mm=1000),
        ScanMeasurement(yaw_deg=0, pitch_deg=90, distance_mm=500),
    ]

    points = list(measurements_to_points(measurements, Point(10, 20, 30)))

    expected = [(2010, 20, 30), (10, 1020, 30), (10, 20, 530)]
    assert len(points) == len(expected)
    for point, expected_coordinates in zip(points, expected, strict=True):
        assert (point.x, point.y, point.z) == pytest.approx(
            expected_coordinates, abs=1e-9
        )


def test_skips_measurements_without_distance() -> None:
    measurements = [
        ScanMeasurement(yaw_deg=0, pitch_deg=0, distance_mm=None),
        ScanMeasurement(yaw_deg=0, pitch_deg=0, distance_mm=1000),
    ]

    points = list(measurements_to_points(measurements, Point(0, 0, 0)))

    assert points == [Point(1000, 0, 0)]
