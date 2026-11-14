import sys
from pathlib import Path

import pytest

from scanner.simulation.cli import (
    DEFAULT_PITCH_MAX,
    DEFAULT_PITCH_MIN,
    DEFAULT_YAW_MAX,
    DEFAULT_YAW_MIN,
    parse_args,
)


def test_parse_args_uses_default_scan_bounds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["simulate-scan", "scan.csv"])

    args = parse_args()

    assert args.output == Path("scan.csv")
    assert args.yaw_min == DEFAULT_YAW_MIN
    assert args.yaw_max == DEFAULT_YAW_MAX
    assert args.pitch_min == DEFAULT_PITCH_MIN
    assert args.pitch_max == DEFAULT_PITCH_MAX


def test_parse_args_accepts_custom_scan_bounds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "simulate-scan",
            "scan.csv",
            "--yaw-min",
            "-10",
            "--yaw-max",
            "20",
            "--pitch-min",
            "-5",
            "--pitch-max",
            "15",
        ],
    )

    args = parse_args()

    assert (args.yaw_min, args.yaw_max) == (-10, 20)
    assert (args.pitch_min, args.pitch_max) == (-5, 15)


@pytest.mark.parametrize(
    "arguments",
    [
        ["--yaw-min", "10", "--yaw-max", "0"],
        ["--pitch-min", "10", "--pitch-max", "0"],
    ],
    ids=["yaw", "pitch"],
)
def test_parse_args_rejects_inverted_bounds(
    monkeypatch: pytest.MonkeyPatch, arguments: list[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["simulate-scan", "scan.csv", *arguments])

    with pytest.raises(SystemExit):
        parse_args()
