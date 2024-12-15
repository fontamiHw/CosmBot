import os, time, yaml
import threading

from contextlib import asynccontextmanager

from fastapi import FastAPI
from CosmBot import CosmBot
from servers.web.fastapiServer import WebServer



@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"lifespan started")  
    
    main_thread = threading.Thread(target=main_run)
    main_stop_event = threading.Event()
    main_thread.start()
    yield
    print(f"lifespan completed")

def main_run():
    webServer = WebServer(app)
    cosm_bot = CosmBot(webServer, config) 
    cosm_bot.bot_start()


start=False      
# Load configuration from YAML file
# Check if the directory exists, if not, create it
directory_path = f"{os.environ['RESOURCE_PATH']}/config.yaml"       
            
while not start:       
    time.sleep(5)
    with open(f"{directory_path}", 'r') as file:
        config = yaml.safe_load(file)
        start = config['start']
                
app = FastAPI(lifespan=lifespan)
