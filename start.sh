
export APPLOGS="./host/logs"
export RESOURCE_PATH="./host/resources"

rm -rf ${APPLOGS}/*

cp CosmWebex-debug-config.yaml ${RESOURCE_PATH}/CosmWebex-config.yaml
python3 src/main.py
