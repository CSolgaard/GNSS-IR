import os
import re

def get_doy_range(directory):
    # Regular expression to match the station ID, year, and DOY
    pattern = re.compile(r"^([A-Z0-9]{4}).*_(\d{4})(\d{3}).*\.rnx$")

    doy_list = []
    station_id = None
    year = None

    # Iterate through files in the specified directory
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            station_id = match.group(1)  # Extract the station ID
            year = int(match.group(2))   # Extract the year
            doy = int(match.group(3))    # Extract the DOY
            doy_list.append(doy)         # Append only DOY since the year is the same

    # If there are no matching files, return None
    if not doy_list:
        return None, None, None

    # Determine the start and end DOY
    start_doy = min(doy_list)
    end_doy = max(doy_list)

    return station_id, year, (start_doy, end_doy)

if __name__ == "__main__":
    # Use an absolute path to the directory
    rinex3_path = "/mnt/c/Users/csol/GNSS_IR/Data_Rinex/NUK2/NUK2/"

    # Check if the path exists before proceeding
    if not os.path.exists(rinex3_path):
        print(f"Directory {rinex3_path} does not exist.")
    else:
        # Change to the specified directory (optional)
        os.chdir(rinex3_path)
        print("Data Directory:", os.getcwd())

        # Call the function to get the station ID, year, and DOY range
        station_id, year, doy_range = get_doy_range(rinex3_path)

        if station_id:
            start_doy, end_doy = doy_range
            print(f"Station ID: {station_id}")
            print(f"Year: {year}")
            print(f"Start DOY: {start_doy}")
            print(f"End DOY: {end_doy}")
        else:
            print("No Rinex files found in the specified directory.")
