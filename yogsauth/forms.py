from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.models import ModelForm

from .models import Player, Developer


class UserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email']


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['gamertag']


class DeveloperForm(ModelForm):
    # The SWIFT-BIC code is between 8 and 11 characters
    swift_length = Developer._meta.get_field('swift').max_length
    swift = forms.fields.CharField(min_length=8, max_length=swift_length)

    class Meta:
        model = Developer
        fields = ['iban', 'swift']


class UserCreationObligatoryEmailForm(UserCreationForm):
    """This form requires the user to specify a valid Email"""
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2", "email")

    def save(self):
        user = super(UserCreationObligatoryEmailForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        # User needs to validate email address before activation
        user.is_active = False
        user.save()

        return user


class EmailValidationAuthenticationForm(AuthenticationForm):
    """Form used for authenticating validation email sending.

    Allows authentication of inactive users."""

    email = forms.EmailField(label="Change your email address (optional):",
                             required=False)

    def confirm_login_allowed(self, user):
        """The user should not be activated at this point."""
        if user.is_active:
            raise forms.ValidationError("User is already activated.",
                                        code='user_is_activated')
