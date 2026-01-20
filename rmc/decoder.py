import json
import os
import time
from datetime import datetime
from typing import Dict


KNOTS_TO_MPS = 0.514444


class RMCDecoder:
    def __init__(self, sentence: str) -> None:
        self.sentence = sentence.strip()

    @staticmethod
    def validate_checksum(sentence: str) -> None:
        if "*" not in sentence:
            raise ValueError("No checksum found")

        data, checksum = sentence.split("*")
        data = data.lstrip("$")

        calculated = 0
        for char in data:
            calculated ^= ord(char)

        if f"{calculated:02X}" != checksum.upper():
            raise ValueError("Invalid NMEA checksum")

    @staticmethod
    def _dmm_to_decimal(value: str, direction: str) -> float:
        degrees = int(float(value) // 100)
        minutes = float(value) - (degrees * 100)
        decimal = degrees + minutes / 60

        if direction in ("S", "W"):
            decimal *= -1

        return decimal

    def decode(self) -> Dict[str, float]:
        self.validate_checksum(self.sentence)

        body = self.sentence.split("*")[0]
        fields = body.split(",")

        if fields[2] != "A":
            raise ValueError("RMC data not valid")

        lat = self._dmm_to_decimal(fields[3], fields[4])
        lon = self._dmm_to_decimal(fields[5], fields[6])

        sog = float(fields[7]) * KNOTS_TO_MPS
        cog = int(float(fields[8]))

        return {
            "LAT": lat,
            "LON": lon,
            "SOG": round(sog, 3),
            "COG": cog,
        }

    @staticmethod
    def save_output(data: Dict[str, float]) -> None:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        os.makedirs(today, exist_ok=True)

        timestamp = int(time.time())
        filename = f"{today}/rmc_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(json.dumps(data, indent=4))


if __name__ == "__main__":
    rmc_sentence = (
        "$GPRMC,112000.000,A,5021.5874,N,00408.9009,"
        "W,9.09,309.61,201022,,,A*74"
    )

    decoder = RMCDecoder(rmc_sentence)
    decoded = decoder.decode()
    decoder.save_output(decoded)

