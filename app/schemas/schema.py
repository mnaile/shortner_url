from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UrlSchema(BaseModel):

    url: str


class ShortnerUrlData(UrlSchema):
    expire_day: Optional[int]


class ShortnerUrlSchema(BaseModel):

    id: UUID
    short_url: str
    url: str
    expire_time: datetime
    created: datetime

    class Config:
        orm_mode = True
