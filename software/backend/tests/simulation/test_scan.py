from scanner.models.measurement import ScanMeasurement
from scanner.simulation.scan import simulate_scan


def test_generates_measurements_in_pitch_then_yaw_order() -> None:
    measurements = list(
        simulate_scan(yaw_range=range(-1, 2), pitch_range=range(2))
    )

    assert len(measurements) == 6
    assert all(isinstance(measurement, ScanMeasurement) for measurement in measurements)
    assert [
        (measurement.yaw_deg, measurement.pitch_deg)
        for measurement in measurements
    ] == [
        (-1, 0),
        (0, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]


def test_preserves_measurement_without_intersection() -> None:
    measurements = list(simulate_scan(yaw_range=[0], pitch_range=[-30]))

    assert measurements == [
        ScanMeasurement(yaw_deg=0, pitch_deg=-30, distance_mm=None)
    ]
