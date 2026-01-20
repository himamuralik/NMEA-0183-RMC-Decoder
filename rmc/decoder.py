python
import json
import logging
from datetime import datetime
from pathlib import Path

from rmc.models import RMCData
from rmc.utils import validate_checksum, dmm_to_decimal, knots_to_mps


class RMCDecoder:
    def __init__(self, sentence: str) -> None:
        self.sentence = sentence

    def decode(self) -> RMCData:
        if not validate_checksum(self.sentence):
            raise ValueError("Invalid NMEA checksum")

        body = self.sentence.split("*")[0]
        fields = body.split(",")

        if len(fields) < 9:
            raise ValueError("Incomplete RMC sentence")

        status = fields[2]
        if status != "A":
            raise ValueError("RMC message is void (status != 'A')")

        lat = dmm_to_decimal(fields[3], fields[4])
        lon = dmm_to_decimal(fields[5], fields[6])
        sog = knots_to_mps(float(fields[7]))
        cog = int(float(fields[8]))

        return RMCData(lat=lat, lon=lon, sog=sog, cog=cog)

    @staticmethod
    def to_json(data: RMCData) -> str:
        return json.dumps(
            {
                "LAT": data.lat,
                "LON": data.lon,
                "SOG": data.sog,
                "COG": data.cog,
            },
            indent=2,
        )

    @staticmethod
    def save(json_str: str) -> Path:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        timestamp = int(datetime.utcnow().timestamp())

        directory = Path(today)
        directory.mkdir(exist_ok=True)

        path = directory / f"rmc_{timestamp}.json"
        path.write_text(json_str)

        logging.info("Saved RMC JSON to %s", path)
        return path
