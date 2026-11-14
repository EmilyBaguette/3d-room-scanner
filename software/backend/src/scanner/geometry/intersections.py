from math import hypot

from scanner.geometry.primitives import Plane, Ray


def calculate_ray_plane_distance(ray: Ray, plane: Plane) -> float | None:
    """Calculate the distance from a ray's origin to its intersection with a plane.

    Returns the distance in millimetres, or None if the ray is parallel
    to the plane or the intersection lies behind the ray's origin.
    An intersection at the origin returns 0.0.

    Rays within 1e-12 of parallel are treated as parallel.
    Planes are infinite and have no boundaries.

    Raises:
        ValueError: If the ray direction or plane normal is zero or nonfinite.
    """
    direction_length = hypot(ray.direction.x, ray.direction.y, ray.direction.z)
    normal_length = hypot(plane.normal.x, plane.normal.y, plane.normal.z)
    if not 0 < direction_length < float("inf"):
        raise ValueError("Ray direction must be finite and nonzero")
    if not 0 < normal_length < float("inf"):
        raise ValueError("Plane normal must be finite and nonzero")

    dx = ray.direction.x / direction_length
    dy = ray.direction.y / direction_length
    dz = ray.direction.z / direction_length
    nx = plane.normal.x / normal_length
    ny = plane.normal.y / normal_length
    nz = plane.normal.z / normal_length

    denominator = dx * nx + dy * ny + dz * nz
    if abs(denominator) <= 1e-12:
        return None

    distance = (
        (plane.point.x - ray.origin.x) * nx
        + (plane.point.y - ray.origin.y) * ny
        + (plane.point.z - ray.origin.z) * nz
    ) / denominator
    if distance < 0:
        return None

    return distance
