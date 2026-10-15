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
