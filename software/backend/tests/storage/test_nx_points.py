from pathlib import Path

from scanner.geometry.primitives import Point
from scanner.storage.nx_points import write_points_for_nx


def test_writes_comma_delimited_xyz_without_header(tmp_path: Path) -> None:
    output = tmp_path / "points.txt"

    write_points_for_nx(
        output,
        [Point(1, 2, 3), Point(4.5, -6.25, 7)],
    )

    assert output.read_text(encoding="utf-8") == "1,2,3\n4.5,-6.25,7\n"
