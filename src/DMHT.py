#!/usr/bin/env python3

import os 
import subprocess
from tqdm import tqdm
import re
from dataclasses import dataclass, asdict
import gnss_ir_util as src

# ----------------------- Station Specific Functions -----------------------
def run_convert_rinex2_snr(station_id, year, doy, doy_end, n_cores): 
    rinex2_command = f"rinex2snr {station_id} {year} {doy} -doy_end {doy_end} -orb gbm -nolook True -samplerate 15 -overwrite OVERWRITE -par {n_cores}"
    subprocess.run(rinex2_command, check=True, shell=True)

def run_gnssIR(station_id, year, doy, doy_end, n_cores):
    gnssir_command = f"gnssir {station_id} {year} {doy} -doy_end {doy_end} -snr 66 -par {n_cores}"
    subprocess.run(gnssir_command, check=True, shell=True)
    return

# --------------------- Set Specific Station Location ----------------------
lat = 76.76853056388889
lon = -18.67055783611111
height = 43.218             # Ellipsoidal height WGS80
# --------------------------------------------------------------------------


if __name__ == "__main__": 
    # Set Main file path to data dir. 
    rinex3_path = "/mnt/c/Users/csol/GNSS_IR/src/TEMP_RINEX_DATA/"  #Change to relative for robustness. 
    rinex3_files = src.load_Rinex_files(rinex3_path)

    # Change script absolute path to temporary data folder
    os.chdir(rinex3_path)

    # Unpack Rinex3 files and convert to rinex2
    with tqdm(total=len(rinex3_files)) as pbar:
        for rinex3_file in rinex3_files:
            src.run_convert_rinex3_2(rinex3_file)
            pbar.update(1)

    # Extract the DOY range based on rinex2 files
    station_id, year, doy_range = src.get_doy_range(rinex3_path)
    start_doy, end_doy = doy_range

    # Create JSON for GNSS-IR (1.st iteration only)
    input_orig = src.create_gnssir_input_class(lat=lat, lon=lon, height=height, 
                                                e1=2, e2=12, h1=4.0, h2=15.0, nr1=4.0, 
                                                nr2=15.0, peak2noise=2.7, ampl=6.0, 
                                                frlist="1 20 5 101 102 201 205 206 207 302 306", 
                                                azlist2 = "150 250"
                                                )
    src.create_json(station_id, lat, lon, height, input_orig)
    
    n_cores = src.count_nr_cores()      # Count logical processers used for parallel compution max=10
    # Convert Rinex2 -> SNR
    run_convert_rinex2_snr(station_id, year, start_doy, end_doy, n_cores)

    # Running GNSS-IR calculations on SNR files
    run_gnssIR(station_id, year, start_doy, end_doy, n_cores)







# if __name__ == "__main__": 
#     # Set Main file path to data dir. 
#     rinex3_path = "/mnt/c/Users/csol/GNSS_IR/src/TEMP_RINEX_DATA/"
#     rinex3_files = src.load_Rinex_files(rinex3_path)

#     os.chdir(rinex3_path)

#     # Now the script will run as if it's in the specified directory
#     print("Data Directory:", os.getcwd())


#     with tqdm(total=len(rinex3_files)) as pbar:
#         for rinex3_file in rinex3_files:
#             # Extract basic information from Rinex 3 files.
#             station_id, year, doy = src.get_info(rinex3_file)
        
#             # Convert Rinex3 -> Rinex2 files 
#             src.run_convert_rinex3_2(rinex3_file)

#             # Convert Rinex2 -> SNR files
#             run_convert_rinex2_snr(station_id, year, doy)

#             # Create JSON file using gnssir_input (only for the first iteration)

#             rinex_file_path = src.determine_new_path(rinex3_file)
            
#             # Extract position from rinex file 
#             lat, lon, height = src.get_xyz(rinex_file_path)

#             if pbar.n == 0:

#                 # Create JSON for GNSS-IR (1.st iteration only)
#                 input_orig = src.create_gnssir_input_class(lat=lat, lon=lon, height=height, 
#                                                            e1=2, e2=12, h1=4.0, h2=15.0, nr1=4.0, 
#                                                            nr2=15.0, peak2noise=2.7, ampl=6.0, 
#                                                            frlist="1 20 5 101 102 201 205 206 207 302 306", 
#                                                            azlist2 = "150 250"
#                                                            )
#                 src.create_json(station_id, lat, lon, height, input_orig)

#             # Run GNSS-IR calculation
#             run_gnssIR(station_id, year, doy)
#             pbar.update(1)




# refl_zones dmht -lat 76.76853 -lon -18.670557 -height 43.222 -el_list 2 7 15 -azlist 110 190