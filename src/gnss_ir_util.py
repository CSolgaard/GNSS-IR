#!/usr/bin/env python3

import os 
import subprocess
from tqdm import tqdm
import numpy as np
import re
from dataclasses import dataclass, asdict
from pprint import pprint


def load_Rinex_files(rinex3_path): 
    rinex3_files = [f for f in os.listdir(rinex3_path) if f.endswith('.gz')]
    return rinex3_files

def get_info(rinex3_file): 
    info = rinex3_file.split("_")
    station_id = info[0][0:4].lower()
    year = info[2][0:4]
    doy = info[2][4:7]
    return station_id, year, doy

def run_convert_rinex3_2(rinex3_file):
    # Convert Rinex3 -> Rinex2 using rinex3_rinex2
    rinex3_command = f"rinex3_rinex2 {rinex3_file}"
    subprocess.run(rinex3_command, check=True, shell=True)

def determine_new_path(rinex3_file): 
    new_path = rinex3_file.split(".")
    if new_path[-2] == "crx" or new_path[-1] == "gz": 
        rinex_file_path = new_path[0] + ".rnx"
    else:
        rinex_file_path = rinex3_file
    return rinex_file_path

class wgs84:
    """
    wgs84 parameters for Earth radius and flattening
    """
    a = 6378137. # meters Earth radius
    f  =  1./298.257223563 # flattening factor
    e = np.sqrt(2*f-f**2) # 

def xyz2llhd(xyz):
    """
    Converts cartesian coordinates to latitude,longitude,height

    Parameters
    ----------
    xyz : three vector of floats
        Cartesian position in meters

    Returns
    -------
    lat : float
        latitude in degrees

    lon : float
        longitude in degrees

    h : float
        ellipsoidal height in WGS84 in meters

    """
    x=xyz[0]
    y=xyz[1]
    z=xyz[2]
    lon = np.arctan2(y, x)
    p = np.sqrt(x**2+y**2)
    lat0 = np.arctan((z/p)/(1-wgs84.e**2))
    b = wgs84.a*(1-wgs84.f)
    error = 1
    a2=wgs84.a**2
    i=0 # make sure it doesn't go forever
    tol = 1e-10
    while error > tol and i < 6:
        n = a2/np.sqrt(a2*np.cos(lat0)**2+b**2*np.sin(lat0)**2)
        h = p/np.cos(lat0)-n
        lat = np.arctan((z/p)/(1-wgs84.e**2*n/(n+h)))
        error = np.abs(lat-lat0)
        lat0 = lat
        i+=1
    return lat*180/np.pi, lon*180/np.pi, h


def extract_approx_xyz_from_rinex_file(file_path):
    with open(file_path, 'r') as rinex_file:
        header_lines = []
        for line in rinex_file:
            if "APPROX POSITION XYZ" in line:
                # Extract the XYZ values using a regular expression
                match = re.search(r'\s*([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)', line)
                if match:
                    x, y, z = map(float, match.groups())
                    return x, y, z
            header_lines.append(line)  # Store header lines in case you need them

    return None

def get_xyz(rinex_file_path): 
    xyz = extract_approx_xyz_from_rinex_file(rinex_file_path)
    if xyz is not None:
        x, y, z = xyz
        print(f"Approximate Position XYZ: x={x}, y={y}, z={z}")
    else:
        print("Approximate Position XYZ not found in the Rinex file.")
        lat = input("Input the Latitude for the reciever: ")
        lon = input("Input the Longitude for the reciever: ")
        height = input("Input the reciever height (Ellipsoidal, H): ")

    lat, lon, height = xyz2llhd(xyz)
    return lat, lon, height


def create_gnssir_input_class(lat, lon, height, e1, e2, h1, h2, nr1, nr2, peak2noise, ampl, frlist, azlist2): 
    @dataclass
    class gnssir_input_class:
        lat: str
        lon: str
        height: str
        e1: str
        e2: str
        h1: str
        h2: str 
        nr1: str 
        nr2: str 
        peak2noise: str
        ampl: str 
        frlist: str 
        azlist2: str

    return gnssir_input_class(lat=lat, lon=lon, height=height, e1=e1, e2=e2, h1=h1, h2=h2, nr1=nr1, nr2=nr2, peak2noise=peak2noise, ampl=ampl, frlist=frlist, azlist2=azlist2)


def create_json(station_id, lat, lon, height, input_orig):
    # @dataclass
    # class gnssir_input_class:
    #     lat: str
    #     lon: str
    #     height: str
    #     e1: str
    #     e2: str
    #     h1: str
    #     h2: str 
    #     nr1: str 
    #     nr2: str 
    #     peak2noise: str
    #     ampl: str 
    #     frlist: str 
    #     azlist2: str

    # input_orig = gnssir_input_class(lat=lat, lon=lon, height=height, 
    #                                 e1=2, e2=12, h1=4.0, h2=15.0, nr1=4.0, 
    #                                 nr2=15.0, peak2noise=2.7, ampl=6.0, 
    #                                 frlist="1 20 5 101 102 201 205 206 207 302 306", 
    #                                 azlist2 = "150 250")
    
    gnssir_input_dict = asdict(input_orig)

    print("...")
    print("Used GNSS-IR input parameters:")
    pprint(gnssir_input_dict)
    print("...")

    # refl_zones dmht -lat 76.76853 -lon -18.670557 -height 43.222 -el_list 2 7 15 -azlist 110 190
    gnssir_input_command = f"gnssir_input {station_id} -lat {lat} -lon {lon} -height {height} -e1 {input_orig.e1} -e2 {input_orig.e2} -h1 {input_orig.h1} -h2 {input_orig.h2} -nr1 {input_orig.nr1} -nr2 {input_orig.nr2} -peak2noise {input_orig.peak2noise} -ampl {input_orig.ampl} -frlist {input_orig.frlist} -azlist2 {input_orig.azlist2}"
    subprocess.run(gnssir_input_command, check=True, shell=True)
    return

def run_gnssIR(station_id, year, doy):
    gnssir_command = f"gnssir {station_id} {year} {doy} -snr 66"
    subprocess.run(gnssir_command, check=True, shell=True)
    return