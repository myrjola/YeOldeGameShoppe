import logging

from django.shortcuts import render
from django.conf import settings

from social.apps.django_app.views import complete as social_complete
from social.backends.facebook import FacebookOAuth2

logger = logging.getLogger(__name__)


def login(request):
    return render(
        request,
        'login.djhtml',
        context={'facebook_app_id': settings.SOCIAL_AUTH_FACEBOOK_APP_KEY})
