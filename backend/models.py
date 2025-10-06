from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for Movie <-> Genre (composite PK)
class MovieGenre(db.Model):
    __tablename__ = "moviegenre"
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.genre_id"), primary_key=True)

# Association table for Movie <-> Person with Role
class MoviePerson(db.Model):
    __tablename__ = "movieperson"
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.person_id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"), primary_key=True)

class Movie(db.Model):
    __tablename__ = "movie"
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer)
    duration = db.Column(db.Integer)  # minutes
    rating = db.Column(db.Numeric(3, 1))

    genres = db.relationship("Genre", secondary="moviegenre", back_populates="movies")
    people = db.relationship("Person", secondary="movieperson", back_populates="movies")

    def to_dict(self, include_relations=True):
        d = dict(
            movie_id=self.movie_id,
            title=self.title,
            release_year=self.release_year,
            duration=self.duration,
            rating=self.rating,
        )
        if include_relations:
            try:
                d["genres"] = [g.genre_name for g in self.genres]
            except:
                d["genres"] = []
            
            # include persons with roles
            persons = []
            try:
                for mp in MoviePerson.query.filter_by(movie_id=self.movie_id).all():
                    person = Person.query.get(mp.person_id)
                    role = Role.query.get(mp.role_id)
                    if person and role:
                        persons.append({
                            "person_id": person.person_id, 
                            "name": f"{person.first_name} {person.last_name}", 
                            "role": role.role_name
                        })
            except:
                pass
            d["people"] = persons
        return d

class Genre(db.Model):
    __tablename__ = "genre"
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(50), nullable=False)

    movies = db.relationship("Movie", secondary="moviegenre", back_populates="genres")

class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date)

    movies = db.relationship("Movie", secondary="movieperson", back_populates="people")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Role(db.Model):
    __tablename__ = "role"
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
