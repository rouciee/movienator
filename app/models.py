from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=256)


class Movie(models.Model):
    title = models.CharField(max_length=256)
    released_year = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)
    is_adult = models.BooleanField(default=True)
    overview = models.CharField(max_length=512, null=True)

    imdb_id = models.CharField(max_length=256)
    imdb_rating = models.DecimalField(null=True, max_digits=3, decimal_places=1)
    imdb_num_votes = models.IntegerField(null=True)

    tmdb_id = models.IntegerField(null=True)

    poster_path = models.CharField(max_length=256, null=True)
    youtube_trailer_key = models.CharField(max_length=256, null=True)

    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return str(self.__dict__)
