
export APPLOGS="./host/logs"
export RESOURCE_PATH="./host/resources"

cp CosmWebex-config.yaml ${RESOURCE_PATH}/CosmWebex-config.yaml
python3 src/main.py
