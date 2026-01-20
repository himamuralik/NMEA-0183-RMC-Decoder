import logging
from typing import Dict, Any, Union
from rmc.utils import validate_checksum, dmm_to_decimal, knots_to_mps

logger = logging.getLogger(__name__)

class RMCDecoder:
    """
    Decoder for NMEA 0183 RMC sentences.
    """
    
    def __init__(self, sentence: str):
        self.sentence = sentence.strip()

    def parse(self) -> Dict[str, Union[float, int]]:
        """
        Parses the RMC sentence and returns a structured dictionary.
        Raises ValueError if checksum is invalid.
        """
        # 1. Fail-Fast: Checksum validation first
        if not validate_checksum(self.sentence):
            logger.error("Checksum validation failed for: %s", self.sentence)
            raise ValueError("Invalid NMEA Checksum")

        parts = self.sentence.split(',')
        
        # Safe extraction with defaults
        try:
            # RMC Structure: $GPRMC,time,status,lat,NS,lon,EW,spd,cog,date...
            # Index:            0     1    2    3  4   5  6   7   8    9
            
            # Validate Status ('A' = Active)
            if parts[2] != 'A':
                logger.warning("RMC Status is Void (V). Data may be invalid.")

            raw_lat = parts[3]
            lat_dir = parts[4]
            raw_lon = parts[5]
            lon_dir = parts[6]
            
            # Handle empty speed/course fields
            sog_knots = float(parts[7]) if parts[7] else 0.0
            cog_deg = float(parts[8]) if parts[8] else 0.0

            # Transformations
            return {
                "LAT": dmm_to_decimal(raw_lat, lat_dir),
                "LON": dmm_to_decimal(raw_lon, lon_dir),
                "SOG": knots_to_mps(sog_knots),
                "COG": int(cog_deg)  # Requirement: Output as int
            }

        except (IndexError, ValueError) as e:
            logger.error("Parsing error: %s", str(e))
            raise ValueError(f"Malformed RMC sentence: {str(e)}")
