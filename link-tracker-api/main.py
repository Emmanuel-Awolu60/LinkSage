# from fastapi import FastAPI
from db import database, engine, metadata
from models.link import link_table
from schemas.link import LinkCreate, LinkResponse
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy import update
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import delete
import secrets
import os

metadata.create_all(engine)
BASE_URL = os.getenv("BASE_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Connected to database")
    yield
    await database.disconnect()
    print("Disconnected from database")

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/shorten", response_model=LinkResponse)
async def shorten_link(link: LinkCreate, request: Request):
    # to generate unique short code
    short_code = link.custom_code or secrets.token_urlsafe(5)[:6]

    # to check if it already exists
    query = link_table.select().where(link_table.c.short_code == short_code)
    existing = await database.fetch_one(query)

    if existing:
        raise HTTPException(status_code=400, detail="Short code already exists. Try again.")
    
    # to insert into database
    insert_query = link_table.insert().values(
        original_url = str(link.original_url), 
        short_code = short_code,
        expires_at = link.expires_at
    )
    await database.execute(insert_query)

    # Dynamic base URL
    # base_url = str(request.base_url)
    short_url =f"{str(request.bas_url)}{short_code}"
    return{
        "original_url": str(link.original_url),
        "short_url": short_url,
        "expires_at": link.expires_at
     }
    short_url = f"{BASE_URL}/{short_code}"

@app.get("/{short_code}")
async def redirect_to_original(short_code: str):
    query = link_table.select().where(link_table.c.short_code == short_code)
    link = await database.fetch_one(query)

    if link is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    expires_at = link["expires_at"]
    if expires_at and expires_at < datatime.utcnow():
        raise HTTPException(status_code=404, detail="Short URL has expired")

    # Update the click count
    update_query = (
        update(link_table)
        .where(link_table.c.short_code == short_code)
        .values(clicks=(link["clicks"] or 0) + 1)
    )
    await database.execute(update_query)

    return RedirectResponse(url=link["original_url"])




@app.get("/stats/{short_code}")
async def get_stats(short_code: str):
    query = link_table.select().where(link_table.c.short_code == short_code)
    link = await database.fetch_one(query)

    if link is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return{
        "original_url": link["original_url"],
        "short_code": link["short_code"],
        "clicks": link["clicks"]
    }


@app.delete("/delete/{short_code}")
async def delete_link(shortt_code: str):
    # to check if the short link exists
    query = link_table.select().where(link_table.c.short_code == shortt_code)
    existing = await database.fetch_one(query)

    if not existing:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    # Proceed to delete
    delete_query = link_table.delete().where(link_table.c.short_code == shortt_code)
    await database.execute(delete_query)

    return {"message": "Short URL deleted successfully"}