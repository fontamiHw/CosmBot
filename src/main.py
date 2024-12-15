from contextlib import asynccontextmanager

from fastapi import FastAPI
from CosmBot import CosmBot
from servers.web.fastapiServer import WebServer

cosm_botinit=False

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("chiamato")
    cosm_bot = CosmBot(webServer)
    cosm_botinit=True
    yield
    pass


app = FastAPI(lifespan=lifespan)
webServer = WebServer(app)
