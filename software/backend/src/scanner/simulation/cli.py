from scanner.geometry.primitives import Point
from scanner.simulation.laser import simulate_range
from scanner.simulation.scenes import create_alcove


def main() -> None:
    surfaces = create_alcove()
    origin = Point(0, 0, 1000)

    for pitch in range(-30, 31):
        for yaw in range(-45, 46):
            distance = simulate_range(origin, yaw, pitch, surfaces)
            print(distance)
