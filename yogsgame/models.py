from django.db import models


class Game(models.Model):
    """A model for the computer games in the service."""
    developer = models.ForeignKey('yogsauth.Developer',
                                  on_delete=models.CASCADE)

    title = models.fields.CharField(max_length=256, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField()


class GameLicense(models.Model):
    """A model representing a bought license to play a game."""
    game = models.ForeignKey('Game',
                             on_delete=models.CASCADE)
    player = models.ForeignKey('yogsauth.Player',
                               on_delete=models.CASCADE)

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    bought_at = models.DateTimeField(auto_now_add=True)


class HighScore(models.Model):
    """The high-scores are saved in this model."""
    game = models.ForeignKey('Game',
                             on_delete=models.CASCADE)
    player = models.ForeignKey('yogsauth.Player',
                               on_delete=models.CASCADE)

    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
