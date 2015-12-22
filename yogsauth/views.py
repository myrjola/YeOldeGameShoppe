import logging

from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger(__name__)


def login(request):
    return render(
        request,
        'login.djhtml',
        context={'facebook_app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY})


def profile(request):
    return render(
        request,
        'profile.djhtml',
        context={'facebook_app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY})
