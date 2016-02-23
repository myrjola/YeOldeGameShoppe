from django.contrib.auth import get_user_model

from yeoldegameshoppe.tests import YogsSeleniumTest

from yogsgame.models import Game


class BasicPlayerFunctionalityTestCase(YogsSeleniumTest):
    """Tests the payment functionality in browser."""
    fixtures = ['0001_example_game.json']

    def test_buying_game(self):
        """Logs in with a player and buys a game."""
        self.login_user("player", "player")

        game = Game.objects.all().first()
        self.selenium.get('%s/game/%d' % (self.live_server_url, game.pk))

        self.selenium.find_element_by_xpath('//button[text()="Buy"]').click()
        self.selenium.find_element_by_xpath('//button[text()="Cancel"]').click(
        )

        # The first payment was cancelled
        player_user = get_user_model().objects.get(username="player")
        self.assertFalse(game.get_gamelicense_for_user(player_user))

        self.selenium.find_element_by_xpath('//button[text()="Buy"]').click()
        self.selenium.find_element_by_xpath('//button[text()="Pay"]').click()

        # The second payment should have passed
        self.assertTrue(game.get_gamelicense_for_user(player_user))
        game_iframe = self.selenium.find_element_by_name("game_iframe")
        self.assertTrue(game_iframe)
