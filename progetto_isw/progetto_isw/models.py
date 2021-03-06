import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class UserProfile(models.Model):                # l'intenzione c'era
    user = models.OneToOneField(User)
    model_pic = models.ImageField(upload_to='progetto_isw/progetto_isw/static/assets/users_profile_pics',
                                  default='progetto_isw/progetto_isw/static/assets/default_profile_pic')


class Board(models.Model):
    name = models.CharField(max_length=128, default='New Board')
    creator = models.ForeignKey(User, related_name='creator', null=True)
    owners = models.ManyToManyField(User, related_name='owner')
    users = models.ManyToManyField(User, related_name='users')
    n_users = models.IntegerField(default=1)
    n_columns = models.IntegerField(default=0)
    n_cards = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def absolute_url(self):
        return reverse('board', args=[str(self.id)])


class Column(models.Model):
    name = models.CharField(max_length=128, default='New Column')
    mother_board = models.ForeignKey(Board, null=True)
    n_cards = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Card(models.Model):
    title = models.CharField(max_length=128, default='New Card')
    description = models.CharField(max_length=1024)
    creation_date = models.DateField(default=datetime.datetime.now)
    expire_date = models.DateField(default=datetime.datetime.now)
    story_points = models.IntegerField()
    mother_column = models.ForeignKey(Column, null=True)
    n_users = models.IntegerField(default=1)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.title
