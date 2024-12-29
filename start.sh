
export APPLOGS="./host/logs"
export RESOURCE_PATH="./host/resources"
export APP_PR_FILES="./host/pr"

mkdir -p ${APPLOGS}
mkdir -p ${RESOURCE_PATH}
mkdir -p ${APP_PR_FILES}
rm -rf ${APPLOGS}/*
rm -rf ${RESOURCE_PATH}/*
rm -rf ${APP_PR_FILES}/*

cp CosmWebex-debug-config.yaml ${RESOURCE_PATH}/CosmWebex-config.yaml
python3 src/main.py
