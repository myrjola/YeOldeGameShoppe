from django.shortcuts import (render, get_object_or_404)
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.http import Http404


from .forms import (UserCreationObligatoryEmailForm,
                    EmailValidationAuthenticationForm,
                    UserForm, PlayerForm, DeveloperForm)
from .models import EmailValidation
from .utils import (send_activation_email_to_user,
                    get_activation_link_for_user_and_request)


@login_required
@csrf_protect
def profile(request):
    """Profile page."""
    user = request.user
    user_form = UserForm(request.POST or None, instance=user)
    if user_form.is_valid():
        user_form.save()

    player = None
    if hasattr(user, 'player'):
        player = user.player
    player_form = PlayerForm(request.POST or None,
                             instance=player)
    if player_form.is_valid():
        player = player_form.save(commit=False)
        player.user = user
        player.save()

    developer = None
    if hasattr(user, 'developer'):
        developer = user.developer
    developer_form = DeveloperForm(request.POST or None,
                                   instance=developer)
    if developer_form.is_valid():
        developer = developer_form.save(commit=False)
        developer.user = user
        developer.save()

    context = {'user_form': user_form,
               'player_form': player_form,
               'developer_form': developer_form}

    # Show the developer and player forms when asked for them
    for querydict in [request.GET, request.POST]:
        if 'activate_player_account' in querydict:
            context['activate_player_account'] = True
        if 'activate_developer_account' in querydict:
            context['activate_developer_account'] = True

    return render(request, 'profile.djhtml', context=context)


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
        return validation_email_sent_redirect(user, request)

    return render(request, 'register.djhtml',
                  context={'registration_form': registration_form})


@csrf_protect
def activate(request, user_id, activation_key):
    """Activate user with link sent to email."""
    user = get_object_or_404(get_user_model(), id=user_id)

    try:
        user.emailvalidation.activate_user_against_token(activation_key)
    except EmailValidation.KeyExpiredException:
        return HttpResponseRedirect(
            "%s?activation_token_expired=1" % reverse('send_activation_email'))
    except EmailValidation.UserActiveException:
        return HttpResponseRedirect(
            "%s?user_already_activated=1" % reverse('login'))
    except EmailValidation.IncorrectTokenException:
        raise Http404("Invalid activation token.")

    return HttpResponseRedirect(reverse('login'))


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
            return validation_email_sent_redirect(user, request)

    return render(request, 'send_activation_email.djhtml', context=context)


def validation_email_sent_redirect(user, request):
    """Redirect to login page when validation email has been sent."""
    url = "%s?validation_email_sent_to=%s" % (reverse('login'), user.email)

    # If we are using the console backend we want the email's contents to be
    # shown for the user.
    email_backend = settings.EMAIL_BACKEND
    if email_backend == 'django.core.mail.backends.console.EmailBackend':
        link = get_activation_link_for_user_and_request(user, request)
        url += "&debug_activation_email_contents=%s" % link

    return HttpResponseRedirect(url)
