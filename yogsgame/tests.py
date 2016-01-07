from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Game, NotAPlayerException


class GameTestCase(TestCase):
    fixtures = ['0001_example_game.json']

    def test_gamelicense_ownership_player(self):
        """A Player should be able to own a game."""
        player_user = get_user_model().objects.get(username="player")
        game = Game.objects.all().first()

        self.assertFalse(game.get_gamelicense_for_user(player_user))

        game.buy_with_user(player_user)

        self.assertTrue(game.get_gamelicense_for_user(player_user))

    def test_gamelicense_ownership_developer(self):
        """A Developer should not be able to own a game."""
        developer_user = get_user_model().objects.get(username="developer")
        game = Game.objects.all().first()

        self.assertFalse(game.get_gamelicense_for_user(developer_user))

        with self.assertRaises(NotAPlayerException):
            game.buy_with_user(developer_user)

        self.assertFalse(game.get_gamelicense_for_user(developer_user))
