#!/bin/bash

########### PREPARE MOUNTED VOLUME ###########
echo "Creating mounted directories"
mkdir -p ${APPLOGS} 
mkdir -p ${RESOURCE_PATH}

########### PREPARE CONFIG IN MOUNTED VOLUME ###########
echo "move resource files int the mounted path"
filename="CosmWebex-config.yaml"
# Variables for source and destination directories
source_file=${TMP_RESOURCE_PATH}/${filename}
destination_dir=${RESOURCE_PATH} 

# Check if the file already exists in the destination directory
if [ ! -e "$destination_dir/$filename" ]; then
    # Copy the file to the destination directory
    cp "$source_file" "$destination_dir/"
    echo "File '$filename' copied to '$destination_dir'."
else
    echo "File '$filename' already exists in '$destination_dir'. No action taken."
fi
echo
echo "show mounted volume"
ls -latR /app/host
echo

########### ENVIROMENT ###########
export PATH="$APP_COSM_PATH:$PATH"
echo "show enviroment variable"
env
echo

########### START APPLICATION ###########
echo "moving in ${APP_COSM_PATH}"
cd ${APP_COSM_PATH}
pwd
echo "Cosm Webex Starting....."
python3 main.py
#python3 clientTest.py
