
from rmc.decoder import RMCDecoder




if __name__ == "__main__":
sentence = "$GPRMC,112000.000,A,5021.5874,N,00408.9009,W,9.09,309.61,201022,,,A*74"


decoder = RMCDecoder(sentence)
data = decoder.decode()
json_str = decoder.to_json(data)


logging.info("RMC JSON output:
%s", json_str)
decoder.save(json_str)
