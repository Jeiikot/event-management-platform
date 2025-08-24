# Mis Eventos — Frontend (Vite + React + Tailwind)

Proyecto base para conectarse a un backend (FastAPI). Incluye:
- React Router, manejo simple de auth con token (localStorage)
- Listado, detalle, creación/edición de eventos
- Registro a eventos
- **Módulo de sesiones** por evento (listar y crear)
- Config de endpoints por `.env` o desde la UI

## Requisitos
- Node 18+

## Configuración
Copia `.env.example` a `.env` y ajusta:
```env
VITE_API_BASE=http://localhost:8000
```

## Scripts
```bash
npm install
npm run dev     # http://localhost:5173
npm run build
npm run preview
```

## Endpoints esperados (puedes cambiarlos en la app → Configuración)
- POST /auth/register
- POST /auth/login  → { "access_token": "..." }
- GET  /auth/me     → (opcional)
- GET  /events?search=&page=&page_size=
- POST /events      (auth)
- GET  /events/:id
- PUT  /events/:id  (auth)
- POST /events/:id/register   (auth)
- GET  /me/registrations      (auth)
- GET  /events/:id/sessions
- POST /events/:id/sessions   (auth)

## Notas
- El listado acepta respuesta `{"items":[],"total":n}` o array simple.
- Fechas en ISO 8601 (`datetime-local` en formularios).
