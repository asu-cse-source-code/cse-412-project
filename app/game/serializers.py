from .models import Game

from award.serializers import AwardNameSerializer

from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    Studio = serializers.SerializerMethodField(read_only=True)
    Awards = serializers.SerializerMethodField(read_only=True)

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
            "Awards",
            "Studio",
        ]

    def get_Studio(self, obj):

        if hasattr(obj, "Studio"):
            studio = obj.Studio.SName
        else:
            studio = None

        return studio

    def get_Awards(self, obj):

        if hasattr(obj, "Awards"):
            awards = AwardNameSerializer(obj.Awards.all(), many=True).data
            awards = [award["Name"] for award in awards]
        else:
            awards = []

        return awards
