# Movie Database API Documentation

## Base URL

```
http://localhost:5000
```

## Response Format

All responses are in JSON format. Error responses include an "error" field.

## Core Endpoints

### Movies

#### List Movies

- **GET** `/movies`
- **Query Parameters:**
  - `search` (string): Search by title
  - `genre` (string): Filter by genre name
  - `sort` (string): Sort by `title`, `rating`, or `release_year`
  - `page` (int): Page number (default: 1)
  - `per_page` (int): Items per page (default: 10)

**Example:**

```bash
GET /movies?search=john&sort=rating&page=1&per_page=10
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
      "title": "John Wick",
      "release_year": 2014,
      "duration": 101,
      "rating": 7.4
    }
  ]
}
```

#### Get Movie Details

- **GET** `/movies/{movie_id}`

**Response:**

```json
{
  "movie_id": 1,
  "title": "John Wick",
  "release_year": 2014,
  "duration": 101,
  "rating": 7.4,
  "genres": ["Action", "Thriller"],
  "people": [
    {
      "person_id": 1,
      "name": "Keanu Reeves",
      "role": "Actor"
    }
  ]
}
```

#### Create Movie

- **POST** `/movies`
- **Body:**

```json
{
  "title": "New Movie",
  "release_year": 2024,
  "duration": 120,
  "rating": 8.0
}
```

#### Update Movie

- **PUT** `/movies/{movie_id}`
- **Body:** Same as create (all fields optional)

#### Delete Movie

- **DELETE** `/movies/{movie_id}`

### Advanced Queries

#### Top Rated Movies

- **GET** `/movies/top-rated?limit=10`

#### Movies by Year

- **GET** `/movies/by-year/{year}`

#### Database Statistics

- **GET** `/movies/stats`

**Response:**

```json
{
  "total_movies": 10,
  "average_rating": 8.1,
  "total_genres": 10,
  "total_people": 30
}
```

### Genres

#### List Genres

- **GET** `/genres`

#### Movies by Genre

- **GET** `/genres/{genre_id}/movies`

#### Create/Update/Delete Genre

- **POST** `/genres`
- **PUT** `/genres/{genre_id}`
- **DELETE** `/genres/{genre_id}`

### People

#### List People

- **GET** `/people?name=search_term`

#### Get Person Details

- **GET** `/people/{person_id}`

**Response:**

```json
{
  "person_id": 1,
  "name": "Keanu Reeves",
  "movies": [
    {
      "movie_id": 1,
      "title": "John Wick",
      "role": "Actor"
    }
  ]
}
```

#### Create/Update/Delete Person

- **POST** `/people`
- **PUT** `/people/{person_id}`
- **DELETE** `/people/{person_id}`

### Search

#### Global Search

- **GET** `/search?q=query`

**Response:**

```json
{
  "movies": [...],
  "people": [...],
  "genres": [...]
}
```

### Health Check

- **GET** `/health`

**Response:**

```json
{ "status": "ok" }
```

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

Error format:

```json
{
  "error": "Error message"
}
```

## Frontend Integration Examples

### JavaScript/Fetch

```javascript
// Get all movies
const movies = await fetch("http://localhost:5000/movies").then((r) =>
  r.json()
);

// Search movies
const searchResults = await fetch(
  "http://localhost:5000/movies?search=john"
).then((r) => r.json());

// Get movie details
const movie = await fetch("http://localhost:5000/movies/1").then((r) =>
  r.json()
);

// Create new movie
const newMovie = await fetch("http://localhost:5000/movies", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    title: "New Movie",
    release_year: 2024,
    duration: 120,
    rating: 8.0,
  }),
}).then((r) => r.json());
```

### React Example

```jsx
const [movies, setMovies] = useState([]);

useEffect(() => {
  fetch("http://localhost:5000/movies")
    .then((response) => response.json())
    .then((data) => setMovies(data.items));
}, []);
```
