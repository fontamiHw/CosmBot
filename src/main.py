import os, time, yaml
import threading
from CosmBot import CosmBot
from CosmException import CosmException
import logger


start=False      
# Load configuration from YAML file
# Check if the directory exists, if not, create it
directory_path = f"{os.environ['RESOURCE_PATH']}/CosmWebex-config.yaml"       
log = logger.getLogger()

            
while not start:   
    with open(f"{directory_path}", 'r') as file:
        config = yaml.safe_load(file)
        start = config['start']   
    if not start: 
        time.sleep(30)
        
    try:
        cosm_bot = CosmBot(config) 
        cosm_bot.bot_start()
    except CosmException as e:
        log.error(f"Application error: {e}")