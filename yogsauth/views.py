import logging

from django.shortcuts import (render, get_object_or_404)
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


from .forms import (UserCreationObligatoryEmailForm,
                    AuthenticationFormAllowInactiveUsers)
from .models import EmailValidation


logger = logging.getLogger(__name__)


@login_required
def profile(request):
    """Profile page"""
    return render(request, 'profile.djhtml')


@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request):
    """Register user"""
    logout(request)
    registration_form = UserCreationObligatoryEmailForm(request.POST or None)
    if registration_form.is_valid():
        registration_form.save()
        return HttpResponseRedirect(reverse('profile'))

    return render(request, 'register.djhtml',
                  context={'registration_form': registration_form})


@csrf_protect
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


@sensitive_post_parameters()
@csrf_protect
@never_cache
def send_activation_email(request):
    """Sends an email with account activation link.

    Requires the user to be authenticated.
    """
    form = AuthenticationFormAllowInactiveUsers(request,
                                                data=request.POST or None)
    context = {'form': form}

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            activation_key = user.emailvalidation.activation_key
            activation_link = (request.get_host() +
                               reverse('activate',
                                       kwargs={
                                           'user_id': user.id,
                                           'activation_key': activation_key
                                       }))
            send_mail('Ye Olde Game Shoppe activation', activation_link,
                      'yeoldegameshoppe', [user.email], fail_silently=False)

    return render(request, 'send_activation_email.djhtml', context=context)
