from django.shortcuts import render
from .forms import GameForm

def add_game(request):
    form=GameForm(request.POST or None)
    context={
        "form": form
    }
    return render(request,"addgame.djhtml",context)
