import os, time, yaml
import logger
from contextlib import asynccontextmanager

from CosmBot import CosmBot


def main():
    log = logger.getLogger()
    start=False      
    # Load configuration from YAML file
    # Check if the directory exists, if not, create it
    directory_path = f"{os.environ['RESOURCE_PATH']}/CosmWebex-config.yaml"       
            
    while not start:  
        with open(f"{directory_path}", 'r') as file:
            config = yaml.safe_load(file)
            start = config['start']     
        if start:
            break
        time.sleep(5)
    
   
    cosm_bot = CosmBot(config, log) 
    cosm_bot.bot_start()
                
if __name__ == "__main__":
    main()