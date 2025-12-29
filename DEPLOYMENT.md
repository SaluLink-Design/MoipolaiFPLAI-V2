# Railway Deployment Guide

## What Was Fixed

Your backend had the following issues that prevented Railway deployment:

1. ✅ **Missing `views.py`** - Created the views blueprint for serving the frontend HTML
2. ✅ **Hardcoded port** - Updated `app.py` to use Railway's `PORT` environment variable
3. ✅ **Missing gunicorn** - Added gunicorn to `requirements.txt` for production WSGI server
4. ✅ **No Procfile** - Created Procfile to tell Railway how to start the app
5. ✅ **No Python version** - Added `runtime.txt` to specify Python 3.11
6. ✅ **Health check endpoint** - Added `/health` and `/api/health` endpoints for Railway monitoring
7. ✅ **Railway config** - Created `railway.toml` for optimal deployment settings

## Deployment Steps

### 1. Push to Git Repository

```bash
git add .
git commit -m "Configure for Railway deployment"
git push
```

### 2. Deploy to Railway

1. Go to [railway.app](https://railway.app) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway will automatically detect your Python app and deploy it

### 3. Monitor Deployment

- Railway will run `pip install -r requirements.txt`
- Then start the app with the Procfile command
- Check the deployment logs for any errors
- Once deployed, you'll get a public URL like `https://your-app.railway.app`

## API Endpoints

Your backend provides these endpoints:

### Frontend
- `GET /` - Serves the web interface
- `GET /health` - Health check for the web service

### API
- `GET /api/health` - API health check
- `GET /api/generate` - Generate optimal FPL squad for current gameweek
- `GET /api/reshuffle` - Generate alternative squad with differential bias

## Environment Variables

No environment variables are currently required, but you can add them in Railway's dashboard if needed:

- `FLASK_ENV` - Set to `production` (optional, default)
- Any API keys for third-party services (if you add them later)

## Testing Locally

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn (production mode)
gunicorn app:app --bind 0.0.0.0:5000

# Or run in development mode
python app.py
```

Visit `http://localhost:5000` to test the app.

## Connecting to Frontend

Once deployed, use your Railway URL in your React frontend:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-app.railway.app';

// Example API call
const response = await fetch(`${API_BASE_URL}/api/generate`);
const data = await response.json();
```

## CORS Configuration (If Needed)

If your React frontend is on a different domain, add Flask-CORS:

```bash
pip install flask-cors
```

Then in `app/__init__.py`:

```python
from flask import Flask
from flask_cors import CORS

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # ... rest of your code
```

## Troubleshooting

### Check Logs
- Go to your Railway project dashboard
- Click on your service
- View the "Deployments" tab for build logs
- View the "Logs" tab for runtime logs

### Common Issues

1. **Build fails**: Check `requirements.txt` for incompatible versions
2. **Health check fails**: Verify the app starts and responds at `/health`
3. **Port errors**: Railway automatically sets `PORT`, no manual config needed
4. **Import errors**: Ensure all dependencies are in `requirements.txt`

## Next Steps

1. Deploy to Railway
2. Test all API endpoints with your deployed URL
3. Update your React frontend to use the Railway backend URL
4. Consider adding:
   - Database for storing user preferences
   - Caching for FPL API responses
   - Authentication for user accounts
   - Rate limiting for API endpoints

