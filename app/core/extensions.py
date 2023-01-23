from gino.ext.starlette import Gino
from passlib.context import CryptContext

from app.config import settings

db = Gino(
    dsn=settings.DATABASE_URL,
    pool_min_size=3,
    pool_max_size=7,
    retry_limit=3,
    retry_interval=1,
)


pwd_context = CryptContext(schemes="sha256_crypt", deprecated="auto")
