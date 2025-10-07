import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from config import Config
from models import db, Movie, Genre, Person, Role, MovieGenre, MoviePerson

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)  # Enable CORS for frontend requests

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    # GET /movies?search=shaw&page=1&per_page=10&genre=Drama
    @app.route("/movies", methods=["GET"])
    def list_movies():
        q = Movie.query
        search = request.args.get("search")
        if search:
            like = f"%{search}%"
            q = q.filter(Movie.title.ilike(like))
        genre = request.args.get("genre")
        if genre:
            q = q.join(Movie.genres).filter(Genre.genre_name == genre)
        sort = request.args.get("sort", "title")  # title, rating, release_year
        if sort == "rating":
            q = q.order_by(Movie.rating.desc().nullslast())
        elif sort == "release_year":
            q = q.order_by(Movie.release_year.desc().nullslast())
        else:
            q = q.order_by(Movie.title.asc())

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        pagination = q.paginate(page=page, per_page=per_page, error_out=False)
        items = [m.to_dict(include_relations=False) for m in pagination.items]
        return jsonify({
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "items": items
        })

    @app.route("/movies/<int:movie_id>", methods=["GET"])
    def movie_detail(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        return jsonify(movie.to_dict(include_relations=True))

    @app.route("/genres", methods=["GET"])
    def list_genres():
        genres = Genre.query.order_by(Genre.genre_name).all()
        return jsonify([{"genre_id": g.genre_id, "genre_name": g.genre_name} for g in genres])

    @app.route("/genres/<int:genre_id>/movies", methods=["GET"])
    def movies_by_genre(genre_id):
        try:
            g = Genre.query.get_or_404(genre_id)
            movies = []
            try:
                movies = [m.to_dict(include_relations=False) for m in g.movies]
            except:
                movies = []
            return jsonify({"genre": g.genre_name, "movies": movies})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/people", methods=["GET"])
    def list_people():
        q = Person.query
        name = request.args.get("name")
        if name:
            like = f"%{name}%"
            q = q.filter((Person.first_name + " " + Person.last_name).ilike(like))
        people = q.limit(100).all()
        return jsonify([{"person_id": p.person_id, "name": p.full_name()} for p in people])

    @app.route("/people/<int:person_id>", methods=["GET"])
    def person_detail(person_id):
        try:
            p = Person.query.get_or_404(person_id)
            # list movies and roles
            movies = []
            try:
                rows = MoviePerson.query.filter_by(person_id=person_id).all()
                for mp in rows:
                    movie = Movie.query.get(mp.movie_id)
                    role = Role.query.get(mp.role_id)
                    if movie and role:
                        movies.append({
                            "movie_id": movie.movie_id, 
                            "title": movie.title, 
                            "role": role.role_name
                        })
            except:
                movies = []
            return jsonify({"person_id": p.person_id, "name": p.full_name(), "movies": movies})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/roles", methods=["GET"])
    def list_roles():
        return jsonify([{"role_id": r.role_id, "role_name": r.role_name} for r in Role.query.all()])

    # CRUD Operations for Movies
    @app.route("/movies", methods=["POST"])
    def create_movie():
        data = request.json or {}
        if "title" not in data:
            return jsonify({"error": "title required"}), 400
        
        try:
            m = Movie(
                title=data.get("title"),
                release_year=data.get("release_year"),
                duration=data.get("duration"),
                rating=data.get("rating")
            )
            db.session.add(m)
            db.session.commit()
            return jsonify(m.to_dict(False)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/movies/<int:movie_id>", methods=["PUT"])
    def update_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        data = request.json or {}
        
        try:
            if "title" in data:
                movie.title = data["title"]
            if "release_year" in data:
                movie.release_year = data["release_year"]
            if "duration" in data:
                movie.duration = data["duration"]
            if "rating" in data:
                movie.rating = data["rating"]
            
            db.session.commit()
            return jsonify(movie.to_dict(False))
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        try:
            db.session.delete(movie)
            db.session.commit()
            return jsonify({"message": "Movie deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    # Advanced Query Endpoints
    @app.route("/movies/top-rated", methods=["GET"])
    def top_rated_movies():
        limit = int(request.args.get("limit", 10))
        movies = Movie.query.filter(Movie.rating.isnot(None)).order_by(Movie.rating.desc()).limit(limit).all()
        return jsonify([m.to_dict(include_relations=True) for m in movies])

    @app.route("/movies/by-year/<int:year>", methods=["GET"])
    def movies_by_year(year):
        movies = Movie.query.filter_by(release_year=year).all()
        return jsonify([m.to_dict(include_relations=False) for m in movies])

    @app.route("/movies/years", methods=["GET"])
    def get_movie_years():
        years = db.session.query(Movie.release_year).distinct().order_by(Movie.release_year.desc()).all()
        return jsonify([year[0] for year in years if year[0] is not None])

    @app.route("/movies/stats", methods=["GET"])
    def movie_stats():
        total_movies = Movie.query.count()
        avg_rating = db.session.query(db.func.avg(Movie.rating)).scalar()
        total_genres = Genre.query.count()
        total_people = Person.query.count()
        
        return jsonify({
            "total_movies": total_movies,
            "average_rating": round(avg_rating, 2) if avg_rating else None,
            "total_genres": total_genres,
            "total_people": total_people
        })

    # CRUD Operations for Genres
    @app.route("/genres", methods=["POST"])
    def create_genre():
        data = request.json or {}
        if "genre_name" not in data:
            return jsonify({"error": "genre_name required"}), 400
        
        try:
            genre = Genre(genre_name=data["genre_name"])
            db.session.add(genre)
            db.session.commit()
            return jsonify({"genre_id": genre.genre_id, "genre_name": genre.genre_name}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/genres/<int:genre_id>", methods=["PUT"])
    def update_genre(genre_id):
        genre = Genre.query.get_or_404(genre_id)
        data = request.json or {}
        
        try:
            if "genre_name" in data:
                genre.genre_name = data["genre_name"]
            db.session.commit()
            return jsonify({"genre_id": genre.genre_id, "genre_name": genre.genre_name})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/genres/<int:genre_id>", methods=["DELETE"])
    def delete_genre(genre_id):
        genre = Genre.query.get_or_404(genre_id)
        try:
            db.session.delete(genre)
            db.session.commit()
            return jsonify({"message": "Genre deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    # CRUD Operations for People
    @app.route("/people", methods=["POST"])
    def create_person():
        data = request.json or {}
        if not data.get("first_name") or not data.get("last_name"):
            return jsonify({"error": "first_name and last_name required"}), 400
        
        try:
            person = Person(
                first_name=data["first_name"],
                last_name=data["last_name"],
                dob=data.get("dob")
            )
            db.session.add(person)
            db.session.commit()
            return jsonify({"person_id": person.person_id, "name": person.full_name()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/people/<int:person_id>", methods=["PUT"])
    def update_person(person_id):
        person = Person.query.get_or_404(person_id)
        data = request.json or {}
        
        try:
            if "first_name" in data:
                person.first_name = data["first_name"]
            if "last_name" in data:
                person.last_name = data["last_name"]
            if "dob" in data:
                person.dob = data["dob"]
            
            db.session.commit()
            return jsonify({"person_id": person.person_id, "name": person.full_name()})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/people/<int:person_id>", methods=["DELETE"])
    def delete_person(person_id):
        person = Person.query.get_or_404(person_id)
        try:
            db.session.delete(person)
            db.session.commit()
            return jsonify({"message": "Person deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    # Movie-Person Relationship Management
    @app.route("/movies/<int:movie_id>/people", methods=["POST"])
    def add_person_to_movie(movie_id):
        data = request.json or {}
        if not data.get("person_id") or not data.get("role_id"):
            return jsonify({"error": "person_id and role_id required"}), 400
        
        try:
            # Check if relationship already exists
            existing = MoviePerson.query.filter_by(
                movie_id=movie_id, 
                person_id=data["person_id"], 
                role_id=data["role_id"]
            ).first()
            
            if existing:
                return jsonify({"error": "Person already has this role in this movie"}), 400
            
            mp = MoviePerson(
                movie_id=movie_id,
                person_id=data["person_id"],
                role_id=data["role_id"]
            )
            db.session.add(mp)
            db.session.commit()
            return jsonify({"message": "Person added to movie successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/movies/<int:movie_id>/people/<int:person_id>/roles/<int:role_id>", methods=["DELETE"])
    def remove_person_from_movie(movie_id, person_id, role_id):
        mp = MoviePerson.query.filter_by(
            movie_id=movie_id, 
            person_id=person_id, 
            role_id=role_id
        ).first_or_404()
        
        try:
            db.session.delete(mp)
            db.session.commit()
            return jsonify({"message": "Person removed from movie successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    # Movie-Genre Relationship Management
    @app.route("/movies/<int:movie_id>/genres", methods=["POST"])
    def add_genre_to_movie(movie_id):
        data = request.json or {}
        if not data.get("genre_id"):
            return jsonify({"error": "genre_id required"}), 400
        
        try:
            # Check if relationship already exists
            existing = MovieGenre.query.filter_by(
                movie_id=movie_id, 
                genre_id=data["genre_id"]
            ).first()
            
            if existing:
                return jsonify({"error": "Movie already has this genre"}), 400
            
            mg = MovieGenre(movie_id=movie_id, genre_id=data["genre_id"])
            db.session.add(mg)
            db.session.commit()
            return jsonify({"message": "Genre added to movie successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route("/movies/<int:movie_id>/genres/<int:genre_id>", methods=["DELETE"])
    def remove_genre_from_movie(movie_id, genre_id):
        mg = MovieGenre.query.filter_by(
            movie_id=movie_id, 
            genre_id=genre_id
        ).first_or_404()
        
        try:
            db.session.delete(mg)
            db.session.commit()
            return jsonify({"message": "Genre removed from movie successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    # Search and Filter Endpoints
    @app.route("/search", methods=["GET"])
    def search_all():
        query = request.args.get("q", "")
        if not query:
            return jsonify({"error": "Query parameter 'q' required"}), 400
        
        results = {
            "movies": [],
            "people": [],
            "genres": []
        }
        
        # Search movies
        movie_results = Movie.query.filter(Movie.title.ilike(f"%{query}%")).limit(10).all()
        results["movies"] = [m.to_dict(include_relations=False) for m in movie_results]
        
        # Search people
        people_results = Person.query.filter(
            (Person.first_name + " " + Person.last_name).ilike(f"%{query}%")
        ).limit(10).all()
        results["people"] = [{"person_id": p.person_id, "name": p.full_name()} for p in people_results]
        
        # Search genres
        genre_results = Genre.query.filter(Genre.genre_name.ilike(f"%{query}%")).limit(10).all()
        results["genres"] = [{"genre_id": g.genre_id, "genre_name": g.genre_name} for g in genre_results]
        
        return jsonify(results)

    # Quick fix endpoint to add sample relationships (for demo purposes)
    @app.route("/setup-relationships", methods=["POST"])
    def setup_relationships():
        try:
            # Add some movie-genre relationships
            from models import MovieGenre, MoviePerson
            
            # Add movie-genre relationships
            relationships = [
                MovieGenre(movie_id=1, genre_id=1),  # John Wick - Action
                MovieGenre(movie_id=3, genre_id=1),  # Avengers - Action
                MovieGenre(movie_id=3, genre_id=8),  # Avengers - Adventure
                MovieGenre(movie_id=5, genre_id=1),  # Dark Knight - Action
                MovieGenre(movie_id=5, genre_id=3),  # Dark Knight - Drama
                MovieGenre(movie_id=6, genre_id=3),  # Forrest Gump - Drama
                MovieGenre(movie_id=6, genre_id=2),  # Forrest Gump - Comedy
            ]
            
            for rel in relationships:
                db.session.add(rel)
            
            # Add movie-person relationships
            person_relationships = [
                MoviePerson(movie_id=1, person_id=1, role_id=1),  # John Wick - Keanu - Actor
                MoviePerson(movie_id=3, person_id=5, role_id=1),  # Avengers - Robert Downey Jr - Actor
                MoviePerson(movie_id=5, person_id=7, role_id=1),  # Dark Knight - Christian Bale - Actor
                MoviePerson(movie_id=6, person_id=8, role_id=1),  # Forrest Gump - Tom Hanks - Actor
            ]
            
            for rel in person_relationships:
                db.session.add(rel)
            
            db.session.commit()
            
            return jsonify({
                "message": "Sample relationships added successfully!",
                "movie_genres": len(relationships),
                "movie_people": len(person_relationships)
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return app

# Create app instance for gunicorn
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
