from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
