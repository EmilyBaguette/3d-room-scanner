import sys
from pathlib import Path

import pytest

from scanner.cli.export_nx_points import main


def test_exports_measurement_csv_with_requested_origin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    input_path = tmp_path / "measurements.csv"
    output_path = tmp_path / "points.txt"
    input_path.write_text(
        "yaw_deg,pitch_deg,distance_mm\n0,0,2000\n1,2,\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "export-nx-points",
            str(input_path),
            str(output_path),
            "--origin-x",
            "10",
            "--origin-y",
            "20",
            "--origin-z",
            "30",
        ],
    )

    main()

    assert output_path.read_text(encoding="utf-8") == "2010.0,20.0,30.0\n"


@pytest.mark.parametrize("alias", ["same", "relative", "symlink", "hardlink"])
def test_rejects_output_referring_to_input_without_changing_it(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    alias: str,
) -> None:
    input_path = tmp_path / "measurements.csv"
    contents = "yaw_deg,pitch_deg,distance_mm\n0,0,2000\n"
    input_path.write_text(contents, encoding="utf-8")
    output_path = input_path
    if alias == "relative":
        monkeypatch.chdir(tmp_path)
        output_path = Path("measurements.csv")
    elif alias == "symlink":
        output_path = tmp_path / "points.txt"
        output_path.symlink_to(input_path)
    elif alias == "hardlink":
        output_path = tmp_path / "points.txt"
        output_path.hardlink_to(input_path)
    monkeypatch.setattr(
        sys, "argv", ["export-nx-points", str(input_path), str(output_path)]
    )

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    assert "input and output must refer to different files" in capsys.readouterr().err
    assert input_path.read_text(encoding="utf-8") == contents


@pytest.mark.parametrize("input_kind", ["missing", "directory"])
@pytest.mark.parametrize("existing_output", [False, True])
def test_rejects_invalid_input_without_touching_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    input_kind: str,
    existing_output: bool,
) -> None:
    input_path = tmp_path / "measurements.csv"
    if input_kind == "directory":
        input_path.mkdir()
    output_path = tmp_path / "points.txt"
    if existing_output:
        output_path.write_text("existing points\n", encoding="utf-8")
    monkeypatch.setattr(
        sys, "argv", ["export-nx-points", str(input_path), str(output_path)]
    )

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    message = (
        "input file does not exist"
        if input_kind == "missing"
        else "input path is not a file"
    )
    assert f"{message}: {input_path}" in capsys.readouterr().err
    if existing_output:
        assert output_path.read_text(encoding="utf-8") == "existing points\n"
    else:
        assert not output_path.exists()
