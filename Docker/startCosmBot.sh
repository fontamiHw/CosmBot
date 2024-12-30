#!/bin/bash
HOST="../host"
export APPLOGS="${HOST}/logs"
export RESOURCE_PATH="${HOST}/resources"
export APP_PR_FILES="${HOST}/pr"
export SUPERVISOR_LOGS="${APPLOGS}/supervisord"

echo ${SUPERVISOR_LOGS}

mkdir -p ${APPLOGS}
mkdir -p ${RESOURCE_PATH}
mkdir -p ${APP_PR_FILES}
mkdir -p ${SUPERVISOR_LOGS}
ls -laR ${HOST}
rm -rf ${APPLOGS}/*.log
rm -rf ${RESOURCE_PATH}/*.yaml
rm -rf ${APP_PR_FILES}/*
rm -rf ${SUPERVISOR_LOGS}/*.log
cp ../CosmWebex-config.yaml ${RESOURCE_PATH}/CosmWebex-config.yaml


# Path to the YAML file
yaml_file="${RESOURCE_PATH}/CosmWebex-config.yaml"

# Use yq to extract the value of 'port'
CONTAINERCOMM_PORT=$(yq eval '.container_communication.port' "$yaml_file")

echo "docker run -d --network Cosm-net --ip 10.58.1.11 -v /home/civico129/MyProject/COSM-webex/host:/app/host --mount type=volume,src=CosmVolume,dst=/app/database --name CosmBot cosm-bot"
      docker run -d --network Cosm-net --ip 10.58.1.11 -v /home/civico129/MyProject/COSM-webex/host:/app/host --mount type=volume,src=CosmVolume,dst=/app/database --name CosmBot cosm-bot
