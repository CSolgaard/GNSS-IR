#!/usr/bin/env python3
import sys
import re

def dms_to_decimal(degrees, minutes, seconds):
    """
    Convert degrees, minutes, and seconds to decimal degrees.
    
    Args:
    - degrees (float): Degrees
    - minutes (float): Minutes
    - seconds (float): Seconds
    
    Returns:
    - float: Decimal degrees
    """
    # Calculate decimal degrees considering negative values for directions like West/South
    decimal_degrees = abs(degrees) + (minutes / 60) + (seconds / 3600)
    if degrees < 0:
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def parse_dms(dms_str):
    """
    Parse a DMS (Degrees Minutes Seconds) string into separate components.
    
    Args:
    - dms_str (str): DMS string formatted as "<degrees>° <minutes>' <seconds>\""
    
    Returns:
    - tuple: (degrees, minutes, seconds) as floats
    """
    # Use a regular expression to match degrees, minutes, and seconds
    pattern = r"(-?\d+)[°*d]\s*(\d+)'?\s*(\d+(?:\.\d+)?)\"?"
    match = re.match(pattern, dms_str)

    if not match:
        raise ValueError("Invalid DMS format. Expected format: '-75° 15' 30\"'")

    degrees = float(match.group(1))
    minutes = float(match.group(2))
    seconds = float(match.group(3))
    return degrees, minutes, seconds

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dms_to_decimal.py \"<degrees>° <minutes>' <seconds>\"")
        sys.exit(1)

    # Parse the DMS string from command line argument
    dms_string = sys.argv[1]

    try:
        degrees, minutes, seconds = parse_dms(dms_string)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Convert DMS to decimal degrees
    decimal_result = dms_to_decimal(degrees, minutes, seconds)
    print(f"Decimal degrees: {decimal_result}")
