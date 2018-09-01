import unittest
from django.test import TestCase

from ..models import UserProfile, Board, Column, Card
from django.contrib.auth.models import User


class UserTests(TestCase):

    def setUp(self):
        User.objects.create(username='utente_di_prova', password='password_di_prova')

    def test_username(self):
        """
            Test per verificare che l'utente abbia un nome corretto
        """
        utente = User.objects.get(username="utente_di_prova")

        self.assertEqual(utente.username, 'utente_di_prova')

    def test_password(self):
        """
            Test per verificare che l'utente abbia una password corretto
        """
        utente = User.objects.get(password="password_di_prova")

        self.assertEqual(utente.password, 'password_di_prova')


class BoardTests(TestCase):

    def setUp(self):
        board = Board.objects.create(name='board_di_prova', n_users=2, n_columns=1, n_cards=1)

        user1 = User.objects.create(username='utente_di_prova_1', password='password_di_prova_1')
        user2 = User.objects.create(username='utente_di_prova_2', password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

    def test_board_name(self):
        """
            Test per verificare che la board abbia un nome corretto
        """

        board = Board.objects.get(name="board_di_prova")

        self.assertEqual(board.name, 'board_di_prova')

    def test_board_users(self):
        """
            Test per verificare che la board abbia colegati gli utenti corretti
        """
        user1 = User.objects.get(username='utente_di_prova_1')
        user2 = User.objects.get(username='utente_di_prova_2')

        board = Board.objects.get(name='board_di_prova')

        userlist = [user1, user2]  # aggiunge i due utenti ad una lista

        boarduserlist = list(board.users.all())  # aggiunge gli utenti associati alla board ad una lista

        self.assertEqual(boarduserlist, userlist)  # confronta le due liste

    def test_board_n_users(self):
        """
            Test per verificare che la board abbia un numero di utenti corretto
        """

        board = Board.objects.get(name='board_di_prova')

        self.assertEqual(board.n_users, 2)

    def test_board_n_columns(self):
        """
            Test per verificare che la board abbia un numero di colonne corretto
        """

        board = Board.objects.get(name='board_di_prova')

        self.assertEqual(board.n_columns, 1)

    def test_board_n_cards(self):
        """
            Test per verificare che la board abbia un numero di carte corretto
        """

        board = Board.objects.get(name='board_di_prova')

        self.assertEqual(board.n_cards, 1)

    def test_board_method__unicode__(self):
        """
            Test per verificare che il metodo __unicode__() della board restituisca il parametro corretto
        """

        board = Board.objects.get(name='board_di_prova')

        self.assertEqual(board.__unicode__(), 'board_di_prova')

    def test_board_method_absolute_url(self):
        """
            Test per verificare che il metodo absolute_url() della board restituisca il parametro corretto
        """

        board = Board.objects.get(name='board_di_prova')

        self.assertEqual(board.absolute_url(), '/board/1/')


class ColumnTests(TestCase):

    def setUp(self):
        board = Board.objects.create(name='board_di_prova', n_users=2, n_columns=1, n_cards=1)

        user1 = User.objects.create(username='utente_di_prova_1', password='password_di_prova_1')
        user2 = User.objects.create(username='utente_di_prova_2', password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        Column.objects.create(name='colonna_di_prova', mother_board=board, n_cards=1)

    def test_column_name(self):
        """
            Test per verificare che la colonna abbia un nome corretto
        """

        colonna = Column.objects.get(name="colonna_di_prova")

        self.assertEqual(colonna.name, 'colonna_di_prova')

    def test_column_mother_board(self):
        """
            Test per verificare che la colonna sia associata alla board corretta
        """

        board = Board.objects.get(name='board_di_prova')

        colonna = Column.objects.get(name='colonna_di_prova')

        self.assertEqual(colonna.mother_board, board)

    def test_column_n_cards(self):
        """
            Test per verificare che la colonna abbia un numero di carte corretto
        """

        colonna = Column.objects.get(name='colonna_di_prova')

        self.assertEqual(colonna.n_cards, 1)

    def test_column_method__unicode__(self):
        """
            Test per verificare che il metodo __unicode__() della colonna restituisca il parametro corretto
        """

        colonna = Column.objects.get(name='colonna_di_prova')

        self.assertEqual(colonna.__unicode__(), 'colonna_di_prova')


class CardTests(TestCase):

    def setUp(self):
        pass

    def test_(self):
        pass


# comando python per far partire i test di una singola classe: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse

# comando python per far partire i test di una singola funzione specifica: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse.nome_del_test

# comando python per far partire i soltanto i test di questo file: python manage.py test --pattern="test_models.py

# comando python per far partire tutti i test della cartella tests: python manage.py test
