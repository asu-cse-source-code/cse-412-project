from .models import Award

from rest_framework import serializers


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = [
            "Game",
            "Organization",
            "Name",
            "Year",
        ]


class AwardNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = [
            "Name",
        ]
