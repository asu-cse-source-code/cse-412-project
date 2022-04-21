from django.db import models
from organization.models import get_org
from organization.models import Organization
from game.models import Game


class Award(models.Model):
    Game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="Awards")
    Organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="reviews"
    )
    Name = models.CharField(max_length=255)
    Year = models.CharField(max_length=10)


def get_award(game: Game, org: str, name: str, year: str) -> Award:
    org = get_org(org)
    if Award.objects.filter(Organization=org, Name=name, Year=year, Game=game).exists():
        award = Award.objects.get(Organization=org, Name=name, Year=year, Game=game)
    else:
        award = Award(Organization=org, Name=name, Year=year, Game=game)
        award.save()

    return award
