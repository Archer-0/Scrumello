import datetime

from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=128)


class Column(models.Model):
    name = models.CharField(max_length=128)


class Card(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    expire_date = models.DateField(default=datetime.datetime.now)
    story_points = models.IntegerField()