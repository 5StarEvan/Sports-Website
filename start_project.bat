@echo off
echo ========================================
echo Starting NBA Sports Website
echo ========================================
echo.

REM Start Backend Server
echo [1/2] Starting Backend Server...
start "NBA Backend" cmd /k "cd Backend && call cleanenv\Scripts\activate.bat && python app.py"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

REM Start Frontend
echo [2/2] Starting Frontend...
start "NBA Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Two windows will open - one for backend, one for frontend
echo Close them to stop the servers
echo.
pause

