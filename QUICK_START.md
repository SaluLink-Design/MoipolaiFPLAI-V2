# Quick Deploy to Railway - 3 Steps

## ⚡ TL;DR

```bash
# 1. Commit and push
git add .
git commit -m "Fix Railway deployment"
git push

# 2. Deploy on Railway
# - Go to railway.app
# - Create new project from your repo
# - Root Directory: leave blank

# 3. Test
curl https://your-app.railway.app/health
```

## ✅ What's Fixed

- ✅ Missing `views.py` file
- ✅ Added logging everywhere
- ✅ Added CORS for frontend
- ✅ Optimized gunicorn (2 workers, 120s timeout)
- ✅ Health check timeout increased to 300s
- ✅ Better error handling with JSON responses
- ✅ All endpoints return proper status codes

## 🔧 Files Changed

| File | Change |
|------|--------|
| `app/__init__.py` | Added logging + CORS |
| `app/routes/views.py` | **NEW** - was missing |
| `app/routes/api.py` | Added error handling + logging |
| `app.py` | Added PORT env var + logging |
| `requirements.txt` | Added gunicorn |
| `Procfile` | **NEW** - optimized settings |
| `runtime.txt` | **NEW** - Python 3.11 |
| `railway.toml` | **NEW** - Railway config |
| `.gitignore` | **NEW** |

## 📡 Your API Endpoints

After deployment, you'll have:

```
GET /health              → {"status": "ok"}
GET /api/health          → {"status": "ok"}
GET /api/generate        → Full squad JSON
GET /api/reshuffle       → Alternative squad JSON
```

## 🎯 Use in React Frontend

```javascript
const API_URL = 'https://your-app.railway.app';

// Generate squad
const response = await fetch(`${API_URL}/api/generate`);
const squad = await response.json();
console.log(squad);
```

## 🐛 If Still Failing

1. Check Railway logs for specific error
2. Look for "ERROR" or "CRITICAL" lines
3. Share the error message

Common issues:
- **Import error** → Missing package in requirements.txt
- **Connection timeout** → FPL API down/blocked
- **Worker timeout** → Already fixed (120s timeout)

