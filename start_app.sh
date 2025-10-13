#!/bin/bash

echo "🏀 Starting NBA AI Basketball Website..."

# Function to kill background processes on exit
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set up cleanup on script exit
trap cleanup EXIT INT TERM

# Start backend API
echo "Starting backend API server..."
cd Backend
python api.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend development server..."
cd ..
npm run dev &
FRONTEND_PID=$!

echo "✅ Both servers are starting up..."
echo "Backend API: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for both processes
wait
