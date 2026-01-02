# How to Run the NBA Sports Website

## Quick Start (Easiest Method)

**Just double-click `start_project.bat`** in the project root folder!

This will automatically:
- Start the backend server with AI predictions
- Start the frontend React app
- Open both in separate windows

---

## Manual Method (Step by Step)

### Step 1: Start the Backend Server

1. Open a terminal/PowerShell in the **Backend** folder
2. Activate the virtual environment:
   ```powershell
   .\cleanenv\Scripts\Activate.ps1
   ```
   Or use the batch file:
   ```cmd
   cleanenv\Scripts\activate.bat
   ```

3. Start the server:
   ```powershell
   python app.py
   ```

You should see:
```
✅ NBA data loaded successfully - 570 players available
🚀 Starting NBA API server...
🌐 Server URL: http://localhost:5000
```

**Keep this window open!**

### Step 2: Start the Frontend

1. Open a **NEW** terminal/PowerShell in the **project root** folder
2. Start the frontend:
   ```powershell
   npm run dev
   ```

You should see:
```
  VITE v7.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

### Step 3: Open Your Browser

Go to: **http://localhost:5173**

---

## Troubleshooting

### Error: "No module named 'bs4'"
**Solution:** Make sure you activated the virtual environment:
```powershell
cd Backend
.\cleanenv\Scripts\Activate.ps1
```

### Error: "AI predictions not available"
**Solution:** The virtual environment has PyTorch installed. Make sure you're using:
```powershell
.\cleanenv\Scripts\python.exe app.py
```

### Port 5000 or 5173 already in use
**Solution:** Stop any existing servers:
```powershell
# Find and stop Python processes
Get-Process python | Stop-Process -Force
```

---

## What Each Server Does

- **Backend (Port 5000)**: Flask API server with AI predictions
- **Frontend (Port 5173)**: React web application

Both must be running for the website to work!

