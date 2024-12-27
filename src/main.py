import os, time, yaml
from contextlib import asynccontextmanager
from CosmBot import CosmBot
    

import logger 
log = logger.getLogger("main")  

def main():
    start=False      
    # Load configuration from YAML file
    # Check if the directory exists, if not, create it
    directory_path = f"{os.environ['RESOURCE_PATH']}/CosmWebex-config.yaml"       
    log.info("wainting for the start flag to be set to True on the config file")
    while not start:  
        with open(f"{directory_path}", 'r') as file:
            config = yaml.safe_load(file)
            start = config['start']     
        if start:
            break
        time.sleep(60)
    
   
    cosm_bot = CosmBot(config) 
    cosm_bot.bot_start()
    # while True:
    #     time.sleep(60)
                
if __name__ == "__main__":
    main()