from django.contrib import admin

from .models import *


class ReviewAdmin(admin.ModelAdmin):
    def get_game_title(self, obj):
        return obj.Game.Title

    get_game_title.short_description = "Game"

    def get_user(self, obj):
        return obj.User.Name

    get_user.short_description = "User"

    list_display = ("get_game_title", "Score", "get_user")
    list_display_links = ("Score",)
    search_fields = ("get_game_title", "get_user")
    list_per_page = 25


admin.site.register(Review, ReviewAdmin)
