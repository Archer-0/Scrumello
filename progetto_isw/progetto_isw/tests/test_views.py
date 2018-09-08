from django.test import TestCase, RequestFactory, Client

from django.urls import reverse

import datetime

from ..models import Board, Column, Card
from django.contrib.auth.models import User, AnonymousUser

from .. import views


class ViewsTestAbout(TestCase):
    """
        Test riguardanti l'about
    """

    def setUp(self):

        User.objects.create_user(username='utente_di_prova_1',
                                 password='password_di_prova_1')

    def test_about(self):

        utente = User.objects.get(username='utente_di_prova_1')  # utente prende un utente loggato

        path = reverse('about')  # path prende la URL corrispondente alla view indicata
        request = RequestFactory().get(path)  # request prende la request del path precedente

        request.user = utente  # la request viene eseguita dall'utente precedentemente specificato

        response = views.about(request)  # response prende la risposta che ha ricevuto il server all'esecuzione della view

        self.assertEqual(response.status_code, 200)  # compara la risposta allo status code 200, ovvero che la richiesta ha avuto pieno successo

    def test_unauthenticated_about(self):

        path = reverse('about')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()  # la request viene eseguita da un utente anonimo

        response = views.about(request)

        self.assertEqual(response.status_code, 200)  # about non ha bisogno del login, quindi ci aspettiamo uno status code 200


class ViewsTestLoginSignup(TestCase):
    """
        Test riguardanti il login_signup
    """

    def setUp(self):

        User.objects.create_user(username='utente_di_prova_1',
                                 password='password_di_prova_1')

    def test_log_in(self):

        client = Client()  # django fornisce la classe Client per compiere test simulando un utente reale

        response = client.get('/dashboard/')  # il client cerca di accedere alla dashboard
        self.assertEqual(response.status_code, 302)  # il client subisce un reindirizzamento
        self.assertEqual(response.url, '/')  # il reindirizzamento restituisce la pagina di login

        client.login(username='utente_di_prova_1',
                     password='password_di_prova_1')  # fornisco le credenziali di accesso di un utente esistente al client ed esegue il login

        response = client.get('/dashboard/')  # il client cerca di accedere alla dashboard

        self.assertEqual(response.status_code, 200)  # il client riesce ad accedere

        response = client.get('/')  # il client tenta di accedere di nuovo alla pagina di login

        self.assertEqual(response.status_code, 302)  # il client subisce un reindirizzamento

        self.assertEqual(response.url, '/dashboard/')  # il reindirizzamento restituisce la dashboard

    def test_log_out(self):

        client = Client()

        response = client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        client.login(username='utente_di_prova_1',
                     password='password_di_prova_1')

        response = client.get('/dashboard/')

        self.assertEqual(response.status_code, 200)

        client.logout()  # il client esegue il logout

        response = client.get('/dashboard/')  # il client cerca di accedere alla dashboard

        self.assertEqual(response.status_code, 302)  # il client subisce un reindirizzamento
        self.assertEqual(response.url, '/')  # il reindirizzamento restituisce la pagina di login


