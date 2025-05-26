from sqlalchemy import Table, Column, Integer, String, DateTime
from db import metadata
import datetime

link_table = Table(
    "links",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("original_url", String, nullable=False),
    Column("short_code", String, unique=True, index=True),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
    Column("clicks", Integer, default=0),
)
