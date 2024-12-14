#!/bin/bash

# Check if the number of arguments is exactly 2
if [ $# -eq 2 ]; then
#  docker volume create --driver local --opt type=none --opt device=$1 --opt o=bind $2
#  docker run --mount type=volume,src=$2,dst=/app/resources --name CosmBot cosm-bot
  docker run -v $1:/app/resources --name CosmBot cosm-bot
else
  echo "Incorrect number of arguments. You need exactly 2 arguments."
fi
