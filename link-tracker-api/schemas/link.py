from pydantic import BaseModel, HttpUrl

class LinkCreate(BaseModel):
    original_url: HttpUrl

class LinkRespone(BaseModel):
    original_url: str
    short_url: str