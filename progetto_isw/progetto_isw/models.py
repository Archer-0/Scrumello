import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=128, default='New Board')
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

    def absolute_url(self):
        return reverse('board', args=[str(self.id)])


class Column(models.Model):
    name = models.CharField(max_length=128, default='New Column')
    mother_board = models.ForeignKey(Board, null=True)

    def __unicode__(self):
        return self.name


class Card(models.Model):
    title = models.CharField(max_length=128, default='New Card')
    description = models.CharField(max_length=1024)
    expire_date = models.DateField(default=datetime.datetime.now)
    story_points = models.IntegerField()
    mother_column = models.ForeignKey(Column, null=True)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.title
