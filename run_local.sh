#!/bin/bash

# Kill background processes on exit
trap "kill 0" EXIT

echo "Starting Backend (FastAPI)..."
cd backend
export OCR_TYPE=easyocr
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Frontend (SimpleHTTPServer)..."
cd ../frontend
python3 -m http.server 3000 &

echo "Application started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"

# Wait for background processes
wait
