import logging
import os
import yaml


log = logging.getLogger("builderProcess")
log.setLevel(logging.INFO)

with open(f"{os.environ['RESOURCE_PATH']}/CosmWebex-config.yaml", 'r') as file:
    config = yaml.safe_load(file)
                
# Create a file handler
handler = logging.FileHandler(f"{os.environ['APPLOGS']}/{config['logs']['webex-log']}")
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
log.addHandler(handler)


def getLogger():
    return log