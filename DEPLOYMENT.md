# Railway Deployment Guide for EquiHealth App

## Prerequisites
1. Railway account (sign up at https://railway.app)
2. Git repository with your code
3. GitHub account (recommended for easy deployment)

## Deployment Steps

### Method 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Railway deployment"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account if not already connected
   - Select your repository
   - Railway will automatically detect it's a Python app and deploy it

### Method 2: Deploy using Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and deploy:**
   ```bash
   railway init
   railway up
   ```

## Environment Variables

After deployment, set these environment variables in Railway:

1. Go to your Railway project dashboard
2. Click on "Variables" tab
3. Add the following variables:

- `SECRET_KEY`: Generate a secure random string (e.g., `python -c "import secrets; print(secrets.token_hex(32))"`)
- `FLASK_ENV`: Set to `production`

## Important Files Created for Deployment

1. **Procfile**: Tells Railway how to run your app
2. **requirements.txt**: Updated with specific versions and gunicorn
3. **runtime.txt**: Specifies Python version
4. **railway.json**: Railway-specific configuration
5. **.gitignore**: Excludes unnecessary files from deployment
6. **.env.example**: Template for environment variables

## Post-Deployment Checklist

1. ✅ App starts without errors
2. ✅ Health check endpoint works (`/health`)
3. ✅ Static files are served correctly
4. ✅ File uploads work (Railway has persistent storage for uploads)
5. ✅ Generated maps are saved and accessible
6. ✅ User sessions work correctly

## Monitoring and Logs

- View logs in Railway dashboard under "Deployments" tab
- Monitor app performance in Railway metrics
- Set up custom domain if needed in Railway settings

## Troubleshooting

### Common Issues:

1. **Import errors**: Check that all dependencies are in requirements.txt
2. **File permission errors**: Ensure static directory has write permissions
3. **Memory issues**: Upgrade Railway plan if needed for machine learning models
4. **Timeout errors**: Increase timeout settings in railway.json

### Debugging Steps:

1. Check Railway deployment logs
2. Verify environment variables are set
3. Test locally with production settings:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   gunicorn app:app
   ```

## Performance Optimization

1. **Static files**: Consider using a CDN for static assets
2. **Database**: Replace in-memory storage with a proper database (PostgreSQL, Railway provides free instances)
3. **Caching**: Implement caching for prediction results
4. **File storage**: Use cloud storage (S3, Railway Volumes) for persistent file storage

## Security Considerations

1. ✅ Secret key is set via environment variable
2. ✅ Debug mode is disabled in production
3. 🔄 Consider implementing proper user authentication with a database
4. 🔄 Add CSRF protection for forms
5. 🔄 Implement rate limiting for file uploads

## Scaling

Railway automatically handles scaling, but consider:
- Upgrading to a higher tier for better performance
- Implementing a proper database for user data persistence
- Using background jobs for heavy computations (map generation, ML predictions)

## Next Steps

1. Set up a proper database (PostgreSQL) for user data
2. Implement proper user authentication and authorization
3. Add error monitoring (Sentry)
4. Set up automated backups for user data
5. Implement proper logging
6. Add API endpoints for mobile apps if needed

## Support

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app
