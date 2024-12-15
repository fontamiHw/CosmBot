#!/bin/bash

# Check if the number of arguments is exactly 2
if [ $# -eq 1 ]; then
#  docker volume create --driver local --opt type=none --opt device=$1 --opt o=bind $2
#  docker run --mount type=volume,src=$2,dst=/app/resources --name CosmBot cosm-bot
  docker run -v $1:/app/host --name CosmBot cosm-bot
else
  echo
  echo "------------------------------------------------------------------"
  echo "Incorrect number of arguments."
  echo "The mount volume where there is the config.yaml file is mandatory."
  echo "------------------------------------------------------------------"
  echo
fi
