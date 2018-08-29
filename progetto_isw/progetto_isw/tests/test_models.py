import unittest
from django.test import TestCase

from ..models import UserProfile, Board, Column, Card
from django.contrib.auth.models import User


class UserTests(TestCase):

    def setUp(self):
        pass

    def test_(self):
        pass


class BoardTests(TestCase):

    def setUp(self):
        Board.objects.create(name='board_di_prova', n_users='1', n_columns='1', n_cards='1')

    def test_board_name(self):
        """
            Test per verificare che la board abbia un nome corretto
        """

        board = Board.objects.get(name="board_di_prova")

        self.assertEqual(board.name, 'board_di_prova')


class ColumnTests(TestCase):

    def setUp(self):
        pass

    def test_(self):
        pass


class CardTests(TestCase):

    def setUp(self):
        pass

    def test_(self):
        pass


# comando python per far partire i test di una singola classe: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse

# comando python per far partire i test di una singola funzione specifica: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse.nome_del_test

# comando python per far partire i soltanto i test di questo file: python manage.py test --pattern="test_models.py

# comando python per far partire tutti i test della cartella tests: python manage.py test
