from dataclasses import dataclass


@dataclass(frozen=True)
class ScanMeasurement:
    yaw_deg: float
    pitch_deg: float
    distance_mm: float | None
