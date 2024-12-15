import os, time, yaml
import threading
from CosmBot import CosmBot


start=False      
# Load configuration from YAML file
# Check if the directory exists, if not, create it
directory_path = f"{os.environ['RESOURCE_PATH']}/config.yaml"       
            
while not start:       
    time.sleep(5)
    with open(f"{directory_path}", 'r') as file:
        config = yaml.safe_load(file)
        start = config['start']
        
cosm_bot = CosmBot(None, config) 
cosm_bot.bot_start()
                


