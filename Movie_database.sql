
CREATE TABLE Movie (
    movie_id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    release_year INT,
    duration INT,
    rating DECIMAL(3,1)
);

CREATE TABLE Person (
    person_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    dob DATE
);

CREATE TABLE Role (
    role_id INT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL
);

CREATE TABLE Genre (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL
);

CREATE TABLE MovieGenre (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE MoviePerson (
    movie_id INT,
    person_id INT,
    role_id INT,
    PRIMARY KEY (movie_id, person_id, role_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (person_id) REFERENCES Person(person_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Role(role_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


INSERT INTO Role (role_id, role_name) VALUES
(1, 'Actor'),
(2, 'Director'),
(3, 'Producer'),
(4, 'Writer'),
(5, 'Cinematographer'),
(6, 'Editor'),
(7, 'Composer'),
(8, 'Costume Designer'),
(9, 'Makeup Artist'),
(10, 'Stunt Coordinator');


INSERT INTO Genre (genre_id, genre_name) VALUES
(1, 'Action'),
(2, 'Comedy'),
(3, 'Drama'),
(4, 'Thriller'),
(5, 'Sci-Fi'),
(6, 'Romance'),
(7, 'Horror'),
(8, 'Adventure'),
(9, 'Mystery'),
(10, 'Biography');


INSERT INTO Person (person_id, first_name, last_name, dob) VALUES
(1, 'Keanu', 'Reeves', '1964-09-02'),         
(2, 'Chad', 'Stahelski', '1968-09-20'),       
(3, 'Bradley', 'Cooper', '1975-01-05'),       
(4, 'Todd', 'Phillips', '1970-04-20'),        
(5, 'Robert', 'Downey Jr.', '1965-04-04'),    
(6, 'Anthony', 'Russo', '1970-02-03'),        
(7, 'Tom', 'Hanks', '1956-07-09'),            
(8, 'Steven', 'Spielberg', '1946-12-18'),     
(9, 'Adrien', 'Brody', '1973-04-14'),         
(10, 'J.K.', 'Simmons', '1955-01-09'),
(11, 'Ian', 'McShane', '1942-09-29'),
(12, 'Justin', 'Bartha', '1978-07-21'),
(13, 'Chris', 'Evans', '1981-06-13'),
(14, 'Mark', 'Ruffalo', '1967-11-22'),
(15, 'Matthew', 'McConaughey', '1969-11-04'),
(16, 'Christian', 'Bale', '1974-01-30'),
(17, 'Gary', 'Sinise', '1955-03-17'),
(18, 'Thomas', 'Kretschmann', '1962-09-08'),
(19, 'Paul', 'Reiser', '1957-03-30'),
(20, 'Al', 'Pacino', '1940-04-25'),
(21, 'David', 'Leitch', '1970-07-18'),
(22, 'Todd', 'Phillips', '1970-04-20'),
(23, 'Anthony', 'Russo', '1970-02-03'),
(24, 'Joe', 'Russo', '1971-07-08'),
(25, 'Christopher', 'Nolan', '1970-07-30'),
(26, 'Christopher', 'Nolan', '1970-07-30'),
(27, 'Roman', 'Polanski', '1933-08-18'),
(28, 'Robert', 'Zemeckis', '1952-05-14'),
(29, 'Steven', 'Spielberg', '1946-12-18'),
(30, 'Brian', 'De Palma', '1940-09-11');


INSERT INTO Movie (movie_id, title, release_year, duration, rating) VALUES
(1, 'John Wick', 2014, 101, 7.4),
(2, 'Hangover 2', 2011, 100, 6.5),
(3, 'Avengers: Endgame', 2019, 181, 8.4),
(4, 'Interstellar', 2014, 169, 8.6),
(5, 'The Dark Knight', 2008, 152, 9.0),
(6, 'Forrest Gump', 1994, 142, 8.8),
(7, 'Saving Private Ryan', 1998, 169, 8.6),
(8, 'The Pianist', 2002, 150, 8.5),
(9, 'Whiplash', 2014, 107, 8.5),
(10, 'Scarface', 1983, 170, 8.3);


INSERT INTO MovieGenre (movie_id, genre_id) VALUES
(1, 1),  -- John Wick, Action
(1, 4),  -- John Wick, Thriller
(2, 2),  -- Hangover 2, Comedy
(3, 1),  -- Avengers, Action
(3, 5),  -- Avengers, Sci-Fi
(4, 5),  -- Interstellar, Sci-Fi
(4, 8),  -- Interstellar, Adventure
(5, 1),  -- Dark Knight, Action
(5, 4),  -- Dark Knight, Thriller
(6, 3),  -- Forrest Gump, Drama
(6, 6),  -- Forrest Gump, Romance
(7, 1),  -- Saving Private Ryan, Action
(7, 3),  -- Saving Private Ryan, Drama
(8, 3),  -- The Pianist, Drama
(9, 3),  -- Whiplash, Drama
(10, 3), -- Scarface, Drama
(10, 1); -- Scarface, Action


-- John Wick
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(1, 1, 1),  -- Keanu Reeves, Actor
(1, 11, 1), -- Ian McShane, Actor
(1, 2, 2),  -- Chad Stahelski, Director
(1, 21, 2); -- David Leitch, Director

-- Hangover 2
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(2, 3, 1),  -- Bradley Cooper, Actor
(2, 12, 1), -- Justin Bartha, Actor
(2, 4, 2);  -- Todd Phillips, Director

-- Avengers: Endgame
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(3, 5, 1),  -- Robert Downey Jr., Actor
(3, 13, 1), -- Chris Evans, Actor
(3, 14, 1), -- Mark Ruffalo, Actor
(3, 6, 2),  -- Anthony Russo, Director
(3, 24, 2); -- Joe Russo, Director

-- Interstellar
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(4, 15, 1), -- Matthew McConaughey, Actor
(4, 25, 2); -- Christopher Nolan, Director

-- Dark Knight
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(5, 16, 1), -- Christian Bale, Actor
(5, 26, 2); -- Christopher Nolan, Director

-- Forrest Gump
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(6, 7, 1),  -- Tom Hanks, Actor
(6, 28, 2); -- Robert Zemeckis, Director

-- Saving Private Ryan
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(7, 17, 1), -- Gary Sinise, Actor
(7, 8, 2);  -- Steven Spielberg, Director

-- The Pianist
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(8, 9, 1),  -- Adrien Brody, Actor
(8, 18, 1), -- Thomas Kretschmann, Actor
(8, 27, 2); -- Roman Polanski, Director

-- Whiplash
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(9, 10, 1), -- J.K. Simmons, Actor
(9, 19, 1); -- Paul Reiser, Actor

-- Scarface
INSERT INTO MoviePerson (movie_id, person_id, role_id) VALUES
(10, 20, 1), -- Al Pacino, Actor
(10, 30, 2); -- Brian De Palma, Director