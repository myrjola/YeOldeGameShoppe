from django.db import models
from django.conf import settings


class Developer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)


class Player(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    gamertag = models.fields.CharField(max_length=32,
                                       unique=True)

    def get_name_for_high_score(self):
        return self.gamertag or self.user.username
