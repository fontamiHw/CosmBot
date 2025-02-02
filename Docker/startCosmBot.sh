#!/bin/bash
HOST="/data/COSM-bot"  # write here the path of mounted volume
export APPLOGS="${HOST}/logs"
export RESOURCE_PATH="${HOST}/resources"
export APP_PR_FILES="${HOST}/files"
export SUPERVISOR_LOGS="${APPLOGS}/supervisord"

# must be identical to the one in CosmWeb-config.yaml
export DATABASE_PATH="/app/database"  

mkdir -p ${HOST}

mkdir -p ${APPLOGS}
mkdir -p ${RESOURCE_PATH}
mkdir -p ${APP_PR_FILES} 
mkdir -p ${SUPERVISOR_LOGS}
https_proxy=http://proxy.esl.cisco.com:80
NO_PROXY=.cisco.com
HTTPS_PROXY=http://proxy.esl.cisco.com:80
HTTP_PROXY=http://proxy.esl.cisco.com:80
http_proxy=http://proxy.esl.cisco.com:80


echo "docker run -d \
             --network Cosm-net \
             --hostname CosmBot \
             -e https_proxy \
             -e NO_PROXY \
             -e HTTPS_PROXY \
             -e HTTP_PROXY \
             -e http_proxy \
             -v $HOST:/app/host \
             --mount type=volume,src=CosmVolume,dst=$DATABASE_PATH \
             --name CosmBot \
             cosm-bot"
             
docker run -d \
             --network Cosm-net \
             --hostname CosmBot \
             -e https_proxy \
             -e NO_PROXY \
             -e HTTPS_PROXY \
             -e HTTP_PROXY \
             -e http_proxy \
             -v $HOST:/app/host \
             --mount type=volume,src=CosmVolume,dst=$DATABASE_PATH \
             --name CosmBot \
             cosm-bot