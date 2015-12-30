# Ye Olde Game Shoppe

A game store, which can easily be deployed to Heroku.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org). Make sure you install Python 3.5. Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup). It's recommended to use a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) with Python.

```sh
$ pip install -r requirements.txt
$ createdb yeoldegameshoppe
$ heroku local:run python manage.py migrate
$ heroku local:run python manage.py collectstatic
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

## Facebook login support

We use [Python Social Auth](http://python-social-auth.readthedocs.org/en/stable/backends/facebook.html?highlight=facebook) to implement Facebook login. You need to register a Facebook app at [Facebook App Creation](http://developers.facebook.com/setup/) and set the app variables to Heroku like this:

```sh
$ heroku config:set FACEBOOK_APP_ID=*your_facebook_app_id*
$ heroku config:set FACEBOOK_API_SECRET=*your_facebook_api_secret*
```

Remember to set the Site URL in the Facebook app settings to the URL of your Heroku deployment.
