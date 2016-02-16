from hashlib import md5
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from yogsauth.decorators import player_required
from yogsgame.models import Game

def success(request):
    get_checksum = request.GET.get('checksum', '')
    result = process(request)
    game = result[0]
    user = result[1]
    get_checksum = result[2]
    calc_checksum = result[3]

    #verify the checksum
    if get_checksum != calc_checksum:
        return render(request, 'game.djhtml', {"title":'Payment Failed'})

    # check if the url belongs to the user
    # if str(user) != str(buyer):
    #     text = "Wrong URL<br><a href=\"http://localhost:8000/game/\">Return to Homepage</a>"

    game.buy_with_user(user)

    # Redirect back to game page to play the game
    return HttpResponseRedirect(reverse("game", kwargs={"game_id": game.id}))

@player_required
def cancel(request):
    get_checksum = request.GET.get('checksum', '')
    result = process(request)
    game = result[0]
    user = result[1]
    get_checksum = result[2]
    calc_checksum = result[3]

    #verify the checksum
    if get_checksum != calc_checksum:
        return render(request, 'game.djhtml', {"title":'Payment Failed'})

    return HttpResponseRedirect("%s?payment_cancel=1" %reverse("game", kwargs={"game_id": game.id}))


@login_required
def error(request):
    get_checksum = request.GET.get('checksum', '')
    result = process(request)
    game = result[0]
    user = result[1]
    get_checksum = result[2]
    calc_checksum = result[3]

    #verify the checksum
    if get_checksum != calc_checksum:
        return render(request, 'game.djhtml', {"title":'Payment Failed'})
    return HttpResponseRedirect("%s?payment_error=1" %reverse("game", kwargs={"game_id": game.id}))


def process(request):
    secret_key = getattr(settings, "PAYMENT_SECRET_KEY", None)
    pid = request.GET.get('pid', '')
    ref = request.GET.get('ref', '')
    result = request.GET.get('result', '')
    get_checksum = request.GET.get('checksum', '')
    getattr(settings, "PAYMENT_SECRET_KEY", None)
    splitpid = pid.split("a", 2)
    gameid = int(splitpid[0])
    buyer = str(splitpid[2])
    game = get_object_or_404(Game, id=gameid)
    user = get_user_model().objects.get(username=buyer)

    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
    calc_checksum = md5(checksumstr.encode('ascii')).hexdigest()

    return [game, user, get_checksum, calc_checksum]
