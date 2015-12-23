import logging

from django.shortcuts import (render, get_object_or_404)
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import UserCreationObligatoryEmailForm
from .models import EmailValidation


logger = logging.getLogger(__name__)


def auth_logout(request):
    """Logout user"""
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def auth_login(request):
    """Login user"""

    next = ''
    for querydict in (request.POST, request.GET):
        if 'next' in querydict:
            next = querydict['next']
    nextpage = next or reverse("profile")
    print(nextpage)
    if request.user.is_authenticated():
        return HttpResponseRedirect(nextpage)

    auth_form = AuthenticationForm(request, data=request.POST or None)

    context = {"auth_form": auth_form}

    if auth_form.is_valid():
        login(request, auth_form.get_user())
        return HttpResponseRedirect(nextpage)

    return render(request, 'login.djhtml', context=context)


@login_required
def profile(request):
    """Profile page"""
    return render(request, 'profile.djhtml')


def register(request):
    """Register user"""
    logout(request)
    registration_form = UserCreationObligatoryEmailForm(request.POST or None)
    if registration_form.is_valid():
        registration_form.save()
        return HttpResponseRedirect(reverse('profile'))

    return render(request, 'register.djhtml',
                  context={'registration_form': registration_form})


def activate(request, user_id, activation_key):
    """Activate user with link sent to email"""
    email_validation = get_object_or_404(EmailValidation,
                                         activation_key=activation_key)
    user = email_validation.user
    if not user.is_active:
        if timezone.now() < email_validation.key_expires:
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('login'))
