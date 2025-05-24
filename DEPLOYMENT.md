# Deployment Guide

This guide covers deploying the EmptyCup Designer Shortlist Platform to production using Netlify (frontend) and Railway (backend).

## Architecture Overview

```
Frontend (React) → Netlify
Backend (Flask API) → Railway  
Database → Supabase PostgreSQL
```

## Prerequisites

1. GitHub account with your code repository
2. Netlify account ([netlify.com](https://netlify.com))
3. Railway account ([railway.app](https://railway.app))
4. Supabase account ([supabase.com](https://supabase.com))

## Step 1: Database Setup (Supabase)

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - Name: `emptycup-designers`
   - Database Password: (generate a strong password)
   - Region: Choose closest to your users
5. Click "Create new project"

### 1.2 Get Database Connection String
1. Go to Project Settings → Database
2. Copy the connection string under "Connection string"
3. Replace `[YOUR-PASSWORD]` with your actual password
4. Save this for Railway deployment

Example:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

## Step 2: Backend Deployment (Railway)

### 2.1 Deploy to Railway
1. Go to [railway.app](https://railway.app) and sign up/login
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select your repository
5. Railway will auto-detect the Flask app

### 2.2 Configure Railway Settings
1. In Railway dashboard, click on your service
2. Go to "Settings" tab
3. Set **Root Directory** to: `api`
4. Set **Build Command** to: `pip install -r requirements.txt`
5. Set **Start Command** to: `gunicorn --bind 0.0.0.0:$PORT app:app`

### 2.3 Add Environment Variables
1. Go to "Variables" tab in Railway
2. Add the following variables:
   ```
   DATABASE_URL=your_supabase_connection_string
   FLASK_ENV=production
   ```

### 2.4 Deploy
1. Railway will automatically deploy your app
2. Once deployed, copy the public URL (e.g., `https://your-app.railway.app`)
3. Test the API: `https://your-app.railway.app/api/health`

## Step 3: Frontend Deployment (Netlify)

### 3.1 Deploy to Netlify
1. Go to [netlify.com](https://netlify.com) and sign up/login
2. Click "New site from Git"
3. Connect to GitHub and select your repository
4. Configure build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
   - **Base directory**: (leave empty)

### 3.2 Add Environment Variables
1. Go to Site settings → Environment variables
2. Add the following variables:
   ```
   VITE_API_BASE_URL=https://your-app.railway.app/api
   VITE_ENVIRONMENT=production
   ```

### 3.3 Deploy
1. Click "Deploy site"
2. Netlify will build and deploy your frontend
3. Once deployed, you'll get a URL like `https://amazing-name-123456.netlify.app`

## Step 4: Testing Production Deployment

### 4.1 Test Backend API
```bash
# Health check
curl https://your-app.railway.app/api/health

# Get designers
curl https://your-app.railway.app/api/designers

# Test shortlist (should return success)
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_session": "test"}' \
  https://your-app.railway.app/api/designers/1/shortlist
```

### 4.2 Test Frontend
1. Open your Netlify URL
2. Verify designers load from the API
3. Test shortlisting functionality
4. Test report functionality
5. Check browser console for any errors

## Step 5: Custom Domain (Optional)

### 5.1 Frontend Domain (Netlify)
1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Follow DNS configuration instructions

### 5.2 Backend Domain (Railway)
1. Go to your service settings
2. Click "Networking" tab
3. Add custom domain
4. Configure DNS records

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure your frontend URL is allowed in Flask-CORS
   - Check browser console for specific CORS errors

2. **Database Connection Issues**
   - Verify DATABASE_URL is correct
   - Check Supabase project is active
   - Ensure IP restrictions allow Railway connections

3. **Build Failures**
   - Check build logs in Railway/Netlify
   - Verify all dependencies are in requirements.txt/package.json
   - Ensure Python/Node versions are compatible

4. **Environment Variables**
   - Double-check all environment variables are set
   - Restart services after adding new variables
   - Verify variable names match exactly

### Monitoring

1. **Railway Logs**
   - Go to your service → Deployments
   - Click on latest deployment to view logs
   - Monitor for errors or performance issues

2. **Netlify Logs**
   - Go to Site overview → Functions (if using)
   - Check deploy logs for build issues

3. **Supabase Monitoring**
   - Go to Project → Reports
   - Monitor database performance and usage

## Security Considerations

1. **Environment Variables**
   - Never commit `.env` files to Git
   - Use different databases for development/production
   - Rotate database passwords regularly

2. **API Security**
   - Consider adding rate limiting
   - Implement proper authentication for production
   - Use HTTPS only in production

3. **Database Security**
   - Enable Row Level Security in Supabase
   - Limit database access to necessary IPs
   - Regular security updates

## Performance Optimization

1. **Frontend**
   - Enable Netlify's asset optimization
   - Use CDN for static assets
   - Implement lazy loading for images

2. **Backend**
   - Use connection pooling for database
   - Implement caching for frequently accessed data
   - Monitor and optimize slow queries

3. **Database**
   - Add indexes for frequently queried columns
   - Monitor query performance in Supabase
   - Consider read replicas for high traffic

## Maintenance

1. **Regular Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Test updates in staging environment

2. **Backups**
   - Supabase provides automatic backups
   - Consider additional backup strategies for critical data
   - Test backup restoration procedures

3. **Monitoring**
   - Set up uptime monitoring
   - Monitor error rates and performance
   - Set up alerts for critical issues
