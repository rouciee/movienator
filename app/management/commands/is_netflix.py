from django.core.management.base import BaseCommand
from app.models import Movie

from bs4 import BeautifulSoup
import requests

URL = "https://www.finder.com/netflix-movies"

class Command(BaseCommand):
	help = 'Pulls data from ' + URL + ' to mark movies in Netflix'

	def handle(self, *args, **kwargs):
		response = requests.get(URL)

		soup = BeautifulSoup(response.text, 'html.parser')
		for row in soup.select('table tbody tr'):
			tds = row.select('td')
			title = tds[0].select('b')[0].text
			year = tds[1].text

			Movie.objects.filter(title=title, released_year=year).update(in_netflix=True)
