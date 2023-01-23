import random
import string
import time
from datetime import datetime, timedelta

from fastapi.exceptions import HTTPException

from app.config import settings
from app.data.model import UrlShortner


class ShortnerUrlService:
    async def create_shortner_url(self, data):
        url = data.url
        expire_day = data.expire_day

        if expire_day:
            if expire_day >= 1 and expire_day <= 365:
                expire_day = datetime.now() + timedelta(days=expire_day)
            else:
                raise HTTPException(
                    status_code=400, detail="Expire day must be between 1 and 365"
                )
        else:
            expire_day = datetime.now() + timedelta(days=90)

        tm = str(time.time())
        index = tm.find(".") - 2
        timestamp = tm[index:]
        timestamp = timestamp.replace(".", random.choice(string.ascii_letters))

        short_url = f"{settings.BASE_SHORT_URL}/{timestamp}"

        record = await UrlShortner.create(
            short_url=short_url, url=url, expire_time=expire_day
        )
        return record

    async def get_url(self, short_url: str):

        records = await UrlShortner.query.where(
            UrlShortner.short_url == short_url
        ).gino.first()

        if not records:
            raise HTTPException(status_code=404, detail="Url not found!")

        diff = records.expire_time - datetime.now()

        if diff.days < 0 or (
            diff.days == 0
            and diff.seconds // 3600 <= 0
            and (diff.seconds // 60) % 60 <= 0
        ):
            raise HTTPException(status_code=400, detail="Url has expired!")

        return {"url": records.url}
