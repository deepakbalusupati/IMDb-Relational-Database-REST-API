from flask import Blueprint, render_template, request, redirect, url_for
from models.movie_model import MovieModel
from models.actor_model import ActorModel

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def home():
    movies = MovieModel.get_top_rated_movies(10)
    return render_template('index.html', movies=movies)

@web_bp.route('/movies')
def movies():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    movies = MovieModel.get_all_movies(page, per_page)
    return render_template('movies.html', movies=movies, page=page, per_page=per_page)

@web_bp.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    movie = MovieModel.get_movie_by_id(movie_id)
    if not movie:
        return render_template('404.html'), 404
    return render_template('movie_detail.html', movie=movie)

@web_bp.route('/actors')
def actors():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    actors = ActorModel.get_all_actors(page, per_page)
    return render_template('actors.html', actors=actors, page=page, per_page=per_page)

@web_bp.route('/actors/<int:actor_id>')
def actor_detail(actor_id):
    actor = ActorModel.get_actor_by_id(actor_id)
    if not actor:
        return render_template('404.html'), 404
    return render_template('actor_detail.html', actor=actor)

@web_bp.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('web.home'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    movies = MovieModel.search_movies(query, page, per_page)
    actors = ActorModel.search_actors(query, page, per_page)
    
    return render_template('search.html', 
                         movies=movies, 
                         actors=actors, 
                         query=query, 
                         page=page, 
                         per_page=per_page)