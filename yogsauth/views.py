from django.shortcuts import (render, get_object_or_404)
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.http import Http404


from .forms import (UserCreationObligatoryEmailForm,
                    EmailValidationAuthenticationForm)
from .models import EmailValidation
from .utils import send_activation_email_to_user


@login_required
def profile(request):
    """Profile page."""
    return render(request, 'profile.djhtml')


@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request):
    """Register user."""
    logout(request)
    registration_form = UserCreationObligatoryEmailForm(request.POST or None)
    if registration_form.is_valid():
        user = registration_form.save()
        send_activation_email_to_user(user, request)
        return validation_email_sent_redirect()

    return render(request, 'register.djhtml',
                  context={'registration_form': registration_form})


@csrf_protect
def activate(request, user_id, activation_key):
    """Activate user with link sent to email."""
    email_validation = get_object_or_404(EmailValidation,
                                         activation_key=activation_key)
    user = email_validation.user
    if not user.is_active:
        if timezone.now() < email_validation.key_expires:
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('login'))

        return HttpResponseRedirect(
            "%s?activation_token_expired=1" % reverse('send_activation_email'))

    raise Http404("Invalid validation URL.")


@sensitive_post_parameters()
@csrf_protect
@never_cache
def send_activation_email(request):
    """Sends an email with account activation link.

    Requires the user to be authenticated.
    """
    form = EmailValidationAuthenticationForm(request,
                                             data=request.POST or None)
    context = {'form': form}

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            email = form.cleaned_data["email"]
            if form.cleaned_data["email"]:
                # User wants to change his/her email address.
                user.email = email
                user.save()
            send_activation_email_to_user(user, request)
            return validation_email_sent_redirect()

    return render(request, 'send_activation_email.djhtml', context=context)


def validation_email_sent_redirect():
    """Redirect to login page when validation email has been sent."""
    return HttpResponseRedirect("%s?validation_email_sent=1" %
                                reverse('login'))
