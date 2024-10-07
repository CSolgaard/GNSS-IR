#!/bin/bash

# Initialize conda
source /home/csol/anaconda3/etc/profile.d/conda.sh      # Change so that all can run

# Activate virtual environment
conda activate gnssIR

# -------------------- Download Rinex3 files ---------------------

mkdir "TEMP_RINEX_DATA"  # Create Temp data folder

DOWNLOAD_SCRIPT="download_Rinex.py"

echo "Downloading Rinex3 files"

# Run the Python script interactively
python "$DOWNLOAD_SCRIPT"

# Read the station ID from the file written by the Python script
STATION_ID=$(cat /tmp/station_id.txt)


# ----------------------------------------------------------------

# Directory containing the Python script. 
SCRIPT_DIR="/mnt/c/Users/csol/GNSS_IR/src"        # Change to relative

# Change to the script directory 
cd "$SCRIPT_DIR"

# Ensure a station ID is provided
if [ -z "$STATION_ID" ]; then
  echo "Error: Station ID not provided."
  exit 1
fi

# Python script path, based on the station ID
PYTHON_SCRIPT="$SCRIPT_DIR/${STATION_ID}.py"

echo $PYTHON_SCRIPT

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: GNSS-IR Python script for station ID '$STATION_ID' not found."
  exit 1
fi

# Run the Python script
python "$PYTHON_SCRIPT"

conda deactivate 

# Remove the temp directory for Rinex3 data. 
rm -rf "/mnt/c/Users/csol/GNSS_IR/src/TEMP_RINEX_DATA"        # Change to relative

echo ">>  Done processing GNSS-IR for '$STATION_ID'"