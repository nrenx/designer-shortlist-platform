# 🚨 Railway Health Check Troubleshooting Guide

## Current Issue: Health Check Failing

Your Railway deployment is building successfully but failing the health check with "service unavailable" errors.

## 🔍 Immediate Troubleshooting Steps

### Step 1: Check Railway Logs
1. Go to your Railway project dashboard
2. Click on your backend service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Check the "Logs" section

**Look for these error patterns:**
- `Error: bind EADDRINUSE` - Port already in use
- `ModuleNotFoundError` - Missing dependencies
- `psycopg2.OperationalError` - Database connection issues
- `Permission denied` - File permission issues
- `Killed` - Out of memory errors

### Step 2: Test Locally
Run the health check test:
```bash
python test_health_endpoint.py
```

This will help identify if the issue is local or Railway-specific.

### Step 3: Check Database Connection
The most common cause is database connection issues. Verify:
1. PostgreSQL service is running in Railway
2. `DATABASE_URL` environment variable is set
3. Database and API are in the same Railway project

## 🛠️ Common Fixes

### Fix 1: Database Connection Issues

**Problem**: App can't connect to PostgreSQL database
**Solution**: Ensure PostgreSQL service is added to your Railway project

1. In Railway dashboard, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Wait for provisioning to complete
4. Redeploy your API service

### Fix 2: Port Binding Issues

**Problem**: App not listening on correct port
**Solution**: Already fixed in our configuration

✅ `Dockerfile.backend` uses `${PORT:-5001}`
✅ `railway.json` removed custom start command
✅ Gunicorn binds to `0.0.0.0:$PORT`

### Fix 3: Health Check Timeout

**Problem**: App takes too long to start
**Solution**: Already increased timeout to 300 seconds

✅ `railway.json` has `"healthcheckTimeout": 300`

### Fix 4: Memory Issues (Starter Plan)

**Problem**: App crashes due to memory limits (512MB)
**Solution**: Optimize memory usage

Update `Dockerfile.backend`:
```dockerfile
# Reduce workers for Starter Plan
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 1 --timeout 120 --access-logfile - --error-logfile - app:app"]
```

## 🔧 Advanced Debugging

### Check Railway Environment Variables
In Railway dashboard → Variables tab, verify:
- `DATABASE_URL` is automatically set by PostgreSQL service
- `PORT` is automatically set by Railway
- No conflicting environment variables

### Test Database Connection Manually
Add this temporary endpoint to `api/app.py` for debugging:

```python
@app.route('/api/debug', methods=['GET'])
def debug_info():
    """Debug endpoint to check environment"""
    return jsonify({
        'port': os.environ.get('PORT', 'Not set'),
        'database_url_set': bool(os.environ.get('DATABASE_URL')),
        'use_sqlite': USE_SQLITE,
        'python_version': sys.version,
        'working_directory': os.getcwd()
    })
```

### Enable Verbose Logging
Update `Dockerfile.backend` CMD to include more logging:
```dockerfile
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 1 --timeout 120 --log-level debug --access-logfile - --error-logfile - app:app"]
```

## 📋 Deployment Checklist

Before redeploying, verify:

- ✅ PostgreSQL service is running in Railway
- ✅ `DATABASE_URL` environment variable exists
- ✅ Latest code is pushed to GitHub
- ✅ `Dockerfile.backend` is in root directory
- ✅ `railway.json` points to `Dockerfile.backend`
- ✅ Health endpoint `/api/health` exists in Flask app
- ✅ App binds to `0.0.0.0:$PORT`

## 🚀 Quick Fix Commands

### 1. Commit Current Fixes
```bash
git add .
git commit -m "Fix Railway health check issues - remove Docker healthcheck, increase timeout"
git push origin main
```

### 2. Test Locally
```bash
python test_health_endpoint.py
```

### 3. Check Railway Logs
After redeployment, immediately check logs for:
- Database connection success/failure
- Port binding confirmation
- Any startup errors

## 🎯 Expected Success Indicators

When working correctly, Railway logs should show:
```
[INFO] Starting gunicorn 20.1.0
[INFO] Listening at: http://0.0.0.0:PORT (1)
[INFO] Using worker: sync
[INFO] Booting worker with pid: X
Database connection successful
Tables created/verified successfully
Sample data inserted successfully
```

And health check should pass:
```
Health check passed: /api/health returned 200
```

## 🆘 If Still Failing

### Last Resort Options:

1. **Simplify the App**: Temporarily remove database initialization
2. **Use Railway's PostgreSQL Template**: Start with Railway's Flask template
3. **Check Railway Status**: Verify no platform issues at status.railway.app
4. **Contact Railway Support**: With deployment logs and error details

### Alternative Health Check
If health check continues failing, try changing the path in `railway.json`:
```json
{
  "deploy": {
    "healthcheckPath": "/api/info",
    "healthcheckTimeout": 300
  }
}
```

The `/api/info` endpoint doesn't require database connection and might be more reliable.

## 📞 Getting Help

If you're still stuck:
1. Share Railway deployment logs
2. Share output from `test_health_endpoint.py`
3. Confirm PostgreSQL service status in Railway dashboard
4. Check if the issue persists with a fresh Railway project

The health check failure is usually one of these three issues:
1. **Database connection** (most common)
2. **Port binding** (fixed in our config)
3. **App startup errors** (check logs)

Let's get this working! 🚀
