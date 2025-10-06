# Railway Deployment Guide

## Files Created/Modified for Railway

### 1. Procfile

```
web: gunicorn app:create_app() --bind 0.0.0.0:$PORT
```

### 2. runtime.txt

```
python-3.12.0
```

### 3. requirements.txt (updated)

- Added `gunicorn>=21.0.0` for production server

### 4. app.py (updated)

- Added `import os`
- Updated to use `PORT` environment variable
- Set `host="0.0.0.0"` for Railway
- Disabled debug mode for production

## Railway Deployment Steps

### 1. Create Railway Account

- Go to [railway.app](https://railway.app)
- Sign up with GitHub

### 2. Deploy from GitHub

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Select the `backend` folder as the root directory

### 3. Environment Variables

Set these in Railway dashboard:

```
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
PORT=5000
```

### 4. Database Setup

You'll need to:

1. Add a MySQL database service in Railway
2. Get the connection string from Railway
3. Update the `DATABASE_URL` environment variable

### 5. Deploy

Railway will automatically:

- Install dependencies from `requirements.txt`
- Use the `Procfile` to start the application
- Use `runtime.txt` for Python version

## Testing Your Deployment

Once deployed, test these endpoints:

```bash
# Health check
curl https://your-app-name.railway.app/health

# Get movies
curl https://your-app-name.railway.app/movies

# Search
curl "https://your-app-name.railway.app/search?q=test"
```

## Troubleshooting

### Common Issues:

1. **Database Connection**: Make sure `DATABASE_URL` is correctly set
2. **Port Issues**: Railway sets `PORT` automatically, don't hardcode it
3. **Dependencies**: All packages in `requirements.txt` must be available

### Logs:

Check Railway dashboard logs for any errors during deployment.

## Production Considerations

- Database should be properly configured with credentials
- CORS is enabled for frontend integration
- All API endpoints are ready for frontend consumption
- Error handling is implemented for all routes
