from .models import Review

from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "Game",
            "User",
            "Comment",
            "Score",
        ]
