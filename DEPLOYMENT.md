# Deployment Guide

This guide covers deploying the EmptyCup Designer Shortlist Platform to production using Netlify (frontend) and Railway (backend with PostgreSQL).

## Architecture Overview

```
Frontend (React) → Netlify
Backend (Flask API) → Railway
Database → Railway PostgreSQL
```

## Prerequisites

1. GitHub account with your code repository
2. Netlify account ([netlify.com](https://netlify.com))
3. Railway account ([railway.app](https://railway.app))

## Step 1: Backend Deployment (Railway)

### 1.1 Add PostgreSQL Database
1. Go to [railway.app](https://railway.app) and sign up/login
2. Click "New Project"
3. Add a PostgreSQL database service:
   - Click "New Service" → "Database" → "PostgreSQL"
   - Railway will automatically provision the database
   - Note the `DATABASE_URL` environment variable

### 1.2 Deploy Flask API
1. In the same Railway project, click "New Service"
2. Choose "Deploy from GitHub repo"
3. Connect your GitHub account and select your repository
4. Railway will automatically detect the Flask application using `Dockerfile.backend`

### 1.3 Configure Environment Variables
Railway automatically sets:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Application port

Optional variables you can add:
```
FLASK_ENV=production
FLASK_DEBUG=False
```

### 1.4 Deploy and Test
1. Railway will automatically deploy your application
2. Note the deployment URL (e.g., `https://your-app.railway.app`)
3. Test the API endpoints:
   - Health check: `https://your-app.railway.app/api/health`
   - Designers: `https://your-app.railway.app/api/designers`
   - Admin dashboard: `https://your-app.railway.app/`

## Step 2: Frontend Deployment (Netlify)

### 2.1 Deploy to Netlify
1. Go to [netlify.com](https://netlify.com) and sign up/login
2. Click "New site from Git"
3. Connect to GitHub and select your repository
4. Configure build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
   - **Base directory**: (leave empty)

### 2.2 Add Environment Variables
1. Go to Site settings → Environment variables
2. Add the following variables:
   ```
   VITE_API_BASE_URL=https://your-app.railway.app/api
   VITE_ENVIRONMENT=production
   ```

### 2.3 Deploy
1. Click "Deploy site"
2. Netlify will build and deploy your frontend
3. Once deployed, you'll get a URL like `https://amazing-name-123456.netlify.app`

## Step 3: Testing Production Deployment

### 3.1 Test Backend API
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

### 3.2 Test Frontend
1. Open your Netlify URL
2. Verify designers load from the API
3. Test shortlisting functionality
4. Test report functionality
5. Check browser console for any errors

## Step 4: Custom Domain (Optional)

### 4.1 Frontend Domain (Netlify)
1. Go to Site settings → Domain management
2. Click "Add custom domain"
3. Follow DNS configuration instructions

### 4.2 Backend Domain (Railway)
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
   - Check Railway PostgreSQL service is active
   - Ensure database and API are in the same Railway project

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

3. **Railway Database Monitoring**
   - Go to your PostgreSQL service in Railway
   - Monitor database performance and usage in the metrics tab

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
   - Railway PostgreSQL is automatically secured within the platform
   - Database is only accessible from within your Railway project
   - Regular security updates handled by Railway

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
   - Monitor query performance in Railway metrics
   - Consider upgrading Railway plan for higher traffic

## Maintenance

1. **Regular Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Test updates in staging environment

2. **Backups**
   - Railway provides automatic backups for PostgreSQL
   - Consider additional backup strategies for critical data
   - Test backup restoration procedures

3. **Monitoring**
   - Set up uptime monitoring
   - Monitor error rates and performance
   - Set up alerts for critical issues
