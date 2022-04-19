from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q

from game.serializers import GameSerializer
from game.models import Game
from review.serializers import ReviewSerializer
from review.models import Review
from user.serializers import UserSerializer
from user.models import User

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class Profile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profile.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")

        queryset = UserSerializer(request.user, many=False)
        return Response({"profile": queryset.data})

    def post(self, request):
        searched = request.POST["searched"]
        return HttpResponseRedirect(f"/?search={searched}")


class Home(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"

    def get(self, request):
        query = request.GET.get("search")
        console = request.GET.get("console")
        genre = request.GET.get("genre")
        search = False

        game = Game.objects.all()

        if query is not None:
            search = True
            lookups = Q(Title__icontains=query) | Q(Description__icontains=query)
            game = game.filter(lookups).distinct()
        if console is not None:
            lookups = Q(Console__icontains=console)
            game = game.filter(lookups).distinct()
        if genre is not None:
            lookups = Q(Genre__icontains=genre)
            game = game.filter(lookups).distinct()

        if console is None and query is None and genre is None:
            # Get the most recent 5
            queryset = GameSerializer(Game.objects.all(), many=True)
        else:
            queryset = GameSerializer(game, many=True)

        paginator = Paginator(queryset.data, 6)  # Show 6 per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return Response(
            {
                "games": page_obj,
                "search": search,
                "searched": query,
                "genre": genre,
                "console": console,
            }
        )

    def post(self, request):
        searched = request.POST["searched"]
        return HttpResponseRedirect(f"/?search={searched}")


class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "authenticate/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("profile")

        return Response()

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("index")
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There was an error logging in, try again..."))
            return redirect("login")


class Logout(APIView):
    def get(self, request):
        logout(request)
        messages.success(request, ("You were logged out!"))
        return redirect("index")


class Register(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "authenticate/register.html"

    def get(self, request):
        return Response()

    def post(self, request):
        username = request.POST["username"]
        age = request.POST["age"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        name = first_name + " " + last_name
        password = request.POST["password"]
        user = User.objects.create_user(
            username,
            name,
            age,
            password,
        )
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Your account was created successfully!"))
            # Redirect to a success page.
            return redirect("profile")
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There was an error logging in, try again..."))
            return redirect("login")


class Games(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "game.html"

    def get(self, request, id):
        try:
            if Game.objects.filter(GameId=id).exists():
                game = Game.objects.get(GameId=id)
                serializer = GameSerializer(game, many=False)
                favorited = False
                review = None
                owned = False
                avg_review = None
                if request.user.Favorites.filter(GameId=id).exists():
                    favorited = True
                if request.user.Owns.filter(GameId=id).exists():
                    owned = True
                if request.user and hasattr(request.user, "reviews"):
                    if request.user.reviews.filter(Game=game).exists():
                        review = ReviewSerializer(
                            request.user.reviews.get(Game=game), many=False
                        )
                if hasattr(game, "reviews"):
                    avg_review = game.get_avg_reviews()

                return Response(
                    {
                        "game": serializer.data,
                        "favorited": favorited,
                        "owned": owned,
                        "review": review,
                        "avg_review": avg_review,
                    }
                )
            else:
                print("Game doesn't exist")
                return Response({"game": None})
        except Exception as e:
            print(e)
            return redirect("error")

    def post(self, request, id):
        if "searched" in request.POST:
            searched = request.POST["searched"]
            return HttpResponseRedirect(f"/?search={searched}")

        game = Game.objects.get(GameId=id)
        user = request.user
        print(request.POST)
        if "fav" in request.POST:
            request.user.favorite_game(id)
            messages.success(request, ("Game has been favorited!"))
        elif "own" in request.POST:
            request.user.own_game(id)
            messages.success(request, ("Game has been added to your collection!"))
        else:
            comment = request.POST["comment"]
            score = int(request.POST["score"])
            if Review.objects.filter(Game=game, User=user).exists():
                # Update the user's review
                review = Review.objects.get(Game=game, User=user)
                setattr(review, "Comment", comment)
                setattr(review, "Score", score)
                review.save()
                messages.success(request, ("Your review was updated successfully!"))
            else:
                review = Review(Game=game, User=user, Comment=comment, Score=score)
                review.save()
                setattr(game, "Reviews", game.Reviews + 1)
                game.save()
                messages.success(request, ("Your review was created successfully!"))

        return HttpResponseRedirect(f"/game/{game.GameId}")


class NotFound(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "404.html"

    def get(self, request):
        return Response()

    def post(self, request):
        searched = request.POST["searched"]
        return HttpResponseRedirect(f"/?search={searched}")