class ViewsTestDashboard(TestCase):
    """
        Test riguardanti la dashboard
    """

    def setUp(self):

        User.objects.create_user(username='utente_di_prova_1',
                                 password='password_di_prova_1')

    def test_dashboard(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('dashboard')
        request = RequestFactory().get(path)

        request.user = utente

        response = views.dashboard(request)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_dashboard(self):

        path = reverse('dashboard')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.dashboard(request)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_dashboard(self):

        path = reverse('dashboard')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.dashboard(request)

        self.assertEqual(response.url, '/')  # compara la URL in risposta alla request del server alla URL usata per il login


class ViewsTestAddBoard(TestCase):
    """
        Test riguardanti la add_board
    """

    def setUp(self):

        User.objects.create_user(username='utente_di_prova_1',
                                 password='password_di_prova_1')

    def test_add_board(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_board')
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_board(request)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_add_board(self):

        path = reverse('add_board')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_board(request)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_add_board(self):

        path = reverse('add_board')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_board(request)

        self.assertEqual(response.url, '/')


class ViewsTestAddOrRemoveUserToBoard(TestCase):
    """
        Test riguardanti la add_or_remove_user_to_board
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

    def test_add_or_remove_user_to_board_1(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_or_remove_user_to_board', kwargs={'board_id': 1})
        # print('path: ' + path)
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_or_remove_user_to_board(request, board_id=1)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_add_or_remove_user_to_board_1(self):

        path = reverse('add_or_remove_user_to_board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_or_remove_user_to_board(request, board_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_add_or_remove_user_to_board_1(self):

        path = reverse('add_or_remove_user_to_board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_or_remove_user_to_board(request, board_id=1)

        self.assertEqual(response.url, '/')

    def test_add_or_remove_user_to_board_2(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_or_remove_user_to_board', kwargs={'board_id': 1, 'user_id': 1})
        # print('path: ' + path)
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_or_remove_user_to_board(request, board_id=1, user_id=1)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_add_or_remove_user_to_board_2(self):

        path = reverse('add_or_remove_user_to_board', kwargs={'board_id': 1, 'user_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_or_remove_user_to_board(request, board_id=1, user_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_add_or_remove_user_to_board_2(self):

        path = reverse('add_or_remove_user_to_board', kwargs={'board_id': 1, 'user_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_or_remove_user_to_board(request, board_id=1, user_id=1)

        self.assertEqual(response.url, '/')


class ViewsTestModifyOrDeleteBoard(TestCase):
    """
        Test riguardanti la modify_or_delete_board
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

    def test_modify_or_delete_board(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('modify_or_delete_board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.modify_or_delete_board(request, board_id=1)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_modify_or_delete_board(self):

        path = reverse('modify_or_delete_board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.modify_or_delete_board(request, board_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_modify_or_delete_board(self):

        path = reverse('modify_or_delete_board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.modify_or_delete_board(request, board_id=1)

        self.assertEqual(response.url, '/')


class ViewsTestSearchUserBoard(TestCase):
    """
        Test riguardanti la search_user_board
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

# ##############################################################RIVEDERE################################################
#     def test_search_user_board(self):
#
#         utente = User.objects.get(username='utente_di_prova_1')
#
#         path = reverse('search_user_board')
#         print('path: ' + path)
#         request = RequestFactory().get(path)
#
#         request.user = utente
#
#         response = views.search_user_board(request)
#
#         self.assertEqual(response.status_code, 200)
# ######################################################RIVEDERE########################################################

    def test_unauthenticated_search_user_board(self):

        path = reverse('search_user_board')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.search_user_board(request)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_search_user_board(self):

        path = reverse('search_user_board')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.search_user_board(request)

        self.assertEqual(response.url, '/')


class ViewsTestBoardViews(TestCase):
    """
        Test riguardanti la board_view
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

    def test_board_views(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.board_view(request, board_id=1)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_board_views(self):

        path = reverse('board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.board_view(request, board_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_board_views(self):

        path = reverse('board', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.board_view(request, board_id=1)

        self.assertEqual(response.url, '/')


class ViewsTestAddColumn(TestCase):
    """
        Test riguardanti la add_column
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

    def test_add_column(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_column', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_column(request, board_id=1)

        self.assertEqual(response.status_code, 302)  # avviene un reindirizzamento a /board/1/

    def test_redirection_add_column(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_column', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_column(request, board_id=1)

        self.assertEqual(response.url, '/board/1/')

    def test_unauthenticated_add_column(self):

        path = reverse('add_column', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_column(request, board_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_add_column(self):

        path = reverse('add_column', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_column(request, board_id=1)

        self.assertEqual(response.url, '/')


class ViewsTestModifyOrDeleteColumn(TestCase):
    """
        Test riguardanti la modify_or_delete_column
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        Column.objects.create(name='colonna_di_prova',
                              mother_board=board,
                              n_cards=1)

    def test_modify_or_delete_column(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('modify_or_delete_column', kwargs={'column_id': 1, 'board_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.modify_or_delete_column(request, column_id=1, board_id=1)

        self.assertEqual(response.status_code, 302)  # avviene un reindirizzamento a /board/1/

    def test_redirection_modify_or_delete_column(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('modify_or_delete_column', kwargs={'column_id': 1, 'board_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.modify_or_delete_column(request, column_id=1, board_id=1)

        self.assertEqual(response.url, '/board/1/')

    def test_unauthenticated_modify_or_delete_column(self):

        path = reverse('modify_or_delete_column', kwargs={'column_id': 1, 'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.modify_or_delete_column(request, column_id=1, board_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_modify_or_delete_column(self):

        path = reverse('modify_or_delete_column', kwargs={'column_id': 1, 'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.modify_or_delete_column(request, column_id=1, board_id=1)

        self.assertEqual(response.url, '/')


class ViewsTestAddCard(TestCase):
    """
        Test riguardanti la add_card
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        Column.objects.create(name='colonna_di_prova',
                              mother_board=board,
                              n_cards=1)

    def test_add_card(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_card', kwargs={'board_id': 1, 'column_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_card(request, board_id=1, column_id=1)

        self.assertEqual(response.status_code, 302)  # avviene un reindirizzamento a /board/1/

    def test_redirection_add_card(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_card', kwargs={'board_id': 1, 'column_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_card(request, board_id=1, column_id=1)

        self.assertEqual(response.url, '/board/1/')

    def test_unauthenticated_add_card(self):

        path = reverse('add_card', kwargs={'board_id': 1, 'column_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_card(request, board_id=1, column_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_add_card(self):

        path = reverse('add_card', kwargs={'board_id': 1, 'column_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_card(request, board_id=1, column_id=1)

        self.assertEqual(response.url, '/')


class ViewsTestModifyOrDeleteCard(TestCase):
    """
        Test riguardanti la modify_or_delete_card
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
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

    def test_modify_or_delete_card(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('modify_or_delete_card', kwargs={'card_id': 1, 'board_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.modify_or_delete_card(request, card_id=1, board_id=1)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_modify_or_delete_card(self):

        path = reverse('modify_or_delete_card', kwargs={'card_id': 1, 'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.modify_or_delete_card(request, card_id=1, board_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_modify_or_delete_card(self):

        path = reverse('modify_or_delete_card', kwargs={'card_id': 1, 'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.modify_or_delete_card(request, card_id=1, board_id=1)

        self.assertEqual(response.url, '/')


class ViewsTestAddOrRemoveUserToCard(TestCase):
    """
        Test riguardanti la add_or_remove_user_to_card
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
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

    def test_add_or_remove_user_to_card(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_or_remove_user_to_card', kwargs={'user_id': 1, 'card_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_or_remove_user_to_card(request, user_id=1, card_id=1)

        self.assertEqual(response.status_code, 302)  # avviene un reindirizzamento a /modify_or_delete_card/1/1/

    def test_redirection_add_or_remove_user_to_card(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('add_or_remove_user_to_card', kwargs={'user_id': 1, 'card_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.add_or_remove_user_to_card(request, user_id=1, card_id=1)

        self.assertEqual(response.url, '/modify_or_delete_card/1/1/')

    def test_unauthenticated_add_or_remove_user_to_card(self):

        path = reverse('add_or_remove_user_to_card', kwargs={'user_id': 1, 'card_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_or_remove_user_to_card(request, user_id=1, card_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_add_or_remove_user_to_card(self):

        path = reverse('add_or_remove_user_to_card', kwargs={'user_id': 1, 'card_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.add_or_remove_user_to_card(request, user_id=1, card_id=1)

        self.assertEqual(response.url, '/')


class ViewsTestSearchUserCard(TestCase):
    """
        Test riguardanti la search_user_card
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
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

# ##############################################################RIVEDERE################################################
#     def test_search_user_card(self):
#
#         client = Client()
#
#         response = client.get(reverse('search_user_card'))
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.url, '/')
#
#         client.login(username='utente_di_prova_1',
#                      password='password_di_prova_1')
#
#         response = client.get(reverse('search_user_card'))
#
#
#
#
#
#         utente = User.objects.get(username='utente_di_prova_1')
#
#         path = reverse('search_user_card')
#         print('path: ' + path)
#         request = RequestFactory().get(path)
#
#         request.user = utente
#
#         response = views.search_user_card(request)
#
#         self.assertEqual(response.status_code, 200)
# ######################################################RIVEDERE########################################################

    def test_unauthenticated_search_user_card(self):

        path = reverse('search_user_card')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.search_user_card(request)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_search_user_card(self):

        path = reverse('search_user_card')
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.search_user_card(request)

        self.assertEqual(response.url, '/')


# ###############################################################RIVEDERE################################################
class ViewsTestRaiseErrorPage(TestCase):
    """
        Test riguardanti la raise_error_page
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
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

    def test_raise_error_page(self):

        client = Client()

        response = client.get(reverse('board', kwargs={'board_id': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        client.login(username='utente_di_prova_1',
                     password='password_di_prova_1')

        with self.assertRaises(Board.DoesNotExist):  # verifica se l'eccezione viene chiamata
            Board.objects.get(name='board_non_presente')  # tento di accedere ad una board inesistente nel database

        response = client.get(reverse('board', kwargs={'board_id': 2}))  # il client loggato tenta di accedere ad una board inesistente

        self.assertContains(response, 'The board you are trying to access does not exist.')  # La pagina contiene il messaggio di errore corretto

        # with self.assertRaises(views.raise_error_page):
        #     client.get(reverse('board', kwargs={'board_id': 2}))
        #
        # with self.assertRaisesMessage(views.raise_error_page, 'The board you are trying to access does not exist.'):
        #     client.get(reverse('board', kwargs={'board_id': 2}))

# ######################################################RIVEDERE########################################################


class ViewsTestBurndown(TestCase):
    """
        Test riguardanti la burndown
    """

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
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

    def test_burndown(self):

        utente = User.objects.get(username='utente_di_prova_1')

        path = reverse('burndown', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = utente

        response = views.burndown(request, board_id=1)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_burndown(self):

        path = reverse('burndown', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.burndown(request, board_id=1)

        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_redirection_burndown(self):

        path = reverse('burndown', kwargs={'board_id': 1})
        request = RequestFactory().get(path)

        request.user = AnonymousUser()

        response = views.burndown(request, board_id=1)

        self.assertEqual(response.url, '/')


# comando python per far partire i test di una singola classe: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse

# comando python per far partire i test di una singola funzione specifica: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse.nome_del_test

# comando python per far partire i soltanto i test di questo file: python manage.py test --pattern="test_views.py

# comando python per far partire tutti i test della cartella tests: python manage.py test


class ProvaClient(TestCase):

    def setUp(self):

        board = Board.objects.create(name='board_di_prova',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
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

    def test_prove_varie(self):

        client = Client()

        response = client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # client.login(username='utente_di_prova_1',
        #              password='password_di_prova_1')

        # response = client.get('/dashboard/')

        # self.assertEqual(response.status_code, 200)

        response = client.get('/')

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'username')

        response = client.post('/', {'username': 'utente_di_prova_1', 'password': 'password_di_prova_1'}, follow=True)

        response = client.get('/dashboard/')

        self.assertEqual(response.status_code, 302)
        # self.assertTrue(response)
        # response = self.client.get('/search_user_board/', follow=True)
        # self.assertContains(response, 'utente_di_prova_2')
