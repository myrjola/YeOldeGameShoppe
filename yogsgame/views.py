from django.shortcuts import (render, get_object_or_404)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from yogsauth.decorators import player_required

from .models import Game


@player_required
def game(request, game_id):
    """The main view for the Game model.

    A player can buy the game and play it from this view."""
    game = get_object_or_404(Game, pk=game_id)
    user = request.user

    context = {
        'game': game,
        'user_owns_game': game.get_gamelicense_for_user(user)
    }

    return render(request, 'game.djhtml', context=context)


@player_required
def buy_game(request, game_id):
    """A view for buying a game."""
    game = get_object_or_404(Game, pk=game_id)

    # TODO validate payment here
    user = request.user
    game.buy_with_user(user)

    return HttpResponseRedirect(reverse("game", kwargs={"game_id": game_id}))
