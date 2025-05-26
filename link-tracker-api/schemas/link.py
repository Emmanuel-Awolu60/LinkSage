from pydantic import BaseModel, HttpUrl

class LinkCreate(BaseModel):
    original_url: HttpUrl

class LinkResponse(BaseModel):
    original_url: HttpUrl
    short_url: str
