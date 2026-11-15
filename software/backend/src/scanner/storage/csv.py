import csv
from collections.abc import Iterable, Iterator
from pathlib import Path

from scanner.models.measurement import ScanMeasurement

MEASUREMENT_COLUMNS = ("yaw_deg", "pitch_deg", "distance_mm")


def read_measurements_from_csv(path: Path) -> Iterator[ScanMeasurement]:
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None or not set(MEASUREMENT_COLUMNS).issubset(
            reader.fieldnames
        ):
            raise ValueError(
                "Measurement CSV must contain yaw_deg, pitch_deg and distance_mm"
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                yaw_text = row["yaw_deg"]
                pitch_text = row["pitch_deg"]
                distance_text = row["distance_mm"]
                if yaw_text is None or pitch_text is None:
                    raise ValueError("Missing angle")

                yield ScanMeasurement(
                    yaw_deg=float(yaw_text),
                    pitch_deg=float(pitch_text),
                    distance_mm=(
                        None
                        if distance_text is None or distance_text == ""
                        else float(distance_text)
                    ),
                )
            except (KeyError, ValueError) as error:
                raise ValueError(
                    f"Invalid measurement at CSV row {row_number}"
                ) from error


def write_measurements_to_csv(
    path: Path, measurements: Iterable[ScanMeasurement]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(MEASUREMENT_COLUMNS)

        for measurement in measurements:
            writer.writerow(
                (measurement.yaw_deg, measurement.pitch_deg, measurement.distance_mm)
            )
