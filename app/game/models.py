from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
from studio.models import Studio


def get_default_arr() -> list:
    return []


class Game(models.Model):
    GameId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Title = models.CharField(max_length=255)
    LengthOfTime = models.IntegerField(null=True)
    Genre = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=8, decimal_places=2)
    Console = ArrayField(
        models.CharField(max_length=255),
        default=get_default_arr,
    )
    Description = models.TextField()
    Reviews = models.IntegerField(default=0)
    Studio = models.ForeignKey(Studio, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title

    def get_avg_reviews(self):
        if hasattr(self, "reviews"):
            return self.reviews.aggregate(models.Avg("Score"))
        else:
            return None
