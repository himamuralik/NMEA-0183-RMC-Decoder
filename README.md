

# NMEA 0183 RMC Decoder

## Overview

This project implements a decoder for **NMEA 0183 RMC (Recommended Minimum Specific GNSS Data)** messages.
It validates the NMEA checksum, parses the RMC sentence, converts required units, and outputs the decoded data as a formatted JSON string.

The solution follows **OOP principles**, complies with **PEP8**, and includes **unit tests**.

---

## Features

* Validates NMEA 0183 checksum
* Decodes RMC messages
* Converts:

  * Latitude & Longitude to decimal degrees
  * Speed Over Ground (SOG) from knots to meters per second
* Outputs JSON to:

  * Terminal
  * File named `rmc_<unix_timestamp>.json`
* Creates output folder named with the **current date (YYYY-MM-DD)**
* Includes unit tests using `pytest`

---

## Input Format

Example RMC sentence:

```
$GPRMC,112000.000,A,5021.5874,N,00408.9009,W,9.09,309.61,201022,,,A*74
```

---

## Output Format

```json
{
    "LAT": 50.35979,
    "LON": -4.14835,
    "SOG": 4.674,
    "COG": 309
}
```

---

## Important Note on Latitude & Longitude Conversion

The exercise specification mentions converting coordinates from **deg.min.sec** to decimal degrees.

However, according to the **official NMEA 0183 RMC standard**, latitude and longitude are provided in **degrees and decimal minutes (DMM)** format:

```
DDMM.MMMM  (latitude)
DDDMM.MMMM (longitude)
```

This implementation correctly converts **DMM → decimal degrees**, which is the standard and correct interpretation for RMC messages.

---

## How It Works

### Checksum Validation

* XOR is applied to all characters between `$` and `*`
* The calculated checksum is compared against the transmitted checksum
* Decoding stops if the checksum is invalid

### Unit Conversions

* **Latitude / Longitude**
  decimal_degrees = degrees + (minutes / 60)

* **Speed Over Ground (SOG)**
  meters_per_second = knots × 0.514444

* **Course Over Ground (COG)**
  Converted to integer as required

---

## How to Run

### Run the decoder

```bash
python rmc_decoder.py
```

### Run tests

```bash
pytest
```

---

## Project Structure

```
.
├── rmc_decoder.py
├── tests/
│   └── test_decoder.py
├── README.md
```

---

## Assumptions

* Only valid `$GPRMC` sentences are processed
* RMC status must be `A` (data valid)
* UTC time and date fields are not included in the output
* Output directory is created automatically if it does not exist

---

## Sources

* NMEA 0183 Standard – RMC Sentence Definition
* [https://gpsd.gitlab.io/gpsd/NMEA.html](https://gpsd.gitlab.io/gpsd/NMEA.html)

---

## Author

Hima Murali Kattur

---




