from django.db import models

from game.models import Game
from user.models import User


class Review(models.Model):
    Game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="reviews", null=True
    )
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", null=True
    )
    Comment = models.CharField(max_length=255, null=True)
    Score = models.IntegerField(null=True)
    # NumOfReviews = models.IntegerField(default=0)
