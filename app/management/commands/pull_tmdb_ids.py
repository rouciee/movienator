import os
import requests

from django.core.management.base import BaseCommand
from app.models import Movie

API_URL_FORMAT = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id'


class Command(BaseCommand):
	help = 'Pulls ids from TMDB by searching 1 by 1 by IMDB id.'

	def handle(self, *args, **kwargs):
		api_key = os.environ['TMDB_API_KEY']
		for movie in Movie.objects.filter(tmdb_id=None).exclude(imdb_id=None):
			res = requests.get(API_URL_FORMAT % (movie.imdb_id, api_key))
			movie_results = res.json()['movie_results']
			if len(movie_results) == 0:
				movie.tmdb_id = -1
			else:
				movie.tmdb_id = movie_results[0]['id']
			movie.save()