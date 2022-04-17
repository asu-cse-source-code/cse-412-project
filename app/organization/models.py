from django.db import models


class Organization(models.Model):
    OrgName = models.CharField(max_length=255, primary_key=True)


def get_org(org_name: str) -> Organization:
    if Organization.objects.filter(OrgName=org_name).exists():
        org = Organization.objects.get(OrgName=org_name)
    else:
        org = Organization(OrgName=org_name)
        org.save()

    return org
