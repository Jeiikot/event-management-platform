# My Events — Monorepo

Full‑stack event management platform (create events, sessions, speakers, attendee registrations, and authentication).
This repo contains **backend (FastAPI + PostgreSQL)** and **frontend (Vite + React)** and can be run end‑to‑end with **Docker Compose**.

> Aligned with the technical test: backend + frontend, auth, search/pagination, and Docker setup.


## 🗂 Repository structure

```
.
├── backend/        # FastAPI app (Poetry, Alembic, SQLAlchemy)
├── frontend/       # Vite + React
├── docker-compose.yml
└── README.md
```

## 🚀 Quick start (Docker)

**Requirements:** Docker 24+ and Docker Compose plugin.

1) **Environment files** (optional; compose already provides safe defaults)

- `backend/.env` (you can copy from `.env.example`):
```env
DATABASE_URL=postgresql+psycopg2://miseventos:miseventos@db:5432/miseventos
SECRET_KEY=change-me
ENV=dev
DOCS_ENABLED=true
CORS_ORIGINS=["http://localhost:5173"]
API_V1_PREFIX=/api/v1
```

- `frontend/.env` (you can copy from `.env.example`):
```env
VITE_API_BASE=http://localhost:8000
```

2) **Bring everything up**

```bash
docker compose up --build
```

Services:
- **API** → http://localhost:8000  (Docs: http://localhost:8000/docs)
- **Web** → http://localhost:5173
- **Postgres** → localhost:5432  (db: `miseventos` / user: `miseventos` / pass: `miseventos`)

> On startup the API runs DB migrations (`alembic upgrade head`).
> The frontend runs Vite dev server with HMR.


## 🔌 API overview (main endpoints)

Default prefix: `/api/v1`

- **Auth**
  - `POST /auth/register`
  - `POST /auth/login` → `{ "access_token": "..." }`

- **Users**
  - `GET /users/me` (requires auth)

- **Events**
  - `GET /events?search=&page=&size=`
  - `POST /events` (requires auth)
  - `GET /events/{id}`
  - `PUT /events/{id}` (requires auth)

- **Registrations**
  - `POST /registrations/events/{eventId}` (requires auth)
  - `GET /registrations/events` (requires auth)

- **Sessions**
  - `GET /sessions/events/{eventId}`
  - `POST /sessions/events/{eventId}` (requires auth)


## 🧪 Quick sanity check

Once the stack is up, try:

```bash
# 1) Register
curl -X POST http://localhost:8000/api/v1/auth/register   -H "Content-Type: application/json"   -d '{"email":"demo@demo.com","password":"Demo1234"}'

# 2) Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login   -H "Content-Type: application/json"   -d '{"email":"demo@demo.com","password":"Demo1234"}' | jq -r .access_token)

# 3) Create an event
curl -X POST http://localhost:8000/api/v1/events   -H "Authorization: Bearer $TOKEN"   -H "Content-Type: application/json"   -d '{"name":"TechConf","description":"Demo","date":"2025-12-01T09:00:00","capacity":200}'
```

> If you don't have `jq`, inspect the login response and copy the token manually.


## 🧰 Local development (without Docker, optional)

### Backend
```bash
cd backend
poetry install
cp .env.example .env   # adjust DATABASE_URL to your local Postgres
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm ci
cp .env.example .env   # VITE_API_BASE=http://localhost:8000
npm run dev -- --host
```


## ⚙️ Backend environment variables

- `DATABASE_URL` — e.g. `postgresql+psycopg2://user:pass@host:5432/db`
- `SECRET_KEY` — JWT signing key
- `API_V1_PREFIX` — API prefix (default `/api/v1`)
- `CORS_ORIGINS` — JSON list of allowed origins
- `DOCS_ENABLED` — enable `/docs` and `/redoc` (`true/false`)
- `ENV` — `dev` | `prod`


## 🧹 Useful backend commands

```bash
# create new migrations (after model changes)
poetry run alembic revision --autogenerate -m "feat: ..."
poetry run alembic upgrade head

# run tests (if present)
poetry run pytest -q
```


## 🛣 Frontend routes

- `/` — Events list (with pagination + search)
- `/events/:id` — Event detail (with sessions)
- `/events/new` and `/events/:id/edit` — CRUD (requires auth)
- `/login` and `/register`
- `/profile` — My registrations

The frontend reads `VITE_API_BASE` and uses the fixed prefix `/api/v1`.


## 📝 Notes

- Postgres credentials are **development only**.
- Change `SECRET_KEY` before any deployment.
- CORS allows `http://localhost:5173` by default; adjust for your domain.
- Compose creates a named volume `dbdata` for persistence.