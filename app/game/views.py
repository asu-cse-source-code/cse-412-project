import json

from studio.models import get_studio
from award.models import get_award


from .serializers import GameSerializer
from .models import Game

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response


@api_view(["GET"])
def get_games(request):
    status = 200
    try:
        all_games = Game.objects.all()
        serializer = GameSerializer(all_games, many=True)
        response = serializer.data
    except:
        status = 500
        response = {"Error": "No games"}

    return Response(data=response, content_type="text/json", status=status)


@api_view(["GET"])
def get_game(request, id):
    status = 200
    if Game.objects.filter(GameId=id).exists():
        game = Game.objects.get(GameId=id)
        serializer = GameSerializer(game, many=False)
        response = serializer.data
    else:
        response = {"Error": "No game with that id exists"}
        status = 404

    return Response(data=response, content_type="text/json", status=status)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_game(request):
    try:
        status = 201
        body = json.loads(request.body)
        awards = get_awards(body)
        body.pop("Won", None)
        body["Studio"] = get_studio(body["Studio"])
        game = Game(**body)
        game.save()
        set_awards(game, awards)
        serializer = GameSerializer(game, many=False)
        response = serializer.data
    except Exception as e:
        print(e)
        status = 500
        response = {"Error": str(e)}
    finally:
        return Response(data=response, content_type="text/json", status=status)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_games(request):
    try:
        status = 201
        all_games = []
        body = json.loads(request.body)
        for game in body:
            awards = get_awards(game)
            game.pop("Won", None)
            game["Studio"] = get_studio(game["Studio"])
            new_game = Game(**game)
            new_game.save()
            set_awards(new_game, awards)
            all_games.append(new_game)
        serializer = GameSerializer(all_games, many=True)
        response = serializer.data
    except Exception as e:
        print(e)
        status = 500
        response = {"Error": str(e)}
    finally:
        return Response(data=response, content_type="text/json", status=status)


def get_awards(game: dict) -> list:
    awards = []
    if game["Won"]:
        awards = game["Won"]

    return awards


def set_awards(game: Game, awards: list):
    for award in awards:
        get_award(
            game=game, org=award["OrgName"], name=award["Name"], year=award["Year"]
        )
