# Contributing to Nautix

Thanks for your interest in contributing!

## Quick Start
- Backend
  - `cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
  - `uvicorn app.main:app --reload`
- Scanner PWA
  - `cd scanner-pwa && npm install && npm run dev`
- Mobile
  - `cd mobile && npm install && npm run start`

## Branching
- main: protected
- feature branches: `feat/<topic>`
- fixes: `fix/<issue>`

## PRs
- Small, focused PRs
- Link to issue (if any)
- Ensure CI is green

## Coding Standards
- Python: type-friendly, clean functions, early returns
- TS/JS: strict TS, avoid `any`, keep components small

## Environment
- Copy `backend/ENV_SAMPLE.txt` to `backend/.env`
- Generate dev keys (already included in repo setup):
  - `openssl ecparam -genkey -name prime256v1 -noout -out backend/keys/qr_es256_private.pem`
  - `openssl ec -in backend/keys/qr_es256_private.pem -pubout -out backend/keys/qr_es256_public.pem`

## Tests
- Placeholder CI is set; feel free to add pytest and component tests over time.

Happy sailing! 🌊
