import pytest

from scanner.geometry.primitives import Direction, Plane, Point, Surface
from scanner.simulation.laser import simulate_range


def wall_at_x(
    x: float, *, lower_y: float = -10, upper_y: float = 10
) -> Surface:
    return Surface(
        plane=Plane(Point(x, 0, 0), Direction(1, 0, 0)),
        lower=Point(x, lower_y, -10),
        upper=Point(x, upper_y, 10),
    )


def test_returns_nearest_surface_distance() -> None:
    surfaces = [wall_at_x(2000), wall_at_x(1000)]

    distance = simulate_range(Point(0, 0, 0), 0, 0, surfaces)

    assert distance == pytest.approx(1000)


def test_ignores_intersection_outside_surface_bounds() -> None:
    surfaces = [
        wall_at_x(1000, lower_y=100, upper_y=200),
        wall_at_x(2000),
    ]

    distance = simulate_range(Point(0, 0, 0), 0, 0, surfaces)

    assert distance == pytest.approx(2000)


def test_returns_none_when_every_surface_is_missed() -> None:
    surfaces = [wall_at_x(1000, lower_y=100, upper_y=200)]

    assert simulate_range(Point(0, 0, 0), 0, 0, surfaces) is None


def test_returns_none_without_surfaces() -> None:
    assert simulate_range(Point(0, 0, 0), 0, 0, []) is None
