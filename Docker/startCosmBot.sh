#!/bin/bash

export RESOURCE_PATH="host/resources"
# Path to the YAML file
yaml_file="${RESOURCE_PATH}/CosmWebex-config.yaml"

# Use yq to extract the value of 'port'
CONTAINERCOMM_PORT=$(yq eval '.container_communication.port' "$yaml_file")

echo "docker run --network Cosm-net --ip 10.58.1.11 -p ${CONTAINERCOMM_PORT}:${CONTAINERCOMM_PORT} -v /home/civico129/MyProject/COSM-webex/host:/app/host --name CosmBot cosm-bot"
docker run --network Cosm-net --ip 10.58.1.11 -p ${CONTAINERCOMM_PORT}:${CONTAINERCOMM_PORT} -v /home/civico129/MyProject/COSM-webex/host:/app/host --name CosmBot cosm-bot
