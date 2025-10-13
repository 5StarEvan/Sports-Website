# 🏀 NBA Sports Website - Setup Instructions

## ✅ **What's Been Connected:**

1. **✅ ML & Database**: NBA player data from `nba_2024_25_data.pkl` (150 players)
2. **✅ Flask API Server**: REST endpoints for player data
3. **✅ React Frontend**: Stats page with player display
4. **✅ Navigation**: Click "STATS" to view NBA players

## 🚀 **How to Run the Application:**

### **Option 1: Easy Start (Windows)**
```bash
# Double-click the start_app.bat file
# OR run in terminal:
start_app.bat
```

### **Option 2: Manual Start**

#### **1. Start Backend API Server:**
```bash
cd Backend
pip install -r requirements.txt
python app.py
```
- Backend runs on: `http://localhost:5000`

#### **2. Start Frontend (New Terminal):**
```bash
npm install
npm run dev
```
- Frontend runs on: `http://localhost:5173`

## 🎯 **How to Use:**

1. **Open**: Go to `http://localhost:5173`
2. **Click**: "STATS" in the navigation bar
3. **Browse**: NBA players with their statistics
4. **Filter**: Search by name, team, or position
5. **Sort**: Click column headers to sort players

## 📊 **Features Available:**

### **Player Stats Display:**
- ✅ Player name, team, position
- ✅ Age, height, weight
- ✅ Current season stats (PPG, APG, RPG, SPG, BPG)
- ✅ Shooting percentages (FG%, 3P%, FT%)
- ✅ Performance trends and consistency scores
- ✅ Games played

### **Interactive Features:**
- ✅ Search players by name
- ✅ Filter by team or position
- ✅ Sort by any stat column
- ✅ Pagination for large datasets
- ✅ Responsive design for mobile

### **API Endpoints:**
- `GET /api/players` - Get all players with pagination
- `GET /api/players/{id}` - Get specific player
- `GET /api/teams` - Get all teams
- `GET /api/positions` - Get all positions
- `GET /api/stats/leaders` - Get stat leaders
- `GET /api/ai-predictions` - Get AI predictions (if PyTorch installed)

## 🗃️ **Data Source:**

- **150 NBA Players** from 2024-25 season
- **Real player names** including LeBron James, Stephen Curry, etc.
- **Comprehensive stats** including trends and consistency metrics
- **AI-ready data** for predictions (optional PyTorch features)

## 🔧 **Technical Stack:**

- **Frontend**: React + Vite + React Router
- **Backend**: Flask + CORS
- **Data**: Pickle files with pandas DataFrames
- **ML**: PyTorch (optional for AI predictions)

## 🎨 **UI Features:**

- **Modern Design**: Glass-morphism cards with gradients
- **Responsive**: Works on desktop, tablet, and mobile
- **Interactive**: Hover effects and smooth transitions
- **Professional**: Clean, sports-themed interface

## 🚨 **Troubleshooting:**

### **Backend Issues:**
```bash
# If Flask server fails to start:
cd Backend
pip install flask flask-cors pandas numpy nba-api requests

# If NBA data not found:
# The system will show an error message
```

### **Frontend Issues:**
```bash
# If React fails to start:
npm install
npm run dev

# If API connection fails:
# Make sure Flask server is running on port 5000
```

### **Data Issues:**
- NBA data is stored in `Backend/nba_2024_25_data.pkl`
- Contains 150 players with comprehensive statistics
- Data loads automatically when Flask server starts

## 🎉 **Success Indicators:**

✅ **Backend Running**: See "NBA API server is running" in terminal  
✅ **Frontend Running**: See "Local: http://localhost:5173" in terminal  
✅ **Data Loaded**: See "Loaded 150 NBA players" in backend terminal  
✅ **Stats Page**: Click STATS → See player cards with statistics  

## 📱 **Mobile Support:**

The stats page is fully responsive and works great on:
- 📱 Mobile phones
- 📱 Tablets  
- 💻 Desktop computers

---

**🎯 Ready to go! Click "STATS" to browse NBA players!**
