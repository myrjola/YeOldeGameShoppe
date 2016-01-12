from django.test import TestCase
from django.contrib.auth import get_user_model
from selenium.common.exceptions import NoSuchElementException

from yeoldegameshoppe.tests import YogsSeleniumTest

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


class BasicPlayerFunctionalityTestCase(YogsSeleniumTest):
    """Tests the basic player functionalities in browser."""
    fixtures = ['0001_example_game.json']

    def test_playing_game(self):
        """Logs in with a player and plays a game that the player owns."""
        self.login_user("player", "player")

        # Try playing the game without buying it
        game = Game.objects.all().first()
        self.selenium.get('%s/game/%d' % (self.live_server_url, game.pk))
        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_name("game_iframe")

        # First we need to buy the game
        player_user = get_user_model().objects.get(username="player")
        game.buy_with_user(player_user)

        # Start playing the game
        self.selenium.get('%s/game/%d' % (self.live_server_url, game.pk))
        game_iframe = self.selenium.find_element_by_name("game_iframe")
        self.assertTrue(game_iframe)
        self.selenium.switch_to.frame(game_iframe)

        # A simple test to see if clicking buttons works
        score = self.selenium.find_element_by_css_selector('#score')
        self.assertEqual("0", score.text)
        self.selenium.find_element_by_css_selector('#add_points').click()
        self.assertEqual("10", score.text)
