from math import sqrt

import pytest

from scanner.geometry.conversion import to_cartesian
from scanner.geometry.primitives import Point


@pytest.mark.parametrize(
    ("yaw_deg", "pitch_deg", "expected"),
    [
        pytest.param(0, 0, (1000, 0, 0), id="positive-x"),
        pytest.param(90, 0, (0, 1000, 0), id="positive-y"),
        pytest.param(180, 0, (-1000, 0, 0), id="negative-x"),
        pytest.param(-90, 0, (0, -1000, 0), id="negative-y"),
        pytest.param(0, 90, (0, 0, 1000), id="positive-z"),
        pytest.param(0, -90, (0, 0, -1000), id="negative-z"),
    ],
)
def test_axis_directions(
    yaw_deg: float, pitch_deg: float, expected: tuple[float, float, float]
) -> None:
    point = to_cartesian(1000, yaw_deg, pitch_deg)

    assert isinstance(point, Point)
    assert (point.x, point.y, point.z) == pytest.approx(expected, abs=1e-9)


def test_combined_yaw_and_pitch() -> None:
    point = to_cartesian(1000, 45, 30)

    # Horizontal projection is 500 * sqrt(3); yaw splits it equally into X/Y.
    assert (point.x, point.y, point.z) == pytest.approx(
        (250 * sqrt(6), 250 * sqrt(6), 500)
    )


@pytest.mark.parametrize(("yaw_deg", "pitch_deg"), [(0, 0), (123, -37), (-90, 90)])
def test_zero_range_returns_origin(yaw_deg: float, pitch_deg: float) -> None:
    point = to_cartesian(0, yaw_deg, pitch_deg)

    assert (point.x, point.y, point.z) == (0, 0, 0)


@pytest.mark.parametrize("yaw_deg", [-270, 450, 810])
def test_yaw_wraps_after_full_turns(yaw_deg: float) -> None:
    point = to_cartesian(1000, yaw_deg, 0)

    assert (point.x, point.y, point.z) == pytest.approx((0, 1000, 0), abs=1e-9)


@pytest.mark.parametrize("yaw_deg", [-123, 45, 270])
def test_vertical_direction_is_independent_of_yaw(yaw_deg: float) -> None:
    point = to_cartesian(1000, yaw_deg, 90)

    assert (point.x, point.y, point.z) == pytest.approx((0, 0, 1000), abs=1e-9)


@pytest.mark.parametrize(
    ("range_mm", "yaw_deg", "pitch_deg"),
    [(0.5, 12, -34), (1234.5, -137, 61), (10000, 225, -15)],
)
def test_distance_from_origin_is_preserved(
    range_mm: float, yaw_deg: float, pitch_deg: float
) -> None:
    point = to_cartesian(range_mm, yaw_deg, pitch_deg)

    distance = sqrt(point.x**2 + point.y**2 + point.z**2)
    assert distance == pytest.approx(range_mm)
