from django.utils import timezone
from django.db import models
from django.conf import settings


class EmailValidation(models.Model):
    class KeyExpiredException(Exception):
        """Raised when the activation key has expired."""
        pass

    class UserActiveException(Exception):
        """Raised when trying to activate an activated user."""
        pass

    class IncorrectTokenException(Exception):
        """Raised when the token doesn't match the activation key."""
        pass

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

    def activate_user_against_token(self, token):
        """Try to activate user against the provided token

        Also checks that the key hasn't expired."""
        user = self.user

        if self.user.is_active:
            raise self.UserActiveException()

        if timezone.now() > self.key_expires:
            raise self.KeyExpiredException()

        if self.activation_key != token:
            raise self.IncorrectTokenException()

        user.is_active = True
        user.save()


class Developer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    iban = models.fields.CharField(
        max_length=34,
        verbose_name="IBAN",
        help_text="Your sales proceedings will be paid here.")

    swift = models.fields.CharField(max_length=11,
                                    verbose_name="SWIFT or BIC code")


class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    gamertag = models.fields.CharField(
        max_length=32, unique=False, null=True, blank=True,
        help_text="Optional name to show in high-scores.")

    def get_name_for_high_score(self):
        return self.gamertag or self.user.username

    def is_gamertag_unique(self, gamertag):
        """Returns True if gamertag is not used by other players.

        Also returns True if the gamertag is empty."""
        if not gamertag:
            return True

        other_players = Player.objects.exclude(pk=self.pk)
        same_gamertag = other_players.filter(gamertag=gamertag)
        return not same_gamertag.exists()
