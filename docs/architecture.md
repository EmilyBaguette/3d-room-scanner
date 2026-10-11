```mermaid
flowchart TB
    UI["<b>Frontend</b><br/><small>Setup, control, progress,<br/>visualisation and export</small>"]
    API["<b>Backend</b><br/><small>Scan jobs, calibration,<br/>acquisition and processing</small>"]
    FW["<b>Firmware</b><br/><small>Motion, measurement<br/>coordination and safety</small>"]
    LASER["<b>Laser sensor</b><br/><small>Measures distance</small>"]
    MOTOR["<b>Motor drivers</b><br/><small>Drive the pan and tilt motors</small>"]
    ENC["<b>Encoders</b><br/><small>Measure angular position of each axis</small>"]
    STORE[("Scan data")]

    UI <-->|"HTTP / WebSocket"| API
    API <-->|"USB serial"| FW
    API <-->|"File I/O"| STORE
    FW <-->|"UART"| LASER
    FW -->|"GPIO"| MOTOR
    ENC -.->|"SPI / I²C / GPIO"| FW

    style ENC stroke-dasharray: 2
```

| Component | Technology | Runs on           |
| --------- | ---------- | ----------------- |
| Frontend  | React      | Browser           |
| Backend   | Python     | Raspberry Pi 4    |
| Firmware  | C/C++      | Raspberry Pi Pico |
