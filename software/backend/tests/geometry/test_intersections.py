from math import hypot, sqrt

import pytest

from scanner.geometry.intersections import calculate_ray_plane_distance
from scanner.geometry.primitives import Direction, Plane, Point, Ray


@pytest.mark.parametrize(
    ("ray", "plane", "expected_distance"),
    [
        pytest.param(
            Ray(Point(0, 0, 0), Direction(1, 0, 0)),
            Plane(Point(2000, 0, 0), Direction(1, 0, 0)),
            2000,
            id="back-wall",
        ),
        pytest.param(
            Ray(Point(0, 0, 0), Direction(2, 1, 0.5)),
            Plane(Point(2000, 0, 0), Direction(1, 0, 0)),
            hypot(2000, 1000, 500),
            id="back-wall-oblique",
        ),
        pytest.param(
            Ray(Point(0, 0, 0), Direction(2, 1, 0.5)),
            Plane(Point(0, 1000, 0), Direction(0, 1, 0)),
            hypot(2000, 1000, 500),
            id="side-wall",
        ),
        pytest.param(
            Ray(Point(0, 0, 0), Direction(2, -1, 0.5)),
            Plane(Point(0, -1000, 0), Direction(0, 1, 0)),
            hypot(2000, 1000, 500),
            id="opposite-side-wall",
        ),
        pytest.param(
            Ray(Point(100, 200, 300), Direction(1, 2, -1)),
            Plane(Point(500, 0, 0), Direction(-10, 0, 0)),
            hypot(400, 800, 400),
            id="translated-origin-and-reversed-normal",
        ),
        pytest.param(
            Ray(Point(10, 20, 30), Direction(1, 0, 0)),
            Plane(Point(10, 0, 0), Direction(1, 0, 0)),
            0,
            id="origin-on-plane",
        ),
        pytest.param(
            Ray(Point(0, 0, 0), Direction(1, 1, 1)),
            Plane(Point(100, 100, 100), Direction(1, 1, 1)),
            sqrt(3 * 100**2),
            id="tilted-plane",
        ),
    ],
)
def test_calculates_distance_to_plane(
    ray: Ray, plane: Plane, expected_distance: float
) -> None:
    distance = calculate_ray_plane_distance(ray, plane)

    assert distance == pytest.approx(expected_distance)


@pytest.mark.parametrize(
    "direction",
    [Direction(0, 1, 0), Direction(1e-14, 1, 0), Direction(-1, 0, 0)],
    ids=["parallel", "nearly-parallel", "behind-origin"],
)
def test_returns_none_without_forward_intersection(direction: Direction) -> None:
    ray = Ray(Point(0, 0, 0), direction)
    wall = Plane(Point(2000, 0, 0), Direction(1, 0, 0))

    assert calculate_ray_plane_distance(ray, wall) is None


def test_ray_lying_in_plane_has_no_unique_intersection() -> None:
    ray = Ray(Point(2000, 0, 0), Direction(0, 1, 0))
    wall = Plane(Point(2000, 0, 0), Direction(1, 0, 0))

    assert calculate_ray_plane_distance(ray, wall) is None


@pytest.mark.parametrize("scale", [1e-15, 1, 1e15])
def test_vector_magnitudes_do_not_change_distance(scale: float) -> None:
    ray = Ray(Point(0, 0, 0), Direction(2 * scale, scale, 0))
    wall = Plane(Point(1000, 0, 0), Direction(-scale, 0, 0))

    distance = calculate_ray_plane_distance(ray, wall)

    assert distance == pytest.approx(hypot(1000, 500))


@pytest.mark.parametrize("invalid", [0, float("inf"), float("nan")])
def test_invalid_direction_is_rejected(invalid: float) -> None:
    ray = Ray(Point(0, 0, 0), Direction(invalid, 0, 0))
    wall = Plane(Point(1000, 0, 0), Direction(1, 0, 0))

    with pytest.raises(ValueError, match="Ray direction"):
        calculate_ray_plane_distance(ray, wall)


@pytest.mark.parametrize("invalid", [0, float("inf"), float("nan")])
def test_invalid_normal_is_rejected(invalid: float) -> None:
    ray = Ray(Point(0, 0, 0), Direction(1, 0, 0))
    wall = Plane(Point(1000, 0, 0), Direction(invalid, 0, 0))

    with pytest.raises(ValueError, match="Plane normal"):
        calculate_ray_plane_distance(ray, wall)
