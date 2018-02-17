import random
from functools import reduce

from django.shortcuts import redirect, render
from django.http import JsonResponse
from app.models import Genre, Movie


INTERNATIONAL_KEY = 100
GENRES_MAP = {
    "Action / Adventure": set([1, 9]),
    "Animation": set([10]),
    "Biography": set([17]),
    "Comedy": set([4]),
    "Crime / Mystery": set([12, 13]),
    "Documentary": set([11]),
    "Drama": set([5]),
    "Family": set([18]),
    "Fantasy / Sci-Fi": set([6]),
    "History": set([2]),
    "Horror / Thriller": set([7, 8]),
    "International": set([INTERNATIONAL_KEY]),
    "Musical": set([16]),
    "Romance": set([14]),
    "Sport / Music": set([19, 20]),
    "Western": set([21])
}


def _get_random_movie_not_in(ids_to_exclude, genres_to_include=[], international=False):
    movies = Movie.objects.filter(
        is_adult=False, imdb_rating__gt=6, imdb_num_votes__gt=400,
        released_year__gt=2010)\
        .exclude(youtube_trailer_key=None)\
        .exclude(youtube_trailer_key='-1')\
        .exclude(poster_path=None)\
        .exclude(pk__in=ids_to_exclude)

    if len(genres_to_include) > 0:
        movies = movies.filter(genres__id__in=genres_to_include)

    if international:
        movies = movies.exclude(original_language='en')
    else:
        movies = movies.filter(original_language='en')

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


def _map_request_to_genres_and_international(request):
    ins = request.GET.getlist('g[]')
    if len(ins) == 0:
        return ([], False)

    # make a copy after modification, o.w. union.remove edits GENRE_MAP
    sets = map(GENRES_MAP.get, ins)
    union = set(reduce(lambda x, y: x.union(y), sets))

    international = INTERNATIONAL_KEY in union
    if international: union.remove(INTERNATIONAL_KEY)
    return (union, international)


def index(request):
    ids_to_exclude = _get_seen_from_session(request)
    movie = _get_random_movie_not_in(ids_to_exclude)  # genres are set to all.
    return redirect('/' + str(movie.id) + '/')


def random_json(request):
    (genres_to_include, international) = _map_request_to_genres_and_international(request)
    ids_to_exclude = _get_seen_from_session(request)

    movie = _get_random_movie_not_in(ids_to_exclude, genres_to_include, international)
    _add_to_session(request, movie)
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
