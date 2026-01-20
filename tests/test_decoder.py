
import pytest
from rmc.decoder import RMCDecoder




VALID_SENTENCE = "$GPRMC,112000.000,A,5021.5874,N,00408.9009,W,9.09,309.61,201022,,,A*74"




def test_valid_decode():
decoder = RMCDecoder(VALID_SENTENCE)
data = decoder.decode()


assert round(data.lat, 4) == 50.3598
assert round(data.lon, 4) == -4.1483
assert data.cog == 309




def test_invalid_checksum():
with pytest.raises(ValueError):
RMCDecoder(VALID_SENTENCE.replace('*74', '*00')).decode()
