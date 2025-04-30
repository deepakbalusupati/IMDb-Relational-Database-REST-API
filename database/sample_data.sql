USE imdb_db;

-- Disable foreign key checks temporarily
SET FOREIGN_KEY_CHECKS = 0;

-- Clear tables in correct order
TRUNCATE TABLE reviews;
TRUNCATE TABLE movie_actors;
TRUNCATE TABLE movie_genres;
TRUNCATE TABLE movies;
TRUNCATE TABLE genres;
TRUNCATE TABLE actors;
TRUNCATE TABLE users;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Insert fresh sample data
INSERT INTO genres (name) VALUES 
('Action'), ('Adventure'), ('Comedy'), ('Crime'), ('Drama'),
('Fantasy'), ('Horror'), ('Mystery'), ('Romance'), ('Sci-Fi'),
('Thriller'), ('Animation'), ('Documentary');

INSERT INTO actors (name, birth_date, bio) VALUES 
('Tom Hanks', '1956-07-09', 'Two-time Academy Award winner'),
('Meryl Streep', '1949-06-22', 'Most Academy Award nominations'),
('Leonardo DiCaprio', '1974-11-11', 'Oscar winner for The Revenant'),
('Scarlett Johansson', '1984-11-22', 'Highest-grossing box office star'),
('Robert Downey Jr.', '1965-04-04', 'Known for Iron Man');

INSERT INTO movies (title, release_year, rating, plot, duration_minutes) VALUES 
('The Shawshank Redemption', 1994, 9.3, 'Two imprisoned men bond over years', 142),
('The Godfather', 1972, 9.2, 'Crime dynasty succession', 175),
('The Dark Knight', 2008, 9.0, 'Batman vs Joker', 152),
('Pulp Fiction', 1994, 8.9, 'Interconnected crime stories', 154),
('Forrest Gump', 1994, 8.8, 'Life through historical events', 142);

INSERT INTO movie_genres (movie_id, genre_id) VALUES 
(1, 4), (1, 5), (2, 4), (2, 5), (3, 1), (3, 4), (3, 5),
(4, 4), (4, 5), (5, 3), (5, 5), (5, 9);

INSERT INTO movie_actors (movie_id, actor_id, role) VALUES 
(1, 1, 'Andy Dufresne'), (2, 3, 'Michael Corleone'),
(3, 5, 'Iron Man'), (4, 4, 'Mia Wallace'),
(5, 1, 'Forrest Gump');

INSERT INTO users (username, email, password_hash) VALUES 
('moviebuff', 'buff@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'),
('cinemalover', 'lover@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW');

INSERT INTO reviews (movie_id, user_id, rating, comment) VALUES 
(1, 1, 10, 'One of the greatest movies ever made!'),
(1, 2, 9, 'Timeless classic'), (2, 1, 10, 'Marlon Brando is unforgettable'),
(3, 2, 9, 'Heath Ledger''s Joker is legendary'),
(5, 1, 8, 'Tom Hanks at his best');