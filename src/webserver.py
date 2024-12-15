from contextlib import asynccontextmanager

from fastapi import FastAPI
from CosmBot import CosmBot

cosm_botinit=False

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("chiamato")
    cosm_bot = CosmBot()
    cosm_botinit=True
    yield
    pass


app = FastAPI(lifespan=lifespan)


@app.get("/predict")
async def predict(x: float):
    return {"result": recosm_botinitsult}