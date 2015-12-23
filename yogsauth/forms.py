import os
import binascii
import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import EmailValidation


class UserCreationObligatoryEmailForm(UserCreationForm):
    """This form requires the user to specify a valid Email"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def save(self, commit=True):
        user = super(UserCreationObligatoryEmailForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        # User needs to validate email address before activation
        user.is_active = False
        email_validation = EmailValidation()
        email_validation.user = user

        # Generate random email activation key
        token_length = email_validation.activation_key.max_length
        token = binascii.hexlify(os.urandom(token_length))
        email_validation.activation_key = token

        # Don't let validation keys be active too long
        email_validation.key_expires = (datetime.datetime.now() +
                                        datetime.timedelta(days=2))

        if commit:
            user.save()

        return user
