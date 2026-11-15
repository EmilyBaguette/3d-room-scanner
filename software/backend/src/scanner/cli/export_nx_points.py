import argparse
from pathlib import Path

from scanner.geometry.primitives import Point
from scanner.processing.point_cloud import measurements_to_points
from scanner.storage.csv import read_measurements_from_csv
from scanner.storage.nx_points import write_points_for_nx


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export scan measurements as XYZ points for Siemens NX"
    )
    parser.add_argument("input", type=Path, help="Measurement CSV to read")
    parser.add_argument("output", type=Path, help="Comma-delimited XYZ file to create")
    parser.add_argument("--origin-x", type=float, default=0.0, help="Scanner X in mm")
    parser.add_argument("--origin-y", type=float, default=0.0, help="Scanner Y in mm")
    parser.add_argument("--origin-z", type=float, default=0.0, help="Scanner Z in mm")
    args = parser.parse_args()
    input_path: Path = args.input
    output_path: Path = args.output
    if not input_path.exists():
        parser.error(f"input file does not exist: {input_path}")
    if not input_path.is_file():
        parser.error(f"input path is not a file: {input_path}")
    if input_path.resolve() == output_path.resolve() or (
        output_path.exists() and input_path.samefile(output_path)
    ):
        parser.error("input and output must refer to different files")
    return args


def main() -> None:
    args = parse_args()
    measurements = read_measurements_from_csv(args.input)
    origin = Point(args.origin_x, args.origin_y, args.origin_z)
    points = measurements_to_points(measurements, origin)
    write_points_for_nx(args.output, points)
