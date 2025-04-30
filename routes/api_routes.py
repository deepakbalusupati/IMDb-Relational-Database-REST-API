from flask_restful import Api
from controllers.movie_controller import (
    Movies, Movie, MovieActors, TopRatedMovies, MovieReviews, Actors, Actor
)
from controllers.user_controller import Users, User, UserLogin

def initialize_routes(api):
    # Movie routes
    api.add_resource(Movies, '/api/movies')
    api.add_resource(Movie, '/api/movies/<int:movie_id>')
    api.add_resource(MovieActors, '/api/movies/<int:movie_id>/actors', 
                    '/api/movies/<int:movie_id>/actors/<int:actor_id>')
    api.add_resource(TopRatedMovies, '/api/movies/top-rated')
    api.add_resource(MovieReviews, '/api/movies/<int:movie_id>/reviews')
    
    # Actor routes
    api.add_resource(Actors, '/api/actors')
    api.add_resource(Actor, '/api/actors/<int:actor_id>')
    
    # User routes
    api.add_resource(Users, '/api/users')
    api.add_resource(User, '/api/users/<int:user_id>')
    api.add_resource(UserLogin, '/api/login')