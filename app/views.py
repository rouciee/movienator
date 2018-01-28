import random

from django.shortcuts import render
from app.models import Movie


def index(request):
    movies = Movie.objects.filter(is_adult=False, released_year__gt=2015,
                                  imdb_rating__gt=7, imdb_num_votes__gt=10000)

    count = movies.count()
    i = random.randint(0, count - 1)
    movie = movies.all()[i]
    print(movie)

    return render(request, 'index.html', {
        'year': movie.released_year,
        'rating': movie.imdb_rating, 'hours': '2', 'minutes': '32',
        'genres': 'Adventure, Family, Fantasy'})
