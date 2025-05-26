from pydantic import BaseModel, HttpUrl

class LinkCreate(BaseModel):
    original_url: HttpUrl

class LinkResponse(BaseModel):
    original_url: str
    short_url: str
