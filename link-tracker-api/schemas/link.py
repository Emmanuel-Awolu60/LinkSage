from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class LinkCreate(BaseModel):
    original_url: HttpUrl
    custom_code: Optional[str] = None
    expires_at: Optional[datetime] = None

class LinkResponse(BaseModel):
    original_url: HttpUrl
    # short_url: str
    custom_code: Optional[str] = None