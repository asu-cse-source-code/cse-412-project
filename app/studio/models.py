from django.db import models


class Studio(models.Model):
    SName = models.CharField(max_length=255, primary_key=True)


def get_studio(studio_name: str) -> Studio:
    if Studio.objects.filter(SName=studio_name).exists():
        studio = Studio.objects.get(SName=studio_name)
    else:
        studio = Studio(SName=studio_name)
        studio.save()

    return studio
