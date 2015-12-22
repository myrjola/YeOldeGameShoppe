import logging

from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


logger = logging.getLogger(__name__)


def auth_login(request):
    """Login user"""

    context = {}

    if request.POST:
        redirect = ''
        if 'redirect' in request.POST:
            redirect = request.POST['redirect']
        nextpage = redirect or reverse("profile")

        if request.user.is_authenticated():
            return HttpResponseRedirect(nextpage)

        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return HttpResponseRedirect(nextpage)
        context['invalid_credentials'] = True

    return render(request, 'login.djhtml', context=context)


def profile(request):
    """Profile page"""
    return render(request, 'profile.djhtml')
