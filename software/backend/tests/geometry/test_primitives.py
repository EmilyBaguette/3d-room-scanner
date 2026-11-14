import pytest

from scanner.geometry.primitives import (
    BOUNDARY_TOLERANCE_MM,
    Direction,
    Plane,
    Point,
    Surface,
)


@pytest.fixture
def surface() -> Surface:
    return Surface(
        plane=Plane(Point(0, 0, 0), Direction(1, 0, 0)),
        lower=Point(0, 0, 0),
        upper=Point(0, 10, 20),
    )


@pytest.mark.parametrize(
    "point",
    [Point(0, 5, 10), Point(0, 0, 0), Point(0, 10, 20)],
    ids=["inside", "lower-edge", "upper-edge"],
)
def test_surface_contains_points_within_bounds(
    surface: Surface, point: Point
) -> None:
    assert surface.contains(point)


@pytest.mark.parametrize(
    "point",
    [Point(0, -1, 10), Point(0, 11, 10), Point(0, 5, 21)],
    ids=["below-lower-bound", "above-y-bound", "above-z-bound"],
)
def test_surface_rejects_points_outside_bounds(
    surface: Surface, point: Point
) -> None:
    assert not surface.contains(point)


def test_surface_allows_rounding_error_at_boundary(surface: Surface) -> None:
    point = Point(0, -BOUNDARY_TOLERANCE_MM, 20 + BOUNDARY_TOLERANCE_MM)

    assert surface.contains(point)


def test_surface_rejects_point_beyond_boundary_tolerance(surface: Surface) -> None:
    point = Point(0, -(2 * BOUNDARY_TOLERANCE_MM), 10)

    assert not surface.contains(point)
