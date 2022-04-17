import json
from django.shortcuts import render
from django.contrib.auth import authenticate

from .serializers import UserSerializer
from .models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


@api_view(["GET"])
def get_users(request):
    status = 200
    try:
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        response = serializer.data
    except:
        status = 500
        response = {"Error": "No users"}

    return Response(data=response, content_type="text/json", status=status)


@api_view(["GET"])
def get_user(request, id):
    status = 200
    if User.objects.filter(id=id).exists():
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, many=False)
        response = serializer.data
    else:
        response = {"Error": "No user with that id exists"}
        status = 404

    return Response(data=response, content_type="text/json", status=status)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_users(request):
    try:
        status = 201
        body = json.loads(request.body)
        new_users = []

        for user_dict in body:
            if "username" not in user_dict.keys():
                user_dict["username"] = "".join(user_dict["Name"].split())
            if "password" not in user_dict.keys():
                user_dict["password"] = "password"

            # Create the user instance
            user = User.objects.create_user(
                user_dict["username"],
                user_dict["Name"],
                user_dict["Age"],
                user_dict["password"],
            )
            user.save()

            new_users.append(user)

        serializer = UserSerializer(new_users, many=True)
        response = serializer.data
    except Exception as e:
        print(e)
        status = 500
        response = {"Error": str(e)}
    finally:
        return Response(response, content_type="text/json", status=status)
