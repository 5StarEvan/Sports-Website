# 🚀 Netlify Deployment Guide

This guide will help you deploy your NBA Sports Website to Netlify with a separate backend API server.

## 📋 Overview

Your application has two parts:
1. **Frontend** (React/Vite) - Deploys to Netlify
2. **Backend** (Flask API) - Needs to be deployed separately (Render, Railway, or Fly.io)

---

## 🔧 Step 1: Deploy Backend API

You need to deploy your Flask backend to a cloud service. Here are the easiest options:

### Option A: Render (Recommended - Free Tier Available)

1. **Sign up** at [render.com](https://render.com)
2. **Create a New Web Service**:
   - Connect your GitHub repository
   - Root Directory: `Backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
3. **Set Environment Variables** (in Render dashboard):
   - `FLASK_ENV=production`
   - `PORT=5000` (Render sets this automatically, but good to have)
4. **Deploy** and copy your service URL (e.g., `https://nba-api-xxxx.onrender.com`)

### Option B: Railway (Free Trial Available)

1. **Sign up** at [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub**
3. **Select Repository** → Choose `Backend` folder
4. **Configure**:
   - Add `requirements.txt` detection
   - Start command: `python app.py`
5. **Deploy** and copy your service URL

### Option C: Fly.io (Free Tier Available)

1. **Install Fly CLI**: `curl -L https://fly.io/install.sh | sh`
2. **In Backend folder**, create `fly.toml`:
   ```toml
   app = "your-app-name"
   primary_region = "iad"

   [build]

   [http_service]
     internal_port = 5000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0
     processes = ["app"]

     [[http_service.checks]]
       interval = "15s"
       timeout = "2s"
       grace_period = "5s"
       method = "GET"
       path = "/api/health"
   ```
3. **Deploy**: `fly deploy`

---

## 🌐 Step 2: Configure Netlify

### 2.1. Build Settings

In your Netlify dashboard:

1. **Build command**: `npm run build`
2. **Publish directory**: `dist`
3. **Node version**: Set to `18.x` or `20.x` in Netlify settings

### 2.2. Environment Variables

Go to **Site settings** → **Environment variables** and add:

```
VITE_API_URL=https://your-backend-url.onrender.com/api
```

**Important**: 
- Replace `https://your-backend-url.onrender.com/api` with your actual backend URL
- Make sure to include `/api` at the end if your backend serves APIs under `/api`
- If your backend is at the root (e.g., `https://api.example.com/api/players`), use `https://api.example.com/api`

### 2.3. Deploy

1. **Push your code** to GitHub (if using Git-based deployment)
2. **Or drag and drop** your `dist` folder after building locally:
   ```bash
   npm run build
   # Then drag the dist folder to Netlify
   ```

---

## ✅ Step 3: Verify Deployment

1. **Check Backend**: Visit `https://your-backend-url.onrender.com/api/health`
   - Should return: `{"status": "healthy", "message": "NBA API server is running"}`

2. **Check Frontend**: Visit your Netlify URL
   - Click "STATS" - should load player data
   - Click "AI PREDICTIONS" - should load predictions (if backend has AI enabled)

---

## 🔍 Troubleshooting

### Backend Issues

**Problem**: Backend doesn't start
- **Solution**: Check logs in Render/Railway dashboard
- Make sure `requirements.txt` includes all dependencies
- Verify `app.py` exists in the Backend folder

**Problem**: CORS errors in browser console
- **Solution**: Backend needs CORS enabled. Check `Backend/app.py` has:
  ```python
  from flask_cors import CORS
  CORS(app)
  ```

**Problem**: Backend URL returns 404
- **Solution**: Make sure your backend URL in Netlify includes `/api` if needed
- Test the backend directly: `https://your-backend-url.onrender.com/api/health`

### Frontend Issues

**Problem**: Frontend shows "Failed to connect to backend"
- **Solution**: 
  1. Check `VITE_API_URL` is set correctly in Netlify environment variables
  2. Rebuild and redeploy after setting the variable
  3. Check browser console for exact error

**Problem**: Environment variable not working
- **Solution**: 
  - Environment variables must start with `VITE_` in Vite
  - Redeploy after adding/changing environment variables
  - Variables are only available at build time, not runtime

**Problem**: Works locally but not on Netlify
- **Solution**: 
  - Local uses Vite proxy (`vite.config.js`)
  - Production needs `VITE_API_URL` set
  - Make sure backend allows requests from your Netlify domain

---

## 🔄 Updating Your Deployment

### After Code Changes

1. **Backend**: Push to GitHub → Auto-deploys (if connected)
2. **Frontend**: Push to GitHub → Netlify auto-builds
   - **Or**: Manual deploy via Netlify dashboard

### After Environment Variable Changes

1. Update `VITE_API_URL` in Netlify
2. **Trigger a new deploy** (Netlify → Deploys → Trigger deploy)

---

## 📝 Quick Reference

### Backend URLs Format

```
Render:     https://app-name-xxxx.onrender.com
Railway:    https://app-name.up.railway.app
Fly.io:     https://app-name.fly.dev
```

### Environment Variable Examples

```bash
# For Render backend serving at root
VITE_API_URL=https://nba-api-xxxx.onrender.com/api

# For Railway backend
VITE_API_URL=https://nba-api-production.up.railway.app/api

# For Fly.io backend
VITE_API_URL=https://nba-api.fly.dev/api
```

### Testing Your Setup

```bash
# Test backend
curl https://your-backend-url.onrender.com/api/health

# Test frontend locally with production backend
VITE_API_URL=https://your-backend-url.onrender.com/api npm run build
npm run preview
```

---

## 🎉 Success Checklist

- [ ] Backend deployed and accessible at `https://your-backend-url.com/api/health`
- [ ] `VITE_API_URL` set in Netlify environment variables
- [ ] Frontend deployed to Netlify
- [ ] Stats page loads player data
- [ ] AI Predictions page works (if enabled)
- [ ] No CORS errors in browser console

---

## 🆘 Need Help?

1. Check backend logs in Render/Railway dashboard
2. Check Netlify build logs
3. Check browser console for errors
4. Verify environment variables are set correctly
5. Test backend URL directly in browser

---

**🎯 You're all set! Your site should now work on Netlify without needing localhost!**





