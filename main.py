import logging
import sys
from rmc.decoder import RMCDecoder

# Configure logging for application info (not output)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)] # Log to stderr so stdout is clean for JSON
)

if __name__ == "__main__":
    # Sample provided in strict requirement
    sentence = "$GPRMC,112000.000,A,5021.5874,N,00408.9009,W,9.09,309.61,201022,,,A*74"

    try:
        decoder = RMCDecoder(sentence)
        data = decoder.decode()
        json_str = decoder.to_json(data)

        # Requirement 5: Print JSON string to terminal (Clean output)
        print(json_str)
        
        # Requirement 6: Save to file
        saved_path = decoder.save(json_str)
        logging.info(f"Process complete. Data saved to {saved_path}")

    except ValueError as e:
        logging.error(f"Application Error: {e}")
        sys.exit(1)
