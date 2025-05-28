from pydantic import BaseModel, HttpUrl
from typing import Optional

class LinkCreate(BaseModel):
    original_url: HttpUrl

class LinkResponse(BaseModel):
    original_url: HttpUrl
    # short_url: str
    custom_code: Optional[str] = None