This service to shorten long URLs to short ones without losing its value.


For development with pip:

```sh
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

For database migrations:
```
alembic revision --autogenerate

alembic upgrade heads
```

For run the server:
```
uvicorn app.main:app --reload
```

Interactive API docs:
```
http://127.0.0.1:8000/api/v1/docs
```