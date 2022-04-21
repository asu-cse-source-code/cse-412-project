from django.contrib import admin

from .models import *


class GameAdmin(admin.ModelAdmin):
    def get_studio(self, obj):
        return obj.Studio.SName

    get_studio.short_description = "studio"

    list_display = ("Title", "Genre", "Price", "get_studio")
    list_display_links = ("Title",)
    search_fields = ("Title", "Genre")
    list_per_page = 25


admin.site.register(Game, GameAdmin)
