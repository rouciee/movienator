import random

from django.shortcuts import render
from app.models import Movie


def hours_and_minutes(runtime):
    if runtime is None:
        return (None, None)
    return (int(runtime / 60), runtime % 60)


def index(request):
    movies = Movie.objects.filter(
        is_adult=False, imdb_rating__gt=5, imdb_num_votes__gt=400, released_year__gt=2000)\
        .exclude(youtube_trailer_key=None)\
        .exclude(youtube_trailer_key="-1")\
        .exclude(poster_path=None)
    count = movies.count()

    if count == 0:
        movie = Movie.objects.first()
    else:
        i = random.randint(0, count - 1)
        movie = movies.all()[i]
    genre_string = ', '.join([g.name for g in movie.genres.all()])
    (hours, minutes) = hours_and_minutes(movie.runtime)

    print(count)
    print(movie)

    return render(request, 'index.html', {
        'title': movie.title,
        'overview': movie.overview,
        'year': movie.released_year,
        'rating': movie.imdb_rating,
        'hours': hours, 'minutes': minutes,
        'poster_path': movie.poster_path,
        'youtube_trailer_key': movie.youtube_trailer_key,
        'genres': genre_string
    })
