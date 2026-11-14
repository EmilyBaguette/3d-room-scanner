import argparse
from pathlib import Path

from scanner.simulation.scan import simulate_scan
from scanner.storage.csv import write_measurements_to_csv

DEFAULT_YAW_MIN = -45
DEFAULT_YAW_MAX = 45
DEFAULT_PITCH_MIN = -30
DEFAULT_PITCH_MAX = 30


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate a room scan")

    parser.add_argument("output", type=Path, help="CSV file to create")
    parser.add_argument("--yaw-min", type=int, default=DEFAULT_YAW_MIN)
    parser.add_argument("--yaw-max", type=int, default=DEFAULT_YAW_MAX)
    parser.add_argument("--pitch-min", type=int, default=DEFAULT_PITCH_MIN)
    parser.add_argument("--pitch-max", type=int, default=DEFAULT_PITCH_MAX)

    args = parser.parse_args()

    if args.yaw_min > args.yaw_max:
        parser.error("--yaw-min must be less than or equal to --yaw-max")
    if args.pitch_min > args.pitch_max:
        parser.error("--pitch-min must be less than or equal to --pitch-max")

    return args


def main() -> None:
    args = parse_args()
    yaw_range = range(args.yaw_min, args.yaw_max + 1)
    pitch_range = range(args.pitch_min, args.pitch_max + 1)

    measurements = simulate_scan(yaw_range=yaw_range, pitch_range=pitch_range)

    write_measurements_to_csv(args.output, measurements)
