import random

from django.shortcuts import redirect, render
from django.http import JsonResponse
from app.models import Movie


def _get_random_movie_not_in(ids_to_exclude):
    movies = Movie.objects.filter(
        is_adult=False, imdb_rating__gt=6, imdb_num_votes__gt=400, released_year__gt=2000)\
        .exclude(youtube_trailer_key=None)\
        .exclude(youtube_trailer_key="-1")\
        .exclude(poster_path=None)\
        .exclude(pk__in=ids_to_exclude)
    count = movies.count()

    if count == 0:
        movie = Movie.objects.first()
    else:
        i = random.randint(0, count - 1)
        movie = movies.all()[i]

    print(count)
    print(movie)
    return movie


def _add_to_session(request, movie):
    request.session.set_expiry(0)  # erase when user closes browser.
    if 'seen' in request.session:
        request.session['seen'] = request.session['seen'] + [movie.id]
    else:
        request.session['seen'] = [movie.id]


def _get_seen_from_session(request):
    if 'seen' in request.session:
        return request.session['seen']
    else:
        return []


def index(request):
    ids_to_exclude = _get_seen_from_session(request)
    movie = _get_random_movie_not_in(ids_to_exclude)
    return redirect('/' + str(movie.id) + '/')


def random_json(request):
    ids_to_exclude = _get_seen_from_session(request)
    movie = _get_random_movie_not_in(ids_to_exclude)
    return JsonResponse({
        'id': movie.id,
        'title': movie.title,
        'year': movie.released_year,
        'genres': ', '.join([g.name for g in movie.genres.all()]),
        'youtube_url': "https://www.youtube.com/embed/" + movie.youtube_trailer_key,
        'poster_path': "https://image.tmdb.org/t/p/original" + movie.poster_path
    })

def _hours_and_minutes(runtime):
    if runtime is None:
        return (None, None)
    return (int(runtime / 60), runtime % 60)


def movie(request, pk):
    movie = Movie.objects.get(pk=pk)
    _add_to_session(request, movie)

    genre_string = ', '.join([g.name for g in movie.genres.all()])
    (hours, minutes) = _hours_and_minutes(movie.runtime)
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
