from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreationObligatoryEmailForm(UserCreationForm):
    """This form requires the user to specify a valid Email"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def save(self, commit=True):
        user = super(UserCreationObligatoryEmailForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
