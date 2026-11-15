import csv
from pathlib import Path

import pytest

from scanner.models.measurement import ScanMeasurement
from scanner.storage.csv import read_measurements_from_csv, write_measurements_to_csv


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


def test_reads_measurements_and_empty_distance(tmp_path: Path) -> None:
    path = tmp_path / "measurements.csv"
    path.write_text(
        "yaw_deg,pitch_deg,distance_mm\n-1.5,2,1234.5\n0,2,\n",
        encoding="utf-8",
    )

    assert list(read_measurements_from_csv(path)) == [
        ScanMeasurement(yaw_deg=-1.5, pitch_deg=2, distance_mm=1234.5),
        ScanMeasurement(yaw_deg=0, pitch_deg=2, distance_mm=None),
    ]


def test_rejects_csv_without_measurement_columns(tmp_path: Path) -> None:
    path = tmp_path / "measurements.csv"
    path.write_text("x,y,z\n1,2,3\n", encoding="utf-8")

    with pytest.raises(ValueError, match="must contain"):
        list(read_measurements_from_csv(path))


def test_reports_invalid_measurement_row(tmp_path: Path) -> None:
    path = tmp_path / "measurements.csv"
    path.write_text(
        "yaw_deg,pitch_deg,distance_mm\nnot-an-angle,2,1000\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="row 2"):
        list(read_measurements_from_csv(path))
