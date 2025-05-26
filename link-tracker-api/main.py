from fastapi import FastAPI
from db import database, engine, metadata
from models.link import link_table
from schemas.link import LinkCreate, LinkRespone
from contextlib import asynccontextmanager
import secrets

metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("✅ Connected to database")
    yield
    await database.disconnect()
    print("🔌 Disconnected from database")

app = FastAPI(lifespan=lifespan)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/shorten", response_model=LinkRespone)
async def shorten_link(link: LinkCreate):
    # To generate unique short code
    short_code = secrets.token_urlsafe(5)[:6]

    # To check if it already exists
    query = link_table.select().where(link_table.c.short_code == short_code)
    existing = await database.fetch_one(query)

    if existing:
        raise HTTPException(status_code=400, detail="Short code already exists. Try again.")
    
    # To insert into database
    insert_query = link_table.insert().values(
        original_url = str(link.original_url), 
        short_code = short_code,
    )
    await database.execute(insert_query)

    # To return the result
    short_url = f"http://localhost:8000/{short_code}"
    return{"original_url": str(link.original_url), "short_url": short_url}
