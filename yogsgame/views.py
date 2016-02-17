import time
from hashlib import md5

from django.conf import settings
from django.shortcuts import (render, get_object_or_404)
from django.http import (HttpResponse, HttpResponseBadRequest, JsonResponse)
from django.views.decorators.csrf import csrf_protect

from yeoldegameshoppe.utils import get_host_url
from yogsauth.decorators import player_required,developer_required
from django.views.decorators.csrf import csrf_protect


from .models import Game, GameLicense, HighScore
from .forms import GameForm


@player_required
def game(request, game_id):
    """The main view for the Game model.

    A player can buy the game and play it from this view."""
    user = request.user
    game = get_object_or_404(Game, id=game_id)
    #if the user had already got the game_id
    # if game.get_gamelicense_for_user(user):
    #     return render(request, 'game.djhtml', context=None)

    pid = str(game.id) + "a" + str(int(time.time())) + "a" +user.username
    amount = game.price
    sid = settings.PAYMENT_SELLER_ID
    secret_key = settings.PAYMENT_SECRET_KEY

    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    checksum = md5(checksumstr.encode('ascii')).hexdigest()

    context = {
        'pid' : pid,
        'sid' : sid,
        'amount' : amount,
        'checksum' : checksum,
        'game' : game,
        'user_owns_game': game.get_gamelicense_for_user(user),
        'host_url':get_host_url(request),
        'game_hostname': game.get_game_hostname(request),
        'checksumstr' : checksumstr
    }

    return render(request, 'game.djhtml', context=context)


@player_required
@csrf_protect
def submit_highscore(request, game_id):
    """Submit highscores through this view."""
    game = get_object_or_404(Game, pk=game_id)

    player = request.user.player

    if request.POST:
        score = request.POST.get('score')
        if score:
            HighScore(game=game, player=player, score=score).save()
            return HttpResponse('')

    return HttpResponseBadRequest()


def top10(request, game_id):
    """Returns top 10 high scores for a game as JSON."""
    top10 = HighScore.objects.filter(game_id=game_id).order_by('-score')[:10]

    top10_formatted = [
        {
            'name': highscore.player.get_name_for_high_score(),
            'score': highscore.score
        }
        for highscore in top10.all()
    ]

    return JsonResponse(top10_formatted, safe=False)


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

<<<<<<< HEAD
@developer_required
@csrf_protect
=======

>>>>>>> 524758d3947380b0324861c0b6aa2fd2d9685672
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
