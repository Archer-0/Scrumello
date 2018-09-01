import unittest
from django.test import TestCase, RequestFactory

from django.urls import reverse

import datetime

from ..models import UserProfile, Board, Column, Card
from django.contrib.auth.models import User

from .. import views


class ViewsTests(TestCase):

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create(username='utente_di_prova_1',
                                    password='password_di_prova_1')

        user2 = User.objects.create(username='utente_di_prova_2',
                                    password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        colonna = Column.objects.create(name='colonna_di_prova',
                                        mother_board=board,
                                        n_cards=1)

        carta = Card.objects.create(title='carta_di_prova',
                                    description='descrizione_di_prova',
                                    expire_date=datetime.datetime(2018, 9, 1),
                                    story_points=5,
                                    mother_column=colonna,
                                    n_users=2)

        carta.users.add(user1)
        carta.users.add(user2)

    def test_board_views(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)
        request.user = utente

        response = views.board_view(request, board_id=1)

        self.assertEqual(response.status_code, 200)


# comando python per far partire i test di una singola classe: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse

# comando python per far partire i test di una singola funzione specifica: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse.nome_del_test

# comando python per far partire i soltanto i test di questo file: python manage.py test --pattern="test_views.py

# comando python per far partire tutti i test della cartella tests: python manage.py test