#!/bin/bash

echo "🌊 Setting up Nautix production environment..."

# Generate JWT keys
echo "🔑 Generating JWT keys..."
mkdir -p backend/keys
if [ ! -f "backend/keys/qr_es256_private.pem" ]; then
    openssl ecparam -genkey -name prime256v1 -noout -out backend/keys/qr_es256_private.pem
    openssl ec -in backend/keys/qr_es256_private.pem -pubout -out backend/keys/qr_es256_public.pem
    echo "✅ JWT keys generated"
else
    echo "⚠️  JWT keys already exist"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copy .env.template to .env and configure your values."
    exit 1
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

# Seed data (optional)
read -p "Do you want to seed sample data? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python scripts/seed.py
    echo "✅ Sample data seeded"
fi

echo "🎉 Production setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the application: uvicorn app.main:app --reload"
echo "2. Visit http://localhost:8000/docs for API documentation"
echo "3. Run tests: pytest tests/ -v"
