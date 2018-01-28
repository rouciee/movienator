from django.db import models


class Genre(models.Model):
	name = models.CharField(max_length=256)


class Movie(models.Model):
	title = models.CharField(max_length=256)
	released_year = models.IntegerField(null=True)
	runtime = models.IntegerField(null=True)
	is_adult = models.BooleanField(default=True)

	imdb_id = models.CharField(max_length=256)
	imdb_rating = models.DecimalField(null=True, max_digits=3, decimal_places=1)
	imdb_num_votes = models.IntegerField(null=True)

	genres = models.ManyToManyField(Genre)

	def __str__(self):
		return str(self.__dict__)
