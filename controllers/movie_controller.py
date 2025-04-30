from flask_restful import Resource, reqparse
from flask import jsonify, request
from models.movie_model import MovieModel
from models.actor_model import ActorModel

class Movies(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=10)
        parser.add_argument('search', type=str)
        args = parser.parse_args()
        
        if args['search']:
            movies = MovieModel.search_movies(args['search'], args['page'], args['per_page'])
        else:
            movies = MovieModel.get_all_movies(args['page'], args['per_page'])
        
        return jsonify({'movies': movies, 'page': args['page'], 'per_page': args['per_page']})

    def post(self):
        data = request.get_json()
        
        required_fields = ['title', 'release_year', 'rating', 'plot', 'duration_minutes']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400
        
        movie_id = MovieModel.add_movie(data)
        return {'message': 'Movie added successfully', 'movie_id': movie_id}, 201

class Movie(Resource):
    def get(self, movie_id):
        movie = MovieModel.get_movie_by_id(movie_id)
        if movie:
            return jsonify(movie)
        return {'message': 'Movie not found'}, 404

    def put(self, movie_id):
        data = request.get_json()
        if MovieModel.update_movie(movie_id, data):
            return {'message': 'Movie updated successfully'}, 200
        return {'message': 'Movie not found'}, 404

    def delete(self, movie_id):
        if MovieModel.delete_movie(movie_id):
            return {'message': 'Movie deleted successfully'}, 200
        return {'message': 'Movie not found'}, 404

class MovieActors(Resource):
    def post(self, movie_id):
        data = request.get_json()
        
        if 'actor_id' not in data or 'role' not in data:
            return {'message': 'Missing actor_id or role'}, 400
        
        cursor = MovieModel.mysql.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO movie_actors (movie_id, actor_id, role)
                VALUES (%s, %s, %s)
            """, (movie_id, data['actor_id'], data['role']))
            MovieModel.mysql.connection.commit()
            return {'message': 'Actor added to movie successfully'}, 201
        except Exception as e:
            MovieModel.mysql.connection.rollback()
            return {'message': str(e)}, 400
        finally:
            cursor.close()

    def delete(self, movie_id, actor_id):
        cursor = MovieModel.mysql.connection.cursor()
        cursor.execute("""
            DELETE FROM movie_actors 
            WHERE movie_id = %s AND actor_id = %s
        """, (movie_id, actor_id))
        MovieModel.mysql.connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        
        if affected_rows > 0:
            return {'message': 'Actor removed from movie successfully'}, 200
        return {'message': 'Actor not found in movie'}, 404

class TopRatedMovies(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, default=10)
        args = parser.parse_args()
        
        movies = MovieModel.get_top_rated_movies(args['limit'])
        return jsonify({'movies': movies})

class MovieReviews(Resource):
    def get(self, movie_id):
        movie = MovieModel.get_movie_by_id(movie_id)
        if not movie:
            return {'message': 'Movie not found'}, 404
        
        return jsonify({'reviews': movie['reviews']})

    def post(self, movie_id):
        data = request.get_json()
        
        if 'user_id' not in data or 'rating' not in data:
            return {'message': 'Missing user_id or rating'}, 400
        
        cursor = MovieModel.mysql.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO reviews (movie_id, user_id, rating, comment)
                VALUES (%s, %s, %s, %s)
            """, (movie_id, data['user_id'], data['rating'], data.get('comment', '')))
            MovieModel.mysql.connection.commit()
            return {'message': 'Review added successfully'}, 201
        except Exception as e:
            MovieModel.mysql.connection.rollback()
            return {'message': str(e)}, 400
        finally:
            cursor.close()

class Actors(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=10)
        parser.add_argument('search', type=str)
        args = parser.parse_args()
        
        if args['search']:
            actors = ActorModel.search_actors(args['search'], args['page'], args['per_page'])
        else:
            actors = ActorModel.get_all_actors(args['page'], args['per_page'])
        
        return jsonify({'actors': actors, 'page': args['page'], 'per_page': args['per_page']})

    def post(self):
        data = request.get_json()
        
        required_fields = ['name']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400
        
        actor_id = ActorModel.add_actor(data)
        return {'message': 'Actor added successfully', 'actor_id': actor_id}, 201

class Actor(Resource):
    def get(self, actor_id):
        actor = ActorModel.get_actor_by_id(actor_id)
        if actor:
            return jsonify(actor)
        return {'message': 'Actor not found'}, 404

    def put(self, actor_id):
        data = request.get_json()
        if ActorModel.update_actor(actor_id, data):
            return {'message': 'Actor updated successfully'}, 200
        return {'message': 'Actor not found'}, 404

    def delete(self, actor_id):
        if ActorModel.delete_actor(actor_id):
            return {'message': 'Actor deleted successfully'}, 200
        return {'message': 'Actor not found'}, 404