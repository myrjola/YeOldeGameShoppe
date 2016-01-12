import os
import binascii
import datetime

from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from django.utils import timezone

from .models import EmailValidation


def generate_email_validation_token_for_user(user):
    """Create a token used for activating the user.

    Create the EmailValidation model for the user if it doesn't exist.
    """
    # User should not be activated when doing this
    assert not user.is_active

    if not hasattr(user, 'emailvalidation'):
        email_validation = EmailValidation()
        email_validation.user = user

    email_validation = user.emailvalidation

    # Generate random email activation key
    length = EmailValidation._meta.get_field('activation_key').max_length
    # A byte is converted to two hex digits, therefore the length needs to
    # be halved, so that the token will fit.
    token = binascii.hexlify(os.urandom(int(length / 2)))
    email_validation.activation_key = token

    # Don't let validation keys be active too long
    email_validation.key_expires = (timezone.now() +
                                    datetime.timedelta(days=2))

    email_validation.save()


def send_activation_email_to_user(user, request):
    """Send a link that will activate the user account."""
    generate_email_validation_token_for_user(user)
    activation_link = get_activation_link_for_user_and_request(user, request)
    send_mail('Ye Olde Game Shoppe activation', activation_link,
              'yeoldegameshoppe', [user.email], fail_silently=False)


def get_activation_link_for_user_and_request(user, request):
    """Returns the link that activates the user."""
    activation_key = user.emailvalidation.activation_key
    return "%s://%s%s" % ('https' if request.is_secure() else 'http',
                          request.get_host(),
                          reverse('activate',
                                  kwargs={
                                      'user_id': user.id,
                                      'activation_key': activation_key
                                  }))
