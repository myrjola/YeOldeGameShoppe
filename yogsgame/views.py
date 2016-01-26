from django.shortcuts import render
from .forms import GameForm

def add_game(request):
    form=GameForm(request.POST or None)
    context={
        "form": form
    }
    if form.is_valid():
        game = form.save(commit=False)
        game.developer=request.user.developer
        game.save()
    return render(request,"addgame.djhtml",context)
