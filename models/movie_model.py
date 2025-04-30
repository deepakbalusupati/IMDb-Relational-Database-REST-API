from database.db_connection import mysql
from utils.omdb import get_movie_poster
from flask import url_for

class MovieModel:
    @staticmethod
    def get_all_movies(page=1, per_page=10):
        offset = (page - 1) * per_page
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT m.*, GROUP_CONCAT(g.name) as genres
            FROM movies m
            LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
            LEFT JOIN genres g ON mg.genre_id = g.genre_id
            GROUP BY m.movie_id
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        movies = cursor.fetchall()
        cursor.close()
        
        for movie in movies:
            movie['genres'] = movie['genres'].split(',') if movie['genres'] else []
            movie['poster_url'] = get_movie_poster(movie['title'], movie['release_year']) or \
                url_for('static', filename='images/default_poster.jpg')
        return movies

    @staticmethod
    def get_top_rated_movies(limit=10):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT m.*, GROUP_CONCAT(g.name) as genres
            FROM movies m
            LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
            LEFT JOIN genres g ON mg.genre_id = g.genre_id
            WHERE m.rating IS NOT NULL
            GROUP BY m.movie_id
            ORDER BY m.rating DESC
            LIMIT %s
        """, (limit,))
        movies = cursor.fetchall()
        
        for movie in movies:
            movie['genres'] = movie['genres'].split(',') if movie['genres'] else []
            movie['poster_url'] = get_movie_poster(movie['title'], movie['release_year']) or \
                url_for('static', filename='images/default_poster.jpg')
        
        cursor.close()
        return movies

    @staticmethod
    def get_movie_by_id(movie_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT m.*, GROUP_CONCAT(g.name) as genres
            FROM movies m
            LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
            LEFT JOIN genres g ON mg.genre_id = g.genre_id
            WHERE m.movie_id = %s
            GROUP BY m.movie_id
        """, (movie_id,))
        movie = cursor.fetchone()
        
        if movie:
            movie['genres'] = movie['genres'].split(',') if movie['genres'] else []
            movie['poster_url'] = (
                get_movie_poster(movie['title'], movie['release_year']) or 
                url_for('static', filename='images/default_poster.jpg')
            )
            
            cursor.execute("""
                SELECT a.actor_id, a.name, a.birth_date, ma.role
                FROM movie_actors ma
                JOIN actors a ON ma.actor_id = a.actor_id
                WHERE ma.movie_id = %s
            """, (movie_id,))
            movie['actors'] = cursor.fetchall()
            
            cursor.execute("""
                SELECT r.review_id, r.rating, r.comment, r.created_at, u.username
                FROM reviews r
                JOIN users u ON r.user_id = u.user_id
                WHERE r.movie_id = %s
                ORDER BY r.created_at DESC
            """, (movie_id,))
            movie['reviews'] = cursor.fetchall()
        
        cursor.close()
        return movie