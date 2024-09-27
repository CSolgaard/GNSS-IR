# Automatication of GNSS-IR Estimation of Tide in Greenland. 

This project focuses on calculating reflector heights of GNSS stations in Greenland, which are used for tide estimations. The GNSS stations used in this project are primarily part of the **GNET (Greenland GNSS Network)**, a project maintained by **DTU SPACE** and **Klima Data Styrelsen (KDS)**.

## Project Overview

The repository contains a shell script, `Run_GNSS_IR.sh`, that automates the GNSS-IR (Global Navigation Satellite System - Interference Reflection) calculations through a series of Python scripts. The purpose is to compute reflector heights from the SNR (Signal-to-Noise Ratio) data of GNSS signals. These reflector heights are then used to estimate tidal variations in the regions around the stations.

## Repository Contents

- **`Run_GNSS_IR.sh`**: This is the main script for running the GNSS-IR calculations. It serves as an interface for executing several Python scripts in sequence, which perform data processing, calculation, and analysis.

## Usage

To run the `Run_GNSS_IR.sh` script, navigate to the project directory and use the following command in the terminal:

```bash
./Run_GNSS_IR.sh
```
You will be prompted to enter the following details:

- **Station ID** (e.g., `NORD`): A unique identifier for the GNSS station.
- **Year** (e.g., `2024`): The year for which the calculations will be performed.
- **Start DOY** (Day of Year, e.g., `140`): The starting day of the year for the analysis.
- **End DOY** (Day of Year, e.g., `145`): The ending day of the year for the analysis.

After providing the required input, the script will execute the GNSS-IR calculations for the specified station and time range.

## Dependencies

- **Bash**
- **Python 3.x**
- Required Python libraries: `numpy`, `matplotlib`, etc.
- GNSS processing tools: `gfzrnx`, `CRX2RNX`, etc.

Make sure to install all necessary dependencies before running the script.

## Acknowledgments

This project utilizes GNSS stations from the **GNET (Greenland GNSS Network)**, which is a collaborative effort maintained by **DTU SPACE** and **Klima Data Styrelsen (KDS)**. We are grateful for their continued support and for providing the necessary data for these calculations.
