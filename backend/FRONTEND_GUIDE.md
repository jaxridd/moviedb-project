# Movie Database API - Frontend Integration Guide

## 🚀 Live API URL
```
https://moviedb-project-production-cd2f.up.railway.app
```

## 📋 Quick Start for Frontend Developers

### Base URL
```javascript
const API_BASE = 'https://moviedb-project-production-cd2f.up.railway.app';
```

### Key Endpoints

#### 1. Get All Movies
```javascript
GET /movies
```
**Response:**
```json
{
  "total": 10,
  "page": 1,
  "per_page": 10,
  "items": [
    {
      "movie_id": 1,
      "title": "Avengers: Endgame",
      "release_year": 2019,
      "duration": 181,
      "rating": "8.4"
    }
  ]
}
```

#### 2. Get Movie Details
```javascript
GET /movies/{id}
```
**Response:**
```json
{
  "movie_id": 1,
  "title": "Avengers: Endgame",
  "release_year": 2019,
  "duration": 181,
  "rating": "8.4",
  "genres": ["Action", "Adventure"],
  "people": [
    {
      "person_id": 1,
      "name": "Robert Downey Jr.",
      "role": "Actor"
    }
  ]
}
```

#### 3. Search Movies
```javascript
GET /movies?search=avengers&sort=rating&page=1&per_page=10
```

#### 4. Get Genres
```javascript
GET /genres
```
**Response:**
```json
[
  {"genre_id": 1, "genre_name": "Action"},
  {"genre_id": 2, "genre_name": "Comedy"},
  {"genre_id": 3, "genre_name": "Drama"}
]
```

#### 5. Get People
```javascript
GET /people
```
**Response:**
```json
[
  {"person_id": 1, "name": "Robert Downey Jr."},
  {"person_id": 2, "name": "Chris Evans"}
]
```

#### 6. Global Search
```javascript
GET /search?q=avengers
```
**Response:**
```json
{
  "movies": [...],
  "people": [...],
  "genres": [...]
}
```

## 🎯 Frontend Examples

### React Example
```jsx
import React, { useState, useEffect } from 'react';

const MovieList = () => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://moviedb-project-production-cd2f.up.railway.app/movies')
      .then(response => response.json())
      .then(data => {
        setMovies(data.items);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {movies.map(movie => (
        <div key={movie.movie_id}>
          <h3>{movie.title}</h3>
          <p>Year: {movie.release_year} | Rating: {movie.rating}</p>
        </div>
      ))}
    </div>
  );
};
```

### JavaScript/Fetch Example
```javascript
// Get all movies
const getMovies = async () => {
  const response = await fetch('https://moviedb-project-production-cd2f.up.railway.app/movies');
  const data = await response.json();
  return data.items;
};

// Search movies
const searchMovies = async (query) => {
  const response = await fetch(
    `https://moviedb-project-production-cd2f.up.railway.app/movies?search=${query}`
  );
  const data = await response.json();
  return data.items;
};

// Get movie details
const getMovieDetails = async (movieId) => {
  const response = await fetch(
    `https://moviedb-project-production-cd2f.up.railway.app/movies/${movieId}`
  );
  return await response.json();
};
```

## 🔧 Available Features

### Movies
- ✅ List all movies with pagination
- ✅ Search by title
- ✅ Filter by genre
- ✅ Sort by title, rating, or year
- ✅ Get movie details with cast/crew
- ✅ Create, update, delete movies

### Genres
- ✅ List all genres
- ✅ Get movies by genre
- ✅ Create, update, delete genres

### People
- ✅ List all people
- ✅ Search people by name
- ✅ Get person details with their movies
- ✅ Create, update, delete people

### Search
- ✅ Global search across movies, people, and genres
- ✅ Case-insensitive search

## 🎨 UI Suggestions

### Movie Cards
Display: Title, Year, Rating, Duration, Genres, Cast

### Search Bar
- Real-time search as user types
- Search across movies, people, genres

### Filters
- Filter by genre
- Filter by year range
- Sort by rating, year, title

### Movie Details Page
- Full movie information
- Cast and crew list
- Related movies by genre

## 🚨 Important Notes

- **CORS enabled** - No issues with cross-origin requests
- **All endpoints return JSON**
- **Error responses include error messages**
- **API is production-ready and stable**

## 📞 Support

If you encounter any issues with the API, check:
1. API is running: `GET /health` should return `{"status":"ok"}`
2. Correct endpoint URLs
3. Proper JSON request bodies for POST/PUT requests

**Happy coding! 🎬**
