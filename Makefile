# Nautix Makefile

.PHONY: help backend dev db-up pwa mobile seed

help:
	@echo "Targets:"
	@echo "  backend    - run FastAPI backend (uvicorn)"
	@echo "  db-up      - start Postgres via docker compose"
	@echo "  seed       - seed sample data"
	@echo "  pwa        - run scanner PWA"
	@echo "  mobile     - run mobile app"

backend:
	cd backend && . .venv/bin/activate || python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt; \
	uvicorn app.main:app --reload

db-up:
	docker compose up -d db

seed:
	cd backend && . .venv/bin/activate && python scripts/seed.py

pwa:
	cd scanner-pwa && npm install && npm run dev

mobile:
	cd mobile && npm install && npm run start
