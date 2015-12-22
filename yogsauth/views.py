import logging

from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

logger = logging.getLogger(__name__)


def auth_logout(request):
    """Logout user"""
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def auth_login(request):
    """Login user"""

    redirect = ''
    if 'redirect' in request.POST:
        redirect = request.POST['redirect']
    elif 'redirect' in request.GET:
        redirect = request.GET['redirect']
    nextpage = redirect or reverse("profile")
    if request.user.is_authenticated():
        return HttpResponseRedirect(nextpage)

    context = {}

    if request.POST:

        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return HttpResponseRedirect(nextpage)
        context['invalid_credentials'] = True

    return render(request, 'login.djhtml', context=context)


def profile(request):
    """Profile page"""
    return render(request, 'profile.djhtml')
