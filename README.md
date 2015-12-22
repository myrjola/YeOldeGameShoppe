# Ye Olde Game Shoppe

A game store, which can easily be deployed to Heroku.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).
Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and
[Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).
It's recommended to use a
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) with
Python.

```sh
$ pip install -r requirements.txt
$ createdb python_getting_started
$ heroku local:run python manage.py migrate
$ python manage.py collectstatic
$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master
$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)
