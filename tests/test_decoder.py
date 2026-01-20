import pytest
from rmc.decoder import RMCDecoder

# Valid reference data
VALID_SENTENCE = "$GPRMC,112000.000,A,5021.5874,N,00408.9009,W,9.09,309.61,201022,,,A*74"

def test_valid_parse():
    """Test that a valid sentence parses into the correct dictionary."""
    decoder = RMCDecoder(VALID_SENTENCE)
    data = decoder.parse()

    # Assert dictionary keys exist
    assert "LAT" in data
    assert "LON" in data
    assert "SOG" in data
    assert "COG" in data

    # Assert values match the math (Lat/Lon conversion)
    # 5021.5874 N -> 50 + (21.5874/60) = 50.35979...
    assert data["LAT"] == 50.35979
    # 00408.9009 W -> -(4 + (8.9009/60)) = -4.148348...
    assert data["LON"] == -4.148348
    assert data["SOG"] == 4.68  # 9.09 * 0.514444
    assert data["COG"] == 309   # Int conversion

def test_invalid_checksum():
    """Test that an invalid checksum raises a ValueError."""
    # Modify the checksum at the end to be wrong
    invalid_sentence = VALID_SENTENCE.replace('*74', '*00')
    
    with pytest.raises(ValueError, match="Invalid NMEA Checksum"):
        RMCDecoder(invalid_sentence).parse()

def test_void_status():
    """Test that a 'V' (Void) status is handled (logs warning but still parses)."""
    # Replace 'A' (Active) with 'V' (Void)
    void_sentence = VALID_SENTENCE.replace(',A,', ',V,')
    
    decoder = RMCDecoder(void_sentence)
    # Should not raise error, but results might be trusted less in real world
    data = decoder.parse()
    assert isinstance(data, dict)
