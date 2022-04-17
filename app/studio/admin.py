from django.contrib import admin

from .models import *


class StudioAdmin(admin.ModelAdmin):
    list_display = ("SName",)
    list_display_links = ("SName",)
    search_fields = ("SName",)
    list_per_page = 25


admin.site.register(Studio, StudioAdmin)
