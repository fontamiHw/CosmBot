import logging
import os
import yaml


def getLogger(name="builderProcess"):

    with open(f"{os.environ['RESOURCE_PATH']}/CosmWebex-config.yaml", 'r') as file:
        config = yaml.safe_load(file)
        
    log = logging.getLogger(name)
    log.setLevel(config['logs']['level'])
                
    # Create a file handler
    handler = logging.FileHandler(f"{os.environ['APPLOGS']}/{config['logs']['webex-log']}")
    handler.setLevel(config['logs']['level'])

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    log.addHandler(handler)
    return log