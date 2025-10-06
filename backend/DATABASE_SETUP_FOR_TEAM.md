# Database Setup for Team Collaboration

## Problem
- Team A created database locally in MySQL Workbench
- Team C (Frontend) needs access to the same data
- Need shared database for all team members

## Solution: Railway MySQL Database

### Step 1: Create Railway MySQL Database

1. Go to your Railway project dashboard
2. Click "New Service" 
3. Select "Database" → "MySQL"
4. Railway will create a managed MySQL database
5. Note the connection details provided

### Step 2: Export Data from Local MySQL

```bash
# Export your local database
mysqldump -u root -p moviedb > team_a_data.sql
```

Or from MySQL Workbench:
1. Go to Server → Data Export
2. Select your `moviedb` database
3. Export to file: `team_a_data.sql`

### Step 3: Import to Railway Database

```bash
# Import to Railway MySQL
mysql -h [railway_host] -u [railway_user] -p [railway_database] < team_a_data.sql
```

Or use MySQL Workbench:
1. Create new connection to Railway database
2. Use connection details from Railway dashboard
3. Import the SQL file

### Step 4: Update Backend Configuration

Update your Railway environment variables:

```
DATABASE_URL=mysql+pymysql://[railway_user]:[railway_password]@[railway_host]:[port]/[railway_database]
```

### Step 5: Test Database Connection

```bash
# Test from your deployed API
curl https://your-app.railway.app/health
curl https://your-app.railway.app/movies
```

## Alternative: Free Cloud Databases

### PlanetScale (MySQL-compatible)
- Free tier: 1GB storage, 1 billion reads/month
- Easy import from MySQL
- Branching for development

### Supabase (PostgreSQL)
- Free tier: 500MB database
- Built-in API generation
- Real-time subscriptions

## Team C Access

Once deployed, Team C can access:

### API Base URL
```
https://your-app-name.railway.app
```

### Key Endpoints for Frontend
```javascript
// Get all movies
GET /movies

// Search movies
GET /movies?search=shaw&sort=rating

// Get movie details
GET /movies/1

// Get genres
GET /genres

// Get people
GET /people

// Global search
GET /search?q=keanu
```

### Example Frontend Code
```javascript
const API_BASE = 'https://your-app-name.railway.app';

// Fetch movies
const movies = await fetch(`${API_BASE}/movies`).then(r => r.json());

// Search movies
const searchResults = await fetch(`${API_BASE}/movies?search=john`).then(r => r.json());
```

## Database Schema (for Team C reference)

### Tables
- `movie` - Movie information
- `genre` - Movie genres  
- `person` - Actors, directors, etc.
- `role` - Actor, Director, Writer, etc.
- `moviegenre` - Movie-Genre relationships
- `movieperson` - Movie-Person-Role relationships

### Key Relationships
- Movies ↔ Genres (many-to-many)
- Movies ↔ People (many-to-many with roles)
- Each movie can have multiple genres
- Each person can have multiple roles in different movies

## Troubleshooting

### Connection Issues
- Check Railway database is running
- Verify DATABASE_URL format
- Ensure database has data imported

### Import Issues  
- Check SQL file format
- Verify table names match your models
- Ensure foreign key constraints are handled

### API Issues
- Check Railway deployment logs
- Verify all environment variables set
- Test health endpoint first
