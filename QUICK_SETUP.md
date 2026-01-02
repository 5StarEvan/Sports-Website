# 🚀 Quick Setup for Netlify Deployment

## The Problem
Your site works locally because the backend runs on `localhost:5000`, but on Netlify there's no backend server, so API calls fail.

## The Solution
1. Deploy your backend separately (to Render/Railway/Fly.io)
2. Tell your frontend where the backend is using an environment variable

---

## ⚡ Quick Steps

### 1. Deploy Backend to Render (Free)

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:
   - **Name**: `nba-api` (or any name)
   - **Root Directory**: `Backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Click **"Create Web Service"**
6. Wait for deployment (takes 2-3 minutes)
7. **Copy your service URL** (looks like `https://nba-api-xxxx.onrender.com`)

### 2. Update Netlify

1. Go to your Netlify site dashboard
2. Click **Site settings** → **Environment variables**
3. Click **"Add variable"**
4. Add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-render-url.onrender.com/api` (replace with your actual URL)
5. Click **"Save"**
6. Go to **Deploys** tab → Click **"Trigger deploy"** → **"Clear cache and deploy site"**

### 3. Test

Visit your Netlify site and click **"STATS"** - it should load players!

---

## 📝 Important Notes

- **Backend URL must include `/api`** at the end
  - ✅ Correct: `https://nba-api-xxxx.onrender.com/api`
  - ❌ Wrong: `https://nba-api-xxxx.onrender.com`

- **After changing environment variables**, you must redeploy in Netlify

- **The backend must have CORS enabled** (already done in `app.py`)

---

## 🔍 Troubleshooting

**Not working?**
1. Test backend: Open `https://your-backend-url.onrender.com/api/health` in browser
   - Should show: `{"status": "healthy", ...}`
2. Check Netlify environment variable is set correctly
3. Redeploy after setting the variable
4. Check browser console for errors

**Need help?** See `NETLIFY_DEPLOYMENT.md` for detailed instructions.





