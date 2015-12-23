from django.db import models
from django.conf import settings


class EmailValidation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=24)
    key_expires = models.DateTimeField()


class Developer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)


class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    gamertag = models.fields.CharField(max_length=32,
                                       unique=True)

    def get_name_for_high_score(self):
        return self.gamertag or self.user.username
