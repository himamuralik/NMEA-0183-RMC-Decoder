import operator
from functools import reduce

KNOTS_TO_MPS = 0.514444

def validate_checksum(sentence: str) -> bool:
    """
    Validates NMEA 0183 checksum (XOR of characters between $ and *).
    """
    if not sentence.startswith('$') or '*' not in sentence:
        return False

    try:
        content, checksum_hex = sentence[1:].strip().split('*')
        if not checksum_hex:
            return False
            
        calculated = reduce(operator.xor, (ord(c) for c in content), 0)
        return calculated == int(checksum_hex, 16)
    except ValueError:
        return False

def dmm_to_decimal(value: str, direction: str) -> float:
    """
    Converts NMEA DMM (Degrees + Minutes) to Decimal Degrees.
    """
    if not value or not direction:
        return 0.0

    # NMEA spec: Latitude is 2 digits degrees, Longitude is 3 digits
    cut_index = 2 if direction in ['N', 'S'] else 3

    try:
        degrees = int(value[:cut_index])
        minutes = float(value[cut_index:])
        
        decimal = degrees + (minutes / 60)
        
        if direction in ['S', 'W']:
            decimal *= -1
            
        return round(decimal, 6)
    except (ValueError, IndexError):
        return 0.0

def knots_to_mps(knots: float) -> float:
    """
    Converts speed from Knots to Meters per Second.
    """
    return round(knots * KNOTS_TO_MPS, 2)
