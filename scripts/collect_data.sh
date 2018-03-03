#!/bin/bash
echo "Collecting data at $(date)"
cd /home/ubuntu/vol_surface
python3 src/yahoo_options.py
/home/ubuntu/.local/bin/aws s3 mv /home/ubuntu/vol_surface/saved_data s3://optionsdatafromyahoo --exclude '*' --include '*.csv' --recursive
