import requests
import os
from functools import lru_cache
from config.config import Config

@lru_cache(maxsize=100)
def get_movie_poster(title, year=None):
    if not Config.OMDB_API_KEY:
        return ""
    
    params = {
        't': title,
        'apikey': Config.OMDB_API_KEY,
        'type': 'movie'
    }
    if year:
        params['y'] = year
        
    try:
        response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
        return response.json().get('Poster', '')
    except:
        return ""