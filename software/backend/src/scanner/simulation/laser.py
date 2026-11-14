from scanner.geometry.conversion import to_cartesian
from scanner.geometry.intersections import calculate_ray_plane_distance
from scanner.geometry.primitives import Direction, Point, Ray, Surface


def simulate_range(
    origin: Point, yaw_deg: float, pitch_deg: float, surfaces: list[Surface]
) -> float | None:
    unit_vector = to_cartesian(1, yaw_deg, pitch_deg)
    ray = Ray(origin, Direction(unit_vector.x, unit_vector.y, unit_vector.z))
    distances: list[float] = []

    for surface in surfaces:
        distance = calculate_ray_plane_distance(ray, surface.plane)
        if distance is None:
            continue

        hit = Point(
            origin.x + distance * unit_vector.x,
            origin.y + distance * unit_vector.y,
            origin.z + distance * unit_vector.z,
        )

        if surface.contains(hit):
            distances.append(distance)

    return min(distances, default=None)
