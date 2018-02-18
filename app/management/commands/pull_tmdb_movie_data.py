import os
import requests

from django.core.management.base import BaseCommand
from django.db.models import Q
from app.models import Movie

API_URL_FORMAT = 'https://api.themoviedb.org/3/movie/%d?api_key=%s'


class Command(BaseCommand):
	help = 'Pulls MOVIE endpoint data from TMDB by searching 1 by 1 by tmdb_id.'

	def handle(self, *args, **kwargs):
		api_key = os.environ['TMDB_API_KEY']
		for movie in Movie.objects.filter(spoken_languages=None).exclude(Q(tmdb_id=None) | Q(tmdb_id=-1)):
			res = requests.get(API_URL_FORMAT % (movie.tmdb_id, api_key))
			if res.status_code != 200:
				print('Bad status %d on %s. skipping...' % (res.status_code, movie))
				continue

			result = res.json()
			print(result)
			if 'tagline' in result:
				movie.tagline = result['tagline']
			if 'status' in result:
				movie.status = result['status']
			if 'revenue' in result:
				movie.revenue = result['revenue']
			if 'spoken_languages' in result:
				movie.spoken_languages = ','.join([s['name'] for s in result['spoken_languages']])
			movie.save()
