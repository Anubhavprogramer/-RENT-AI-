#!/bin/bash

# RentWise Development Setup Script

echo "🏠 Setting up RentWise Development Environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt
cd ..

echo "🤖 Training ML model..."
cd backend
python3 -c "from app import load_and_train_model; load_and_train_model()"
cd ..

echo "🚀 Starting development servers..."

# Start backend in background
echo "🔧 Starting Flask backend on port 5000..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "⚡ Starting React frontend on port 5173..."
npm run dev &
FRONTEND_PID=$!

echo "✅ RentWise is running!"
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user to stop
wait $FRONTEND_PID
kill $BACKEND_PID 2>/dev/null
