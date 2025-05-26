from fastapi import FastAPI
from db import database, engine, metadata
from models.link import link_table

app = FastAPI()

# Create the table
metadata.create_all(engine)

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def disconnect():
    await database.disconnect()

@app.get("/ping")
def ping():
    return {"message": "pong"}
