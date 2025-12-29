# Railway Health Check Fix

## What Was Wrong

The health check was failing because:

1. **Missing/incomplete error handling** - The app might crash during startup and Railway couldn't reach `/health`
2. **No CORS headers** - Frontend requests would be blocked
3. **Insufficient timeout** - Health check timeout was too short (100s → 300s)
4. **No logging** - Couldn't see what was failing
5. **Gunicorn not optimized** - Default settings weren't suitable for Railway

## What Was Fixed

### 1. ✅ Added Comprehensive Logging

**File: `app/__init__.py`**
- Added logging configuration
- Logs when blueprints are registered
- Shows any errors during app creation

**File: `app.py`**
- Added startup logging
- Shows when app is created successfully
- Catches and logs any startup errors

**File: `app/routes/api.py`**
- Added request logging for all endpoints
- Error responses now include details
- Health check explicitly returns 200 status code

### 2. ✅ Added CORS Support

**File: `app/__init__.py`**
- Added `Access-Control-Allow-Origin: *` headers
- Allows your React frontend to call the API
- Supports all HTTP methods (GET, POST, etc.)

### 3. ✅ Optimized Gunicorn Configuration

**Files: `Procfile` and `railway.toml`**
```bash
gunicorn app:app \
  --bind 0.0.0.0:$PORT \
  --workers 2 \
  --threads 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

- **2 workers** - Better concurrency
- **2 threads per worker** - Handle multiple requests
- **120s timeout** - Enough time for FPL API calls
- **Logging to stdout** - See logs in Railway dashboard

### 4. ✅ Increased Health Check Timeout

**File: `railway.toml`**
- Changed from 100s to 300s
- Gives the app more time to start and respond

### 5. ✅ Better Error Handling

**File: `app/routes/api.py`**
- All endpoints now have try-catch blocks
- Return proper JSON error responses
- Include error messages for debugging

## How to Deploy the Fix

### Step 1: Push Changes to Git

```bash
cd "/Users/tjmoipolai/Documents/Thula's Lab/moipolaifplv2/MoipolaiFPLAI-V2"

git add .
git commit -m "Fix Railway health check issues - add logging, CORS, error handling"
git push
```

### Step 2: Railway Will Auto-Deploy

- Railway will detect the push and redeploy
- Watch the logs in Railway dashboard

### Step 3: Check the Logs

In Railway dashboard, look for these log messages:

✅ **Success indicators:**
```
Starting FPL AI Backend...
Flask app created successfully
Blueprints registered successfully
[INFO] Booting worker with pid: ...
[INFO] Listening at: http://0.0.0.0:PORT
```

❌ **If you see errors, common issues:**

1. **Import Error** - Missing dependency in `requirements.txt`
2. **Connection Error** - Can't reach FPL API (network issue)
3. **Port already in use** - Railway will handle this automatically
4. **Timeout** - App takes too long to start (should be fixed now)

## Testing Locally (Optional)

If you want to test before deploying:

```bash
# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run test script
python test_app.py

# Or start the server
python app.py
```

Then visit `http://localhost:5000/health`

## Verifying Deployment

Once deployed, test these endpoints:

### 1. Health Check
```bash
curl https://your-app.railway.app/health
# Should return: {"message":"FPL AI Backend is running","status":"ok"}
```

### 2. API Health Check
```bash
curl https://your-app.railway.app/api/health
# Should return: {"message":"FPL AI API is running","status":"ok"}
```

### 3. Generate Squad (this will be slower)
```bash
curl https://your-app.railway.app/api/generate
# Should return full squad JSON
```

## If Health Check Still Fails

### Check Railway Logs

Look for the specific error message. Common patterns:

**"ModuleNotFoundError"**
- Missing package in `requirements.txt`
- Check the logs for which module is missing
- Add it to `requirements.txt` and redeploy

**"Connection timeout" or "Connection refused"**
- FPL API might be down or blocking Railway IPs
- Try accessing https://fantasy.premierleague.com/api/bootstrap-static/ manually
- May need to add retry logic or caching

**"Address already in use"**
- Shouldn't happen - Railway manages ports
- If it does, check that `$PORT` variable is being used

**"Worker timeout"**
- App is starting but taking too long to respond
- Already increased to 120s in this fix
- If still happens, increase `--timeout` in Procfile

### Force Fresh Deploy

Sometimes Railway cache causes issues:

1. Go to Railway project settings
2. Click "Redeploy"
3. Or add a dummy environment variable to trigger rebuild

### Check Railway Environment

Make sure Railway set these automatically:
- `PORT` - Should be set by Railway
- `PYTHONUNBUFFERED` - Set to `1` (for logging)

## Updated Project Structure

```
MoipolaiFPLAI-V2/
├── app/
│   ├── __init__.py          ← Added logging & CORS
│   ├── routes/
│   │   ├── api.py           ← Added error handling
│   │   └── views.py         ← Created (was missing!)
│   ├── services/
│   └── models/
├── app.py                   ← Added logging
├── requirements.txt         ← Added gunicorn
├── Procfile                 ← Optimized gunicorn settings
├── runtime.txt              ← Python 3.11
├── railway.toml             ← Increased timeout to 300s
├── test_app.py              ← New test script
└── templates/
    └── index.html
```

## Next Steps After Successful Deploy

1. **Add environment variables** for any API keys
2. **Set up custom domain** in Railway (optional)
3. **Add caching** for FPL API responses to reduce load
4. **Monitor logs** for errors or performance issues
5. **Update your React frontend** to use the Railway URL:

```javascript
// In your React app
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-app.railway.app';

fetch(`${API_BASE_URL}/api/generate`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## Questions?

If you're still having issues:
1. Share the Railway deployment logs (look for ERROR or CRITICAL lines)
2. Try the `/health` endpoint manually
3. Check if the FPL API is accessible: https://fantasy.premierleague.com/api/bootstrap-static/

