#!/bin/bash

# set base paths: customize as needed,
# or comment out if you already set these up as global environment variables
export NSDS_METADATA_PATH="${HOME}/Src/NSDSLab-NWB-metadata/"
export NSDS_DATA_PATH='/clusterfs/NSDS_data/hackathon20201201/TTankBackup/'
export NSDS_STIMULI_PATH='/clusterfs/NSDS_data/hackathon20201201/Stimuli/'

SAVE_PATH="_test/"
BLOCK_NAME="RVG02_B09"
BLOCK_META="../tests/_data/RVG02/block_data.csv"

python generate_nwb.py  $SAVE_PATH $BLOCK_NAME $BLOCK_META
