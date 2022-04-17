from django.contrib import admin

from .models import *


class AwardAdmin(admin.ModelAdmin):
    def get_org_name(self, obj):
        return obj.Organization.OrgName

    get_org_name.short_description = "Organization"

    list_display = ("Name", "Year", "get_org_name")
    list_display_links = ("Name",)
    search_fields = ("Name", "get_org_name")
    list_per_page = 25


admin.site.register(Award, AwardAdmin)
