import sys
from datetime import timedelta

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail

from selenium.webdriver.firefox.webdriver import WebDriver
from pyvirtualdisplay import Display

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


class AuthenticationTestCase(StaticLiveServerTestCase):
    """End to end authentication test."""
    @classmethod
    def setUpClass(cls):
        super(AuthenticationTestCase, cls).setUpClass()

        # start virtual display if on linux
        if sys.platform == "linux" or sys.platform == "linux2":
            cls.vdisplay = Display(visible=0, size=(1024, 768))
            cls.vdisplay.start()

        # start browser
        cls.selenium = WebDriver()
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

        if sys.platform == "linux" or sys.platform == "linux2":
            cls.vdisplay.stop()

        super(AuthenticationTestCase, cls).tearDownClass()

    def test_end_to_end_auth(self):
        """Registers a new user, activates the account and logs in."""

        # Register new user
        self.selenium.get('%s%s' % (self.live_server_url, '/register'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('testuser')
        password_input = self.selenium.find_element_by_name("password1")
        password_input.send_keys('secret')
        password_input = self.selenium.find_element_by_name("password2")
        password_input.send_keys('secret')
        email_input = self.selenium.find_element_by_name("email")
        email_input.send_keys('test@example.com')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # Check the inbox
        self.assertEqual(len(mail.outbox), 1)
        activation_mail = mail.outbox[0]
        self.assertEqual(activation_mail.to, ['test@example.com'])
        activation_link = activation_mail.body

        # Activate user and login
        self.selenium.get(activation_link)
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('testuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

        # We should have logged in and be inside the profile now.
        self.assertIn('profile', self.selenium.current_url)
