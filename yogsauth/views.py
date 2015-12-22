from django.shortcuts import render
from django.conf import settings

from social.apps.django_app.views import complete as social_complete
from social.backends.facebook import FacebookOAuth2


def login(request):
    return render(
        request,
        'login.djhtml',
        context={'facebook_app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY})


def facebook(request):
    complete = social_complete(request, FacebookOAuth2)
    print(complete)
    return render(
        request,
        'login.djhtml',
        context={'facebook_app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY})
