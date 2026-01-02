# 🚀 Complete Netlify Deployment Guide (Frontend + Backend)

## 📋 Overview

Your NBA Sports Website has **two parts** that need to be deployed:

1. **Frontend (React)** → Deploy to **Netlify** ✅
2. **Backend (Flask + PyTorch AI)** → Deploy to **Render** ✅ (Netlify can't run Python servers)

**Why separate?** 
- Netlify is for static sites and serverless functions
- PyTorch (AI library) is too large for Netlify Functions
- Render supports Python servers with PyTorch

---

## 🎯 Quick Deployment (5 Steps)

### Step 1: Deploy Backend to Render (Free)

1. **Go to [render.com](https://render.com)** and sign up (free account)

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository**

4. **Configure the service:**
   - **Name**: `nba-api` (or any name you like)
   - **Root Directory**: `Backend` ⚠️ **IMPORTANT!**
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements_production.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free (or paid if you want)

5. **Click "Create Web Service"**

6. **Wait 5-10 minutes** for deployment (PyTorch takes time to install)

7. **Copy your service URL** (looks like `https://nba-api-xxxx.onrender.com`)

8. **Test it**: Open `https://nba-api-xxxx.onrender.com/api/health` in your browser
   - Should show: `{"status": "healthy", "ai_available": true, ...}`

---

### Step 2: Deploy Frontend to Netlify

1. **Go to [netlify.com](https://netlify.com)** and sign up (free account)

2. **Click "Add new site" → "Import an existing project"**

3. **Connect your GitHub repository**

4. **Configure build settings:**
   - **Build command**: `npm run build` (auto-detected)
   - **Publish directory**: `dist` (auto-detected)
   - These should be auto-filled from `netlify.toml`

5. **Add Environment Variable:**
   - Go to **Site settings** → **Environment variables**
   - Click **"Add variable"**
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-render-url.onrender.com/api`
     - ⚠️ Replace with your actual Render URL from Step 1
     - ⚠️ **Must include `/api` at the end!**

6. **Click "Deploy site"**

7. **Wait for build to complete** (2-3 minutes)

8. **Your site is live!** Visit the Netlify URL

---

### Step 3: Test Everything

1. **Test Backend**: 
   - Visit: `https://your-render-url.onrender.com/api/health`
   - Should show: `{"status": "healthy", "ai_available": true}`

2. **Test Frontend**:
   - Visit your Netlify URL
   - Click **"STATS"** → Should load players ✅
   - Click **"AI PREDICTIONS"** → Should show Top Scorers ✅

---

## 🔧 Troubleshooting

### ❌ AI Predictions Not Working

**Problem**: Shows "No predictions available" on Netlify

**Solutions**:

1. **Check Backend Health**:
   - Visit: `https://your-render-url.onrender.com/api/health`
   - Check if `"ai_available": true`
   - If `false`, check Render logs for errors

2. **Check Render Logs**:
   - Go to Render dashboard → Your service → Logs
   - Look for errors like "ModuleNotFoundError: No module named 'torch'"
   - If you see this, make sure you're using `requirements_production.txt`

3. **Verify Requirements File**:
   - In Render dashboard → Settings → Build Command
   - Should be: `pip install -r requirements_production.txt`
   - NOT: `pip install -r requirements.txt`

4. **Check CORS**:
   - Backend should allow requests from your Netlify domain
   - Check `Backend/app.py` has: `CORS(app, resources={r"/api/*": {"origins": "*"}})`

### ❌ Frontend Can't Connect to Backend

**Problem**: "Failed to connect to backend" error

**Solutions**:

1. **Check Environment Variable**:
   - Netlify → Site settings → Environment variables
   - `VITE_API_URL` should be: `https://your-render-url.onrender.com/api`
   - ⚠️ Must include `/api` at the end!

2. **Redeploy After Changing Variables**:
   - After adding/changing `VITE_API_URL`, go to **Deploys** tab
   - Click **"Trigger deploy"** → **"Clear cache and deploy site"**

3. **Test Backend Directly**:
   - Open: `https://your-render-url.onrender.com/api/players` in browser
   - Should return JSON data
   - If 404, check your backend is running

4. **Check Browser Console**:
   - Open browser DevTools (F12) → Console tab
   - Look for CORS errors or 404 errors
   - Check the actual URL being called

### ❌ Backend Won't Start on Render

**Problem**: Render deployment fails

**Solutions**:

1. **Check Build Logs**:
   - Render dashboard → Your service → Logs
   - Look for pip install errors

2. **Verify Root Directory**:
   - Settings → Root Directory should be: `Backend`
   - NOT: `.` or empty

3. **Check Python Version**:
   - Render uses Python 3.12 by default (from `render.yaml`)
   - If issues, try Python 3.11

4. **Memory Issues**:
   - PyTorch installation needs ~2GB RAM
   - Free tier has 512MB - might need to wait longer or upgrade

---

## 📝 Important Notes

### Backend URL Format

✅ **Correct**:
```
VITE_API_URL=https://nba-api-xxxx.onrender.com/api
```

❌ **Wrong**:
```
VITE_API_URL=https://nba-api-xxxx.onrender.com  (missing /api)
VITE_API_URL=https://nba-api-xxxx.onrender.com/  (trailing slash)
```

### Environment Variables

- **Vite requires `VITE_` prefix** for environment variables
- Variables are **only available at build time**, not runtime
- **Must redeploy** after changing environment variables

### Free Tier Limitations

**Render Free Tier**:
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for personal projects)

**Netlify Free Tier**:
- 100GB bandwidth/month
- Unlimited builds
- Perfect for frontend hosting

---

## 🔄 Updating Your Deployment

### After Code Changes

1. **Push to GitHub**
2. **Render**: Auto-deploys (if connected to GitHub)
3. **Netlify**: Auto-builds (if connected to GitHub)
   - Or manually trigger: Deploys → Trigger deploy

### After Environment Variable Changes

1. **Update `VITE_API_URL` in Netlify**
2. **Trigger new deploy**: Deploys → Trigger deploy → Clear cache and deploy site

---

## ✅ Success Checklist

- [ ] Backend deployed to Render
- [ ] Backend health check works: `https://your-url.onrender.com/api/health`
- [ ] Backend shows `"ai_available": true` in health check
- [ ] Frontend deployed to Netlify
- [ ] `VITE_API_URL` set in Netlify environment variables
- [ ] `VITE_API_URL` includes `/api` at the end
- [ ] Stats page loads players
- [ ] AI Predictions page shows Top Scorers
- [ ] No CORS errors in browser console

---

## 🎉 You're Done!

Your NBA Sports Website is now live with:
- ✅ Frontend on Netlify
- ✅ Backend on Render
- ✅ AI Predictions working
- ✅ All features functional

**Your Netlify URL**: `https://your-site-name.netlify.app`
**Your Render URL**: `https://nba-api-xxxx.onrender.com`

---

## 🆘 Still Having Issues?

1. **Check Render logs** for backend errors
2. **Check Netlify build logs** for frontend errors
3. **Check browser console** (F12) for runtime errors
4. **Test backend directly** in browser
5. **Verify environment variables** are set correctly

