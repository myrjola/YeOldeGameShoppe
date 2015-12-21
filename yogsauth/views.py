import os

from django.shortcuts import render


def login(request):
    facebook_app_id = os.environ['FACEBOOK_APP_ID']
    return render(request, 'login.djhtml',
                  context={'facebook_app_id': facebook_app_id})
