#!/usr/bin/env python3

import paramiko
import os

# SSH details
REMOTE_HOST = "10.58.1.129"
REMOTE_USER = "csol"
PASSWORD = "Insert Your Password"
REMOTE_PATH = "/data/rinex3/obs/"
LOCAL_PATH = "/mnt/c/Users/csol/GNSS_IR/src/TEMP_RINEX_DATA/"

def generate_filenames(station_id, year, doy_range):
    """
    Generate RINEX file names based on the Station ID, Year, and DOY range.
    """
    filenames = []
    for doy in doy_range:
        doy_str = f"{doy:03d}"  # Zero-pad DOY to 3 digits
        filename = f"{station_id}00GRL_R_{year}{doy_str}0000_01D_15S_MO.crx.gz"
        filenames.append(filename)
    return filenames

def download_files(station_id, year, doy_range, local_dir):
    # Initialize SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote server
    ssh.connect(REMOTE_HOST, username=REMOTE_USER, password=PASSWORD)

    # Initialize SFTP client
    sftp = ssh.open_sftp()

    # Generate file names based on the input DOY range
    filenames = generate_filenames(station_id, year, doy_range)

    year_path = f"{year}/"
    # Loop through the filenames and download each
    for filename in filenames:
        remote_filepath = os.path.join(REMOTE_PATH, year_path)
        remote_filepath = os.path.join(remote_filepath, filename)
        # print(remote_filepath)
        local_filepath = os.path.join(local_dir, filename)

        # sftp.get(remote_filepath, local_filepath)
        try:
            print(f"Downloading: {remote_filepath} -> {local_filepath}")
            sftp.get(remote_filepath, local_filepath)
            print(f"Successfully downloaded {filename}")
        except FileNotFoundError:
            print(f"File not found: {filename}")
    
    # Close connections
    sftp.close()
    ssh.close()

if __name__ == "__main__":
    # Example inputs (you can modify this to accept user input)
    station_id = (input("Enter the Station ID (e.g., NORD): ").strip()).upper()
    year = input("Enter the Year (e.g., 2024): ").strip()

    # Accept DOY range
    doy_start = int(input("Enter the start DOY (e.g., 102): "))
    doy_end = int(input("Enter the end DOY (e.g., 150): "))
    
    doy_range = range(doy_start, doy_end + 1)

    # Call the download function
    download_files(station_id, year, doy_range, LOCAL_PATH)

    # Write the station_id to a file
    with open("/tmp/station_id.txt", "w") as f:
        f.write(station_id)
    # print(f"STATION_ID={station_id}")