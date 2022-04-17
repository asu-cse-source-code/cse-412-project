from .models import Game

from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    Studio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Game
        fields = [
            "GameId",
            "Title",
            "LengthOfTime",
            "Genre",
            "Price",
            "Console",
            "Description",
            "Reviews",
            "Studio",
        ]

    def get_Studio(self, obj):

        if hasattr(obj, "Studio"):
            studio = obj.Studio.SName
        else:
            studio = None

        return studio
