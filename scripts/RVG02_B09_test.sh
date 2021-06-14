#!/bin/bash

echo "Warning: metadata format for block RVG02_B09 is outdated."
echo "This end-to-end test is expected to fail."

SAVE_PATH="_test/"
BLOCK_NAME="RVG02_B09"
BLOCK_META="${NSDS_DATA_PATH}/RVG02/block_data.csv"

python generate_nwb.py  $SAVE_PATH $BLOCK_NAME $BLOCK_META
