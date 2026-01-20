import json
import logging
import os
import time
from datetime import datetime
from rmc.decoder import RMCDecoder

# Configure logging at the Application Level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def save_to_file(data: dict):
    """Saves JSON to a date-stamped folder."""
    date_folder = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(date_folder, exist_ok=True)

    unix_timestamp = int(time.time())
    filename = f"rmc_{unix_timestamp}.json"
    filepath = os.path.join(date_folder, filename)

    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"File successfully saved to: {filepath}")
    except IOError as e:
        logging.error(f"Failed to write file: {e}")

def main():
    sample_sentence = "$GPRMC,112000.000,A,5021.5874,N,00408.9009,W,9.09,309.61,201022,,,A*74"
    
    try:
        decoder = RMCDecoder(sample_sentence)
        result = decoder.parse()

        # Core Requirement 5: Print JSON to terminal
        json_output = json.dumps(result, indent=4)
        print(json_output)

        # Core Requirement 6: Save to file
        save_to_file(result)

    except ValueError as e:
        logging.error(f"Application Error: {e}")

if __name__ == "__main__":
    main()
