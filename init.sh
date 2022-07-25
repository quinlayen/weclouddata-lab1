#!/bin/bash

# Description
# Entry point for WeCloudData Lab2

# Install specific python version to amke sure all the work for various servers are the same
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt install python3.8 -y
sudo apt install python3.8-distutils -y

# Install awscli
sudo apt install awscli -y

# Create a virtual environment
sudo apt install python3-virtualenv -y
virtualenv --python="/usr/bin/python3.8" sandbox
source sandbox/bin/activate

# Install dependencies
pip install -r requirements.txt
deactivate

chmod a+x run.sh
mkdir -p log