from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import (Player, Developer, EmailValidation)
from .utils import generate_email_validation_token_for_user


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


class EmailValidationTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="user")
        self.user.is_active = False
        generate_email_validation_token_for_user(self.user)
        self.emailvalidation = self.user.emailvalidation

    def test_activation_against_active_user(self):
        """Validating an active user should not be possible."""
        self.user.is_active = True
        with self.assertRaises(EmailValidation.UserActiveException):
            self.emailvalidation.activate_user_against_token("wrong")

    def test_activation(self):
        """Activating an user should work provided the token is correct."""
        with self.assertRaises(EmailValidation.IncorrectTokenException):
            self.emailvalidation.activate_user_against_token("wrong")

        correct_token = self.emailvalidation.activation_key
        self.emailvalidation.activate_user_against_token(correct_token)
        self.assertTrue(self.user.is_active)

    def test_token_expiration(self):
        """The user can't be activated when the token has expired."""
        self.emailvalidation.key_expires = timezone.now()-timedelta(minutes=1)

        correct_token = self.emailvalidation.activation_key
        with self.assertRaises(EmailValidation.KeyExpiredException):
            self.emailvalidation.activate_user_against_token(correct_token)
