
import json
from datetime import datetime
from pathlib import Path


from rmc.parser import RMCData
from rmc.utils import (
validate_checksum,
dmm_to_decimal,
knots_to_mps,
)


class RMCDecoder:
def __init__(self, sentence: str):
self.sentence = sentence


def decode(self) -> RMCData:
if not validate_checksum(self.sentence):
raise ValueError("Invalid NMEA checksum")


body = self.sentence.split('*')[0]
fields = body.split(',')


status = fields[2]
if status != 'A':
raise ValueError("RMC message is void (status != 'A')")
lat = dmm_to_decimal(fields[3], fields[4])
lon = dmm_to_decimal(fields[5], fields[6])
sog = knots_to_mps(float(fields[7]))
cog = int(float(fields[8]))


logging.info("Decoded active RMC message successfully")


return RMCData(lat=lat, lon=lon, sog=sog, cog=cog)(lat=lat, lon=lon, sog=sog, cog=cog)


def to_json(self, data: RMCData) -> str:
return json.dumps(
{
"LAT": data.lat,
"LON": data.lon,
"SOG": data.sog,
"COG": data.cog,
},
indent=2,
)


def save(self, json_str: str) -> None:
today = datetime.utcnow().strftime('%Y-%m-%d')
timestamp = int(datetime.utcnow().timestamp())


directory = Path(today)
directory.mkdir(exist_ok=True)


filepath = directory / f"rmc_{timestamp}.json"
filepath.write_text(json_str)
