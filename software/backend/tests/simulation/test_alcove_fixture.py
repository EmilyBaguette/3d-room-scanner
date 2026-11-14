import csv
from pathlib import Path

FIXTURE_PATH = (
    Path(__file__).parents[1]
    / "fixtures"
    / "simulation"
    / "alcove"
    / "measurements.csv"
)


def read_fixture() -> list[dict[str, str]]:
    with FIXTURE_PATH.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def test_alcove_fixture_has_expected_shape_and_known_measurement() -> None:
    rows = read_fixture()

    assert len(rows) == 5551
    assert set(rows[0]) == {"yaw_deg", "pitch_deg", "distance_mm"}
    assert (rows[0]["yaw_deg"], rows[0]["pitch_deg"]) == ("-45", "-30")
    assert (rows[-1]["yaw_deg"], rows[-1]["pitch_deg"]) == ("45", "30")

    centre = next(
        row
        for row in rows
        if row["yaw_deg"] == "0" and row["pitch_deg"] == "0"
    )
    assert float(centre["distance_mm"]) == 2300


def test_alcove_fixture_represents_missed_measurements_as_empty() -> None:
    rows = read_fixture()

    first_measurement = rows[0]
    assert first_measurement == {
        "yaw_deg": "-45",
        "pitch_deg": "-30",
        "distance_mm": "",
    }
