#!/usr/bin/env python3

import os 
import subprocess
from tqdm import tqdm
import numpy as np
import re
from dataclasses import dataclass, asdict
from pprint import pprint
import gnss_ir_util as src

# ----------------------- Station Specific Functions -----------------------
def run_convert_rinex2_snr(station_id, year, doy): 
    rinex2_command = f"rinex2snr {station_id} {year} {doy} -orb gbm -nolook True -samplerate 5 -snr 50 -overwrite OVERWRITE"
    subprocess.run(rinex2_command, check=True, shell=True)

def run_gnssIR(station_id, year, doy):
    gnssir_command = f"gnssir {station_id} {year} {doy} -snr 50"
    subprocess.run(gnssir_command, check=True, shell=True)
    return
# --------------------------------------------------------------------------


if __name__ == "__main__": 
    # Set Main file path to data dir. 
    rinex3_path = "/mnt/c/Users/csol/GNSS_IR/src/TEMP_RINEX_DATA/"
    rinex3_files = src.load_Rinex_files(rinex3_path)

    os.chdir(rinex3_path)

    # Now the script will run as if it's in the specified directory
    print("Data Directory:", os.getcwd())


    with tqdm(total=len(rinex3_files)) as pbar:
        for rinex3_file in rinex3_files:
            # Extract basic information from Rinex 3 files.
            station_id, year, doy = src.get_info(rinex3_file)
        
            # Convert Rinex3 -> Rinex2 files 
            src.run_convert_rinex3_2(rinex3_file)

            # Convert Rinex2 -> SNR files
            run_convert_rinex2_snr(station_id, year, doy)

            # Create JSON file using gnssir_input (only for the first iteration)
            rinex_file_path = src.determine_new_path(rinex3_file)
            
                # Extract position from rinex file 
            lat, lon, height = src.get_xyz(rinex_file_path)

            if pbar.n == 0:
                # Create JSON for GNSS-IR (1.st iteration only)
                input_orig = src.create_gnssir_input_class(lat=lat, lon=lon, height=height, 
                                                           e1=4, e2=10, h1=14, h2=30, nr1=14, 
                                                           nr2=30, peak2noise=2.7, ampl=6.0, 
                                                           frlist="1 20 5 101 102 201 205 206 207 302 306", 
                                                           azlist2 = "180 250"
                                                           )
                src.create_json(station_id, lat, lon, height, input_orig)

            # Run GNSS-IR calculation
            run_gnssIR(station_id, year, doy)
            pbar.update(1)


