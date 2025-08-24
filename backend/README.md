# Events Backend (FastAPI)

> Production-ready FastAPI backend for **Mis Eventos** – created from the Python Developer Technical Test.

## ✨ Highlights

- **Tech**: FastAPI, SQLAlchemy 2, Pydantic v2, Alembic, PostgreSQL, Poetry, JWT auth
- **Domain**: Events, Sessions, Speakers, Registrations, Users
- **Auth**: Email + password (JWT bearer); protected routes for create/update actions
- **Search & Pagination**: Event listing supports `search`, `page`, `size`
- **DX**: OpenAPI docs, GZip, CORS, `.env` config
- **Migrations**: Alembic (baseline revision included)

---

## 🧱 Architecture

```
├── alembic/                        # Alembic env + versions (initial migration)
├── app                             # Contains the main application files.
│   ├── core/                       # settings, db engine/session, security, pagination, exceptions
│   ├── crud/                       # Data-access functions
│   ├── dependencies/               # DI helpers (DB session, current user)
│   ├── models/                     # SQLAlchemy ORM models (User, Event, Session, Speaker, Registration, Enums)
│   ├── routers/                    # FastAPI routers (auth, users, events, sessions, speakers, registrations)
│   ├── schemas/                    # Pydantic models (request/response DTOs)
│   ├── services/                   # Business logic
│   ├── tests/                      # Test suite
│   ├── api.py                      # App factory, middlewares, router mounting
│   └── main.py                     # Uvicorn entry
├── .evenv.example                  # Environment variables
├── alembic.ini                     # Alembic config
├── README.md                       # README
├── poetry.lock                     # Poetry lock
└── pyproject.toml                  # Poetry config
```

---

## 📦 Requirements

- **Python** 3.12+
- **PostgreSQL** 14+
- **Poetry** 1.8+
- (Opcional) Docker y Docker Compose

---

## ⚙️ Configuration

Create a `.env` in `backend/` (you can copy `.env.example`):

```env
# Database and security settings
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/events
SECRET_KEY=secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment and debug settings
ENV=dev
DEBUG=true

# API settings
API_V1_PREFIX=/api/v1
CORS_ORIGINS='["http://localhost:5173", "http://localhost:3000"]'
ALLOW_HOSTS='["localhost", "127.0.0.1"]'
DOCS_ENABLED=true
GZIP_ENABLED=true
```

> In `ENV=dev`, the app auto-creates tables on startup (for quick local use). For real environments, use Alembic migrations.

---

## 🚀 Run (Local, no Docker)

```bash
    # from backend/
    poetry install
    
    # configure env
    cp .env.example .env
    # (optionally tweak DATABASE_URL, SECRET_KEY, etc.)
    
    # start your Postgres (ensure database exists)
    # then run the API:
    poetry run uvicorn app.main:app --reload
```

Open:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🐳 Docker
### Build & Run with Docker Compose

```bash
    docker build -t events-api .
    docker run --env-file .env -p 8000:8000 events-api
```

Run with Docker Compose:

```bash
    docker compose up --build
```

---

## 🗃️ Database & Migrations

Initialize / upgrade schema:

```bash
    # from backend/
    poetry run alembic upgrade head
```

Create new migration after model changes:

```bash
    poetry run alembic revision --autogenerate -m "your message"
    poetry run alembic upgrade head
```

---

## 🔐 Authentication

- **Register** → returns a JWT
- **Login** → returns a JWT
- Use `Authorization: Bearer <token>` for protected routes.

Token config:
- HS256 signed, subject = user email
- Expiration = `ACCESS_TOKEN_EXPIRE_MINUTES`

---

## 📚 API Overview (v1)

Base prefix (configurable): **`/api/v1`**

### Auth
- **POST** `/auth/register` → register user (returns token)
- **POST** `/auth/login` → login (returns token)

### Users
- **GET** `/users/me` → current user profile (requires JWT)

### Events
- **GET** `/events` → list with `page`, `size`, optional `search`
- **POST** `/events` → create (requires JWT)
- **GET** `/events/{id}` → retrieve (includes sessions)
- **PATCH** `/events/{id}` → update (requires JWT)
- **DELETE** `/events/{id}` → soft delete (requires JWT)

### Sessions
- **GET** `/sessions?event_id=...` → list sessions for an event
- **POST** `/sessions` → create (requires JWT)
- **PATCH** `/sessions/{id}` → update (requires JWT)
- **DELETE** `/sessions/{id}` → delete (requires JWT)

### Speakers
- **GET** `/speakers?event_id=...` → list speakers (by event)
- **POST** `/speakers` → create (requires JWT)
- **PATCH** `/speakers/{id}` → update (requires JWT)
- **DELETE** `/speakers/{id}` → delete (requires JWT)

### Registrations
- **POST** `/registrations/events/{event_id}` → register current user to event
- **GET** `/registrations/me` → my registrations (requires JWT)

> Capacity and scheduling constraints are enforced in services/CRUD (e.g., available capacity, session times, etc.).

---

## 🔎 Query & Pagination

- Pagination wrapper: `{ items, total, page, size }`
- `GET /events?page=1&size=10&search=conf` → case-insensitive search by event name.

---

## 🧪 Tests

Pytest is configured in `pyproject.toml`. To run:

```bash
    # from backend/
    poetry run pytest -q
```

> At the moment there are no test files in `backend/tests/`. Add unit tests for services and routers to improve coverage.

---

## 🧰 Common Commands

```bash
    # run dev server
    poetry run uvicorn app.main:app --reload
    
    # type-check / lint (add your tools)
    # e.g., ruff / mypy if added to dev deps
    
    # run migrations
    poetry run alembic upgrade head
```

---

## 🔒 CORS & Docs

- CORS origins from `CORS_ORIGINS` (CSV), defaults allow local dev frontends.
- Toggle docs with `DOCS_ENABLED=true|false`.

---

## 📄 Environment Variables (key ones)

| Var | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy URL for Postgres | `postgresql+psycopg2://user:pass@host:5432/db` |
| `SECRET_KEY` | JWT signing secret | `supersecret` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL (minutes) | `30` |
| `ENV` | `dev` enables auto `create_all()` | `dev` / `prod` |
| `API_V1_PREFIX` | API base path | `/api/v1` |
| `CORS_ORIGINS` | CSV of allowed origins | `http://localhost:5173` |
| `ALLOW_HOSTS` | CSV allowed hosts | `localhost,127.0.0.1` |
| `DOCS_ENABLED` | Enable Swagger | `true` |
| `GZIP_ENABLED` | Enable gzip middleware | `true` |

---

## 📝 Notes & Known Issues

- **Dockerfile typo**: the line `COPY pyproject.toml1 poetry.lock* /app/` should be `COPY pyproject.toml poetry.lock* /app/`. Fix it before building.
- **Docker Compose**: not included in repo; a minimal example is provided above.
- **Tests**: placeholder config exists, but no test modules are present yet.
- **Roles**: `UserModel.role` defaults to `"ATTENDEE"`. If you plan Admin/Organizer permissions, add enforcement in routers/services (e.g., decorators or dependency checks).

---

## 🗺️ Roadmap (suggested)

- Add role-based access control (admin/organizer/attendee)
- Add rate limiting & better error mapping
- Seed scripts for demo data
- Test suite: services + routers, and coverage report
- CI workflow (lint, test, build)

---

## 📎 Origin

This backend was implemented to satisfy the **Technical Test: Python Developer** for “Mis Eventos” (Tusdatos.co), covering the required backend features (CRUD, auth, sessions, attendees, search, Docker, docs, migrations).