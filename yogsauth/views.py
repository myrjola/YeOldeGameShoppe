import os

from django.shortcuts import render
from django.conf import settings


def login(request):
    return render(
        request,
        'login.djhtml',
        context={'facebook_app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY})
