from game.serializers import GameSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    Owns = serializers.SerializerMethodField(read_only=True)
    Favorites = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "Name",
            "Age",
            "Owns",
            "is_admin",
            "Favorites",
        ]

    def get_Owns(self, obj):

        if hasattr(obj, "Owns"):
            owns = GameSerializer(obj.Owns.all(), many=True).data
        else:
            owns = []

        return owns

    def get_Favorites(self, obj):

        if hasattr(obj, "Favorites"):
            favorites = GameSerializer(obj.Favorites.all(), many=True).data
        else:
            favorites = []

        return favorites


# Creating custom field for creating Refresh access_token for registration Process
class UserSerializerWithToken(UserSerializer):
    Owns = serializers.SerializerMethodField(read_only=True)
    Favorites = serializers.SerializerMethodField(read_only=True)
    access_token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "Name",
            "Age",
            "Owns",
            "Favorites",
            "access_token",
        ]

    def get_access_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
