from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.extensions import db


class SurrogatePK(object):
    """A mixin that adds a surrogate UUID 'primary key' column named ``id`` to
    any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}

    id = db.Column(UUID(), primary_key=True, default=uuid4)
    created = db.Column(db.DateTime(timezone=True), default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class Model(db.Model, SurrogatePK):
    __abstract__ = True

    @classmethod
    async def exists(cls, *args):
        obj = await cls.query.where(*args).gino.first()
        return bool(obj)

    @classmethod
    async def create(cls, **kwargs):
        if issubclass(cls, SurrogatePK):
            unique_id = uuid4()
            if not kwargs.get("id"):

                kwargs["id"] = unique_id
        return await cls(**kwargs)._create()
