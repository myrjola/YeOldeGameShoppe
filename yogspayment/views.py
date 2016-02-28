from hashlib import md5
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from yogsauth.decorators import player_required
from yogsgame.models import Game, GameAlreadyOwnedException


@player_required
def success(request):
    get_checksum = request.GET.get('checksum', '')
    result = process(request)
    game = result[0]
    user = request.user
    get_checksum = result[2]
    calc_checksum = result[3]

    # verify the checksum
    if get_checksum != calc_checksum:
        return HttpResponseRedirect("%s?payment_error=1" %
                                    reverse("game",
                                            kwargs={"game_id": game.id}))

    try:
        game.buy_with_user(user)
    except GameAlreadyOwnedException:
        return HttpResponseRedirect("%s?already_bought=1" %
                                    reverse("game",
                                            kwargs={"game_id": game.id}))

    # Redirect back to game page to play the game
    return HttpResponseRedirect(reverse("game", kwargs={"game_id": game.id}))


@player_required
def cancel(request):
    get_checksum = request.GET.get('checksum', '')
    result = process(request)
    game = result[0]
    get_checksum = result[2]
    calc_checksum = result[3]

    # verify the checksum
    if get_checksum != calc_checksum:
        return render(request, 'game.djhtml', {"title": 'Payment Failed'})

    return HttpResponseRedirect("%s?payment_cancel=1" %
                                reverse("game",
                                        kwargs={"game_id": game.id}))


@player_required
def error(request):
    get_checksum = request.GET.get('checksum', '')
    result = process(request)
    game = result[0]
    get_checksum = result[2]
    calc_checksum = result[3]

    # verify the checksum
    if get_checksum != calc_checksum:
        return render(request, 'game.djhtml', {"title": 'Payment Failed'})
    return HttpResponseRedirect("%s?payment_error=1" %
                                reverse("game",
                                        kwargs={"game_id": game.id}))


def process(request):
    secret_key = getattr(settings, "PAYMENT_SECRET_KEY", None)
    pid = request.GET.get('pid', '')
    ref = request.GET.get('ref', '')
    result = request.GET.get('result', '')
    get_checksum = request.GET.get('checksum', '')
    getattr(settings, "PAYMENT_SECRET_KEY", None)
    splitpid = pid.split("a", 2)
    gameid = int(splitpid[0])
    game = get_object_or_404(Game, id=gameid)
    user = request.user

    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result,
                                                            secret_key)
    calc_checksum = md5(checksumstr.encode('ascii', 'ignore')).hexdigest()

    return [game, user, get_checksum, calc_checksum]
