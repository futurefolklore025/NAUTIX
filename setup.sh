#!/bin/bash

echo "🌊 Setting up Nautix Project..."
echo "================================"

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
else
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if Node.js is available
if command -v node &> /dev/null; then
    echo "✅ Node.js found"
else
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker found"
else
    echo "⚠️  Docker not found. You can still run the backend locally"
fi

echo ""
echo "🚀 Quick Start Options:"
echo "========================"
echo ""
echo "1. Backend (FastAPI):"
echo "   cd backend"
echo "   python3 -m venv .venv"
echo "   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate"
echo "   pip install -r requirements.txt"
echo "   python3 scripts/seed.py  # Seed sample data"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Scanner PWA:"
echo "   cd scanner-pwa"
echo "   npm install"
echo "   npm run dev"
echo ""
echo "3. Mobile App:"
echo "   cd mobile"
echo "   npm install"
echo "   npm run start"
echo ""
echo "4. All-in-one (Docker):"
echo "   docker compose up -d"
echo ""
echo "📱 The backend will be available at: http://localhost:8000"
echo "🔍 API docs will be at: http://localhost:8000/docs"
echo "📱 Scanner PWA will be at: http://localhost:3001"
echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Start with the backend to test the API"
echo "2. Use the scanner PWA to test QR code scanning"
echo "3. Run the mobile app to test the booking flow"
echo "4. Check the README.md for detailed instructions"
echo ""
echo "🌊 Happy sailing with Nautix!" 