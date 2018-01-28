import decimal
from urllib import request
from collections import defaultdict
import gzip

from django.core.management.base import BaseCommand
from app.models import Genre, Movie


class Command(BaseCommand):
	help = 'Pulls data from IMDB https://datasets.imdbws.com/'

	def add_arguments(self, parser):
		parser.add_argument('--year', nargs='?', type=int)

	def handle(self, *args, **kwargs):
		year = kwargs['year']
		print(year)

		imdb_ids_in_db = set()
		for m in Movie.objects.exclude(imdb_id=None):
			imdb_ids_in_db.add(m.imdb_id)

		print('Loading Genres...')
		genres = Genre.objects.all()
		genres_map = dict()
		for g in genres:
			genres_map[g.name] = g

		print('Downloading ratings...')
		ratings_map = dict()
		num_votes_map = dict()
		response = request.urlopen('https://datasets.imdbws.com/title.ratings.tsv.gz')
		data = gzip.decompress(response.read())
		string = data.decode('utf-8')
		for i, line in enumerate(string.split('\n')):
			if i == 0: continue
			columns = line.split('\t')
			if len(columns) == 1: break  # skip last column

			imdb_id = columns[0]
			ratings_map[imdb_id] = decimal.Decimal(columns[1])
			num_votes_map[imdb_id] = int(columns[2])

		print('Downloading movies...')
		response = request.urlopen('https://datasets.imdbws.com/title.basics.tsv.gz')
		data = gzip.decompress(response.read())
		string = data.decode('utf-8')
		for line in string.split('\n'):
			columns = line.split('\t')
			if len(columns) == 1: break  # skip last column

			if columns[1] == 'movie' and (year is None or columns[5] == str(year)) and columns[0] not in imdb_ids_in_db:
				imdb_id = columns[0]
				title = columns[2]
				released_year = None if columns[5] == '\\N' else int(columns[5])
				runtime = None if columns[7] == '\\N' else int(columns[7])
				is_adult = columns[4] == '1'
				entry_genres = columns[8].split(',')

				m_rating = None if imdb_id not in ratings_map else ratings_map[imdb_id]
				m_num_votes = None if imdb_id not in num_votes_map else num_votes_map[imdb_id]
				m = Movie(title=title, released_year=released_year, runtime=runtime,
						  is_adult=is_adult, imdb_id=imdb_id, imdb_rating=m_rating,
						  imdb_num_votes=m_num_votes)
				m.save()

				if entry_genres != ['\\N'] and len(entry_genres) >= 1:
					m_genres = []
					for e in entry_genres:
						if e not in genres_map:
							genres_map[e] = Genre.objects.create(name=e)
						m_genres.append(genres_map[e])

					m.genres.set(m_genres)
					m.save()
