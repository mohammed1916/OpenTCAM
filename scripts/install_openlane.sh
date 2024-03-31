#!/bin/bash

# Check if the system is Ubuntu
if [ -f /etc/os-release ]; then
    source /etc/os-release
    if [ "$ID" == "ubuntu" ]; then
        # Download and execute the script from the gist
        curl -sSL https://gist.github.com/zeeshanrafique23/11dbef9b83075b06b9ec90fddb8dc96f/raw/install_openlane_ubuntu.sh | bash
        exit 0
    fi
fi

if ! command -v docker &> /dev/null; then
    echo -e "Docker is not installed. Please install Docker and re-run this script. \nInstallation instructions: \nInstall Docker https://docs.docker.com/get-docker/ or \ninstall Docker Engine https://docs.docker.com/engine/install/"
    exit 1
else
    echo "Docker is installed. Proceeding with the installation."
fi

# # Clone the OpenLane repository
if [ -d "openlane" ]; then
    echo "OpenLane directory already exists. Using the existing directory."
else
    git clone https://github.com/The-OpenROAD-Project/OpenLane
fi

# Enter the OpenLane directory
cd openlane

# Install the required dependencies
make openlane
make pdk
make test

