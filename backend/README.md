# Backend (FastAPI)

## Requirements
- Python 3.12
- Poetry

## Local development (without Docker)
```bash
    poetry install
    export DATABASE_URL="postgresql+psycopg2://miseventos:miseventos@localhost:5432/miseventos"
    export SECRET_KEY="changeme"
    uvicorn app.main:app --reload
```

## Migrations
```bash
  alembic upgrade head
```

## Evidence
```bash
  pytest -q
```