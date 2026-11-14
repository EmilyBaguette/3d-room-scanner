import csv
from collections.abc import Iterable
from pathlib import Path

from scanner.models.measurement import ScanMeasurement


def write_measurements_to_csv(
    path: Path, measurements: Iterable[ScanMeasurement]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("yaw_deg", "pitch_deg", "distance_mm"))

        for measurement in measurements:
            writer.writerow(
                (measurement.yaw_deg, measurement.pitch_deg, measurement.distance_mm)
            )
