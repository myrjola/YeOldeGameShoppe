from django import forms

from .models import Game
class GameForm(forms.ModelForm):
    # game_name = forms.CharField()
    # game_price = forms.CharField()
    class Meta:
        model = Game
        fields = ['title','price','url']
