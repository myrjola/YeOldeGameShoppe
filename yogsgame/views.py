import time
from hashlib import md5

from django.conf import settings
from django.shortcuts import (render, get_object_or_404)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from yeoldegameshoppe.utils import get_host_url
from yogsauth.decorators import player_required

from .models import Game, GameLicense


@player_required
def game(request, game_id):
    """The main view for the Game model.

    A player can buy the game and play it from this view."""
    user = request.user
    game = get_object_or_404(Game, id=game_id)
    pid = user.username + str(game.id) + str(int(time.time()))
    amount = game.price
    sid = settings.PAYMENT_SELLER_ID
    secret_key = settings.PAYMENT_SECRET_KEY
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid,
                                                            sid,
                                                            amount,
                                                            secret_key)
    checksum = md5(checksumstr.encode('ascii')).hexdigest()

    context = {
        'pid': pid,
        'sid': sid,
        'amount': amount,
        'checksum': checksum,
        'game': game,
        'user_owns_game': game.get_gamelicense_for_user(user),
        'host_url': get_host_url(request)
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


@player_required
def owned_games(request):
    """A view that shows all the owned games of a player."""
    player = request.user.player

    licenses = GameLicense.objects.filter(player=player)
    games = [license.game for license in licenses]

    context = {'games': games}

    return render(request, 'owned_games.djhtml', context=context)


def all_games(request):
    """A view that shows all games."""
    context = {"games": Game.objects.all()}
    return render(request, 'all_games.djhtml', context=context)
