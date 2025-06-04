from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, AnyHttpUrl


class LinkCreate(BaseModel):
    original_url: AnyHttpUrl
    custom_code: Optional[str] = None
    expires_at: Optional[datetime] = None

class LinkResponse(BaseModel):
    original_url: AnyHttpUrl
    short_url: str
    custom_code: Optional[str] = None