# Movie Database System - Backend API

A Flask REST API for managing a movie database with complete CRUD operations, search functionality, and relationship management.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Database

```bash
# Set your MySQL connection
export DATABASE_URL="mysql+pymysql://root:your_password@localhost/moviedb"

# Make sure moviedb database exists in MySQL
```

### 3. Run the API

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Movies

- `GET /movies` - List movies with search, filtering, and pagination
- `GET /movies/{id}` - Get movie details with cast and crew
- `POST /movies` - Create new movie
- `PUT /movies/{id}` - Update movie
- `DELETE /movies/{id}` - Delete movie
- `GET /movies/top-rated` - Get highest rated movies
- `GET /movies/by-year/{year}` - Get movies by release year
- `GET /movies/stats` - Get database statistics

### Genres

- `GET /genres` - List all genres
- `GET /genres/{id}/movies` - Get movies by genre
- `POST /genres` - Create genre
- `PUT /genres/{id}` - Update genre
- `DELETE /genres/{id}` - Delete genre

### People

- `GET /people` - List people with search
- `GET /people/{id}` - Get person details with their movies
- `POST /people` - Create person
- `PUT /people/{id}` - Update person
- `DELETE /people/{id}` - Delete person

### Search

- `GET /search?q=query` - Global search across movies, people, and genres

### Health Check

- `GET /health` - API status check

## Example Usage

### Get all movies

```bash
curl http://localhost:5000/movies
```

### Search movies

```bash
curl "http://localhost:5000/movies?search=john&sort=rating&page=1&per_page=10"
```

### Get movie details

```bash
curl http://localhost:5000/movies/1
```

### Get top rated movies

```bash
curl "http://localhost:5000/movies/top-rated?limit=5"
```

### Global search

```bash
curl "http://localhost:5000/search?q=keanu"
```
