import os
import binascii
import datetime

from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import EmailValidation


class UserCreationObligatoryEmailForm(UserCreationForm):
    """This form requires the user to specify a valid Email"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def save(self):
        user = super(UserCreationObligatoryEmailForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        # User needs to validate email address before activation
        user.is_active = False
        user.save()
        email_validation = EmailValidation()
        email_validation.user = user

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

        return user


class AuthenticationFormAllowInactiveUsers(AuthenticationForm):
    """Allows authentication of inactive users."""
    def confirm_login_allowed(self, user):
        pass
