from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import (Player, Developer)


class PlayerTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="user")
        user2 = get_user_model().objects.create(username="user2")
        Player.objects.create(user=user)
        Player.objects.create(gamertag="awesomegamer",
                              user=user2)

    def test_get_name_for_highscore(self):
        """We should use gamertag for high scores, but fallback to username."""
        with_gamertag = Player.objects.get(gamertag="awesomegamer")
        self.assertEqual(with_gamertag.get_name_for_high_score(),
                         "awesomegamer")

        without_gamertag = get_user_model().objects.get(username="user").player
        self.assertEqual(without_gamertag.get_name_for_high_score(), "user")

    def test_cascading_delete(self):
        """Deleting the User should get rid of the Player"""
        user = get_user_model().objects.get(username="user2")
        user.delete()
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(username="user2")
        with self.assertRaises(Player.DoesNotExist):
            Player.objects.get(gamertag="awesomegamer")


class DeveloperTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(username="user")
        Developer.objects.create(user=user)

    def test_cascading_delete(self):
        """Deleting the Developer shouldn't get rid of the user"""
        developer = get_user_model().objects.get(username="user").developer
        developer.delete()
        user = get_user_model().objects.get(username="user")
        self.assertFalse(hasattr(user, 'developer'))
