import csv
from collections.abc import Iterable
from pathlib import Path

from scanner.geometry.primitives import Point


def write_points_for_nx(path: Path, points: Iterable[Point]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        for point in points:
            writer.writerow((point.x, point.y, point.z))
