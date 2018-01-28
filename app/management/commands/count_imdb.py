from urllib import request
from collections import defaultdict
import gzip

from django.core.management.base import BaseCommand
from app.models import Movie


class Command(BaseCommand):
	help = 'Pulls data from IMDB https://datasets.imdbws.com/'

	def add_arguments(self, parser):
		parser.add_argument('--year', nargs='?', type=int)

	def handle(self, *args, **kwargs):
		year = kwargs['year']

		print('Downloading movies...')
		response = request.urlopen('https://datasets.imdbws.com/title.basics.tsv.gz')
		data = gzip.decompress(response.read())
		string = data.decode('utf-8')

		total = 0
		for line in string.split('\n'):
			columns = line.split('\t')
			if len(columns) == 1: break  # skip last column

			if columns[1] == 'movie' and (year is None or columns[5] == str(year)):
				total += 1
		print(total)
