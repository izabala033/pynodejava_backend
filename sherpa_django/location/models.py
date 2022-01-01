from django.db import models
from django.utils.translation import gettext_lazy as _


class SherpaUser(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'), null=True)

class Location(models.Model):
    name = models.ForeignKey(SherpaUser, null=True, on_delete=models.CASCADE)
    cp = models.PositiveIntegerField(null = True)
    city = models.CharField(max_length=100, verbose_name=_('name'), null=True)