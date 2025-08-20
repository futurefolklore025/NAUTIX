# Nautix Starter (Cursor-Ready)

A minimal, working scaffold for **Nautix**:
- **backend/** FastAPI service with search, booking, tickets (QR), and scan API stubs
- **scanner-pwa/** Vite + React + TS app for QR scanning (web camera)
- **mobile/** Expo (React Native) app with basic Search → Results → Ticket flow
- **docker-compose.yml**: Postgres + Backend
- **openapi.yaml** aligned with the MVP endpoints

## Quick Start

### 1) Backend (FastAPI)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Copy env
cp .env.example .env

# Run DB (optional, or use docker-compose at root)
docker compose up -d db

# Create tables
alembic upgrade head

# Start API
uvicorn app.main:app --reload
```

API runs at http://localhost:8000 (see `/docs`).

### 2) Scanner PWA (QR validation)
```bash
cd scanner-pwa
npm install
npm run dev   # Vite dev server
```
Open the URL shown in terminal. Configure `VITE_API_BASE` in `.env` (defaults to http://localhost:8000).

### 3) Mobile App (Expo)
```bash
cd mobile
npm install
npm run start  # then press i / a to run on iOS/Android simulator (or scan QR with Expo Go)
```
Edit `MOBILE_API_BASE` in `app/config.ts` if needed (defaults to http://localhost:8000).

### 4) All-in-one (docker compose for DB+Backend)
```bash
docker compose up -d
```
Then run Scanner PWA and Mobile separately (they are not dockerized in this starter).

---

## Structure
```
backend/           FastAPI + SQLAlchemy + Alembic
scanner-pwa/       Vite React TS with QR scanner
mobile/            Expo React Native app
docker-compose.yml Postgres + Backend
openapi.yaml       Public API contract (MVP excerpt)
```

## Notes
- This is a lean scaffold to iterate quickly in **Cursor**. Endpoints are stubbed and documented; fill service logic as you go.
- Uses **JWT-like signed QR token** (ES256) for tickets; in dev, a static keypair is provided.
- Minimal error handling & auth intentionally — extend per your needs.


---

## New Additions

### Payments (Stripe test)
- Set `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` in `backend/.env`.
- `/bookings` now returns a `client_secret` for a PaymentIntent.
- Add a Stripe test card in your mobile/portal client and confirm the PI; webhook `/payments/stripe/webhook` flips booking to confirmed and issues tickets.

### CSV Schedule Import
- Endpoint: `POST /operator/import-schedules` (multipart file)
- Template: see `data/sample_schedules.csv`

### Operator Portal
```bash
cd operator-portal
npm install
npm run dev
```
- CSV uploader + basic manifest view; configure `VITE_API_BASE` if needed.

### Seed Data
```bash
# After migrations
python backend/scripts/seed.py
```
Seeds ports, an operator, routes, and a couple of schedules. 