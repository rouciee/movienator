# movienator

### How to run locally

Ensure you have a .env file.

`pipenv shell`

`pipenv install` (optional, for if there are new packages that have been added since last time you installed.)

`python manage.py migrate` (optional, for if there are new database migrations)

`python manage.py runserver`

### Notes

Youtube links are: `https://www.youtube.com/watch?v=<youtube_trailer_key>`

IMDB movies are: `http://www.imdb.com/title/<imdb_id>/`

### Troubleshooting

If you get a Locale UTF error when running the pipenv shell in a Mac, see: https://github.com/pypa/pipenv/issues/187
