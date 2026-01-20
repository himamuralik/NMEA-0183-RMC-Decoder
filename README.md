# NMEA 0183 RMC Decoder

A Python utility to parse NMEA 0183 `$GPRMC` messages into formatted JSON.

## Features
- Validates NMEA Checksums.
- Converts Coordinates (DMS -> Decimal Degrees).
- Converts Speed (Knots -> m/s).
- Exports to JSON (Terminal & File).

## Installation
```bash
pip install -r requirements.txt
```
Usage

Run the main script:
```bash
python main.py
```
Testing
Run the unit tests:

```Bash
pytest
```

