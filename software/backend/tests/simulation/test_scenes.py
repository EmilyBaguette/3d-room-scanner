from math import cos, radians

import pytest

from scanner.geometry.primitives import Point
from scanner.simulation.laser import simulate_range
from scanner.simulation.scenes import create_alcove


@pytest.mark.parametrize(
    ("yaw_deg", "pitch_deg", "expected_distance"),
    [
        pytest.param(0, 0, 2300, id="alcove-back"),
        pytest.param(30, 0, 2000 / cos(radians(30)), id="main-wall-right"),
        pytest.param(0, 30, 2000 / cos(radians(30)), id="main-wall-above"),
    ],
)
def test_known_alcove_measurements(
    yaw_deg: float, pitch_deg: float, expected_distance: float
) -> None:
    distance = simulate_range(
        Point(0, 0, 1000), yaw_deg, pitch_deg, create_alcove()
    )

    assert distance == pytest.approx(expected_distance)


def test_alcove_scan_can_miss_every_surface() -> None:
    distance = simulate_range(Point(0, 0, 1000), 0, -30, create_alcove())

    assert distance is None
