# ⚡ Quick Deploy Guide

## Why AI Predictions Don't Work on Netlify

**The Problem**: 
- Netlify can't run Python/Flask servers (only static sites)
- PyTorch (AI library) is too large for Netlify Functions
- Your backend needs to run continuously for AI predictions

**The Solution**:
- Deploy **Backend** to **Render** (supports Python + PyTorch)
- Deploy **Frontend** to **Netlify** (perfect for React)
- Connect them with an environment variable

---

## 🚀 2-Step Deployment

### 1️⃣ Backend → Render (5 minutes)

1. Go to [render.com](https://render.com) → Sign up
2. **New +** → **Web Service**
3. Connect GitHub repo
4. Settings:
   - **Root Directory**: `Backend`
   - **Build Command**: `pip install -r requirements_production.txt`
   - **Start Command**: `python app.py`
5. **Create** → Wait 5-10 min → Copy URL

**Test**: `https://your-url.onrender.com/api/health` should show `"ai_available": true`

### 2️⃣ Frontend → Netlify (3 minutes)

1. Go to [netlify.com](https://netlify.com) → Sign up
2. **Add new site** → **Import from Git**
3. Connect GitHub repo
4. **Environment Variables** → Add:
   - Key: `VITE_API_URL`
   - Value: `https://your-render-url.onrender.com/api` ⚠️ Include `/api`!
5. **Deploy site**

**Done!** Your site is live with AI predictions working! 🎉

---

## 📋 Files Created

✅ `netlify.toml` - Netlify configuration
✅ `Backend/requirements_production.txt` - Includes PyTorch
✅ `Backend/render.yaml` - Render configuration
✅ `DEPLOY_TO_NETLIFY.md` - Complete guide

---

## 🔍 Quick Troubleshooting

**AI not working?**
- Check Render logs for errors
- Verify `requirements_production.txt` is used (not `requirements.txt`)
- Test: `https://your-url.onrender.com/api/health` → Should show `"ai_available": true`

**Frontend can't connect?**
- Check `VITE_API_URL` includes `/api` at the end
- Redeploy Netlify after changing environment variables
- Test backend directly in browser

---

**See `DEPLOY_TO_NETLIFY.md` for detailed instructions!**

