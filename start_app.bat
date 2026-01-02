@echo off
echo 🏀 Starting NBA Sports Website...
echo.

echo 📦 Installing backend dependencies...
cd Backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Flask API server...
start "NBA API Server" cmd /k "python app.py"

echo.
echo ⏳ Waiting for API server to start...
timeout /t 3 /nobreak > nul

echo.
echo 📦 Installing frontend dependencies...
cd ..
npm install
if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo 🌐 Starting React frontend...
start "NBA Frontend" cmd /k "npm run dev"

echo.
echo ✅ NBA Sports Website started successfully!
echo.
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend API: http://localhost:5000
echo.
echo Click STATS in the navigation to view NBA players!
echo.
pause
