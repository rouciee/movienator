import os
import requests

from django.core.management.base import BaseCommand
from django.db.models import Q
from app.models import Movie

API_URL_FORMAT = 'https://api.themoviedb.org/3/movie/%d/videos?api_key=%s'


class Command(BaseCommand):
	help = 'Pulls Youtube video keys from TMDB by searching 1 by 1 by TMDB id.'

	def handle(self, *args, **kwargs):
		api_key = os.environ['TMDB_API_KEY']
		for movie in Movie.objects.filter(youtube_trailer_key=None).exclude(Q(tmdb_id=None) | Q(tmdb_id=-1)):
			res = requests.get(API_URL_FORMAT % (movie.tmdb_id, api_key))
			if res.status_code != 200:
				print('Bad status %d on %s. skipping...' % (res.status_code, movie))
				continue

			print(res.json())
			movie.youtube_trailer_key = "-1"  # sentinel value for searched but couldn't find.
			for r in res.json()['results']:
				if r['site'] != 'YouTube':
					continue

				movie.youtube_trailer_key = r['key']
				break
			movie.save()
