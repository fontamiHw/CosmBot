#!/bin/bash

docker run --network Cosm-net --ip 10.58.1.11 -v /home/civico129/MyProject/COSM-webex/host:/app/host --name CosmBot cosm-bot
# docker run -v /home/civico129/MyProject/COSM-webex/host:/app/host --name CosmBot cosm-bot
