#!/bin/bash

source ./.enviroment
echo "PYTHONPATH = ${PYTHONPATH}"
echo "PATH       = ${PATH}"

echo "moving in /app/CosmBot"
cd /app/CosmBot
pwd

echo "python version is"
python --version

echo "Cosm Webex Starting....."
python3 CosmBot.py