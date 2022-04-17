from django.contrib import admin

from .models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("OrgName",)
    list_display_links = ("OrgName",)
    search_fields = ("OrgName",)
    list_per_page = 25


admin.site.register(Organization, OrganizationAdmin)
