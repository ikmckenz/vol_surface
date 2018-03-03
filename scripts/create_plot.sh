#!/bin/bash
echo "Saving data, creating plot at $(date)"
cd /home/ubuntu/vol_surface
python3 vol_surface.py
# Move data over
/home/ubuntu/.local/bin/aws s3 mv /home/ubuntu/vol_surface/saved_data s3://optionsdatafromyahoo --exclude '*' --include '*.csv' --recursive
# Save IV image
/home/ubuntu/.local/bin/aws s3 cp /home/ubuntu/vol_surface/pictures s3://optionsdatafromyahoo/pics --exclude '*' --include '*.png' --recursive
# Update main IV image
/home/ubuntu/.local/bin/aws s3 mv pictures/* s3://optionsdatafromyahoo/iv.png --acl public-read
