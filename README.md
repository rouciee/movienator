# movienator

### How to run locally

Ensure you have a .env file.

`pipenv shell`

`pipenv install` (optional, for if there are new packages that have been added since last time you installed.)

`python manage.py migrate` (optional, for if there are new database migrations)

`python manage.py runserver`

### How to deploy

Use:

```
./deploy.sh
```

If want to push data, keep db.sqlite dirty before running that command.

To avoid paying for a database as a service that can hold > 10,000 rows, we commit the database
as a SQLite file and use LSF to share it. Heroku does not provide LFS capabilities,
so to push to heroku we add a commit just before pushing that removes the contents from the
.gitattributes file and potentially updates the database file too. This is the way we
add new movies to the database without paying extra. We push the SQLite database. This will
work until we surpass the Heroku repo slug limit.

### Notes

Youtube links are: `https://www.youtube.com/watch?v=<youtube_trailer_key>`

IMDB movies are: `http://www.imdb.com/title/<imdb_id>/`

### Troubleshooting

If you get a Locale UTF error when running the pipenv shell in a Mac, see: https://github.com/pypa/pipenv/issues/187
