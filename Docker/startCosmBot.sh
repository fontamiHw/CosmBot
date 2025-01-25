#!/bin/bash
HOST="/data/COSM-bot"  # write here the path of mounted volume
export APPLOGS="${HOST}/logs"
export RESOURCE_PATH="${HOST}/resources"
export APP_PR_FILES="${HOST}/pr"
export SUPERVISOR_LOGS="${APPLOGS}/supervisord"

mkdir -p ${HOST}

mkdir -p ${APPLOGS}
mkdir -p ${RESOURCE_PATH}
mkdir -p ${APP_PR_FILES}
mkdir -p ${SUPERVISOR_LOGS}


echo "docker run -d --network Cosm-net --hostname CosmBot -v $HOST:/app/host --mount type=volume,src=CosmVolume,dst=/app/database --name CosmBot cosm-bot"
      docker run -d --network Cosm-net --hostname CosmBot -v $HOST:/app/host --mount type=volume,src=CosmVolume,dst=/app/database --name CosmBot cosm-bot
