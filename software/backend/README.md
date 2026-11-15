# Scanner Backend

Python backend for a DIY 3D room scanner, responsible for laser measurement acquisition, calibration, scan processing and 3D model export.

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Development

| Task       | Command                |
| ---------- | ---------------------- |
| Test       | `uv run pytest`        |
| Lint       | `uv run ruff check .`  |
| Format     | `uv run ruff format .` |
| Type check | `uv run basedpyright`  |

## Simulation

Run the simulated alcove scan with:

```bash
uv run simulate-scan scan.csv
```

Export a measurement CSV as comma-delimited XYZ points for Siemens NX:

```bash
uv run export-nx-points scan.csv scan_points_mm.txt
```

In NX, import the resulting file with **File → Import → Points from File** and
use millimetres as the part units.
