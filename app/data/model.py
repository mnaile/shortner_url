from app.core.dbsetup import Model, db


class UrlShortner(Model):
    __tablename__ = "url_shortner"

    short_url = db.Column(db.String(), nullable=False, index=True)
    url = db.Column(db.String(), nullable=False)
    expire_time = db.Column(db.DateTime())
