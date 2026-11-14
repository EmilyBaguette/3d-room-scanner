import csv
from pathlib import Path

from scanner.models.measurement import ScanMeasurement
from scanner.storage.csv import write_measurements_to_csv


def read_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.reader(file))


def test_writes_header_measurements_and_missing_distance(tmp_path: Path) -> None:
    output = tmp_path / "measurements.csv"
    measurements = (
        measurement
        for measurement in [
            ScanMeasurement(yaw_deg=-1, pitch_deg=2, distance_mm=1234.5),
            ScanMeasurement(yaw_deg=0, pitch_deg=2, distance_mm=None),
        ]
    )

    write_measurements_to_csv(output, measurements)

    assert read_rows(output) == [
        ["yaw_deg", "pitch_deg", "distance_mm"],
        ["-1", "2", "1234.5"],
        ["0", "2", ""],
    ]


def test_overwrites_existing_csv(tmp_path: Path) -> None:
    output = tmp_path / "measurements.csv"
    write_measurements_to_csv(
        output, [ScanMeasurement(yaw_deg=1, pitch_deg=2, distance_mm=3)]
    )

    write_measurements_to_csv(
        output, [ScanMeasurement(yaw_deg=4, pitch_deg=5, distance_mm=6)]
    )

    assert read_rows(output) == [
        ["yaw_deg", "pitch_deg", "distance_mm"],
        ["4", "5", "6"],
    ]
