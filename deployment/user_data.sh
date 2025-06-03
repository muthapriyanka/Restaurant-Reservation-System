#!/bin/bash

# Make mountpath
sudo mkdir /data

# Mount device xvdh file system to created mountpath
sudo mount /dev/xvdf /data

# Run the script stored on dir, REQUIRES THE DEVICE TO BE FORMATTED, MOUNTED, AND THE FILE TO BE MOVED TO THE DIRECTORY
chmod 755 /data/install_apache.sh
sh /data/install_apache.sh
