from django.test import TestCase

from django.urls import reverse, resolve


class UrlTests(TestCase):
    """
        test per validare il nome delle URL
    """

    def test_url_login_signup(self):

        url = reverse('login_signup')  # reverse('test') restituisce '/test/'
        self.assertEqual(url, '/')  # assertEqual verifica se i due parametri sono uguali

    def test_url_about(self):

        url = reverse('about')
        self.assertEqual(url, '/about/')

    def test_url_logout(self):

        url = reverse('logout')
        self.assertEqual(url, '/logout/')

    def test_url_dashboard(self):

        url = reverse('dashboard')
        self.assertEqual(url, '/dashboard/')

    def test_url_board(self):

        url = reverse('board', kwargs={'board_id': 1})
        self.assertEqual(url, '/board/1/')

    def test_url_burndown(self):

        url = reverse('burndown', kwargs={'board_id': 1})
        self.assertEqual(url, '/burndown/1/')

    def test_url_add_board(self):

        url = reverse('add_board')
        self.assertEqual(url, '/add_board/')

    def test_url_modify_or_delete_board(self):

        url = reverse('modify_or_delete_board', kwargs={'board_id': 1})
        self.assertEqual(url, '/modify_or_delete_board/1/')

    def test_url_add_or_remove_user_to_board_1(self):

        url = reverse('add_or_remove_user_to_board', kwargs={'board_id': 1})
        self.assertEqual(url, '/add_or_remove_user_to_board/1/')

    def test_url_add_or_remove_user_to_board_2(self):

        url = reverse('add_or_remove_user_to_board', kwargs={'board_id': 1, 'user_id': 1})
        self.assertEqual(url, '/add_or_remove_user_to_board/1/1/')

    def test_url_add_column(self):

        url = reverse('add_column', kwargs={'board_id': 1})
        self.assertEqual(url, '/add_column/1/')

    def test_url_modify_or_delete_column(self):

        url = reverse('modify_or_delete_column', kwargs={'column_id': 1, 'board_id': 1})
        self.assertEqual(url, '/modify_or_delete_column/1/1/')

    def test_url_add_card(self):

        url = reverse('add_card', kwargs={'board_id': 1, 'column_id': 1})
        self.assertEqual(url, '/add_card/1/1/')

    def test_url_modify_or_delete_card(self):

        url = reverse('modify_or_delete_card', kwargs={'card_id': 1, 'board_id': 1})
        self.assertEqual(url, '/modify_or_delete_card/1/1/')

    def test_url_add_or_remove_user_to_card(self):
        url = reverse('add_or_remove_user_to_card', kwargs={'user_id': 1, 'card_id': 1})
        self.assertEqual(url, '/modify_or_delete_card/add_or_remove_user_to_card/1/1/')

    def test_url_search_user_board(self):

        url = reverse('search_user_board')
        self.assertEqual(url, '/search_user_board/')

    def test_url_search_user_card(self):

        url = reverse('search_user_card')
        self.assertEqual(url, '/search_user_card/')


class UrlTestsView(TestCase):   # test sugli URL presenti nel file urls.py e la loro relazione nel file views.py
    """
        test per validare se le view corrispondono alle rispettive URL
    """

    def test_url_view_login_signup(self):

        resolver = resolve('/')  # la resolve() restituisce una ResolverMatch a cui e possibile passare metodi
        self.assertEqual(resolver.view_name, 'login_signup')  # .view_name restituisce la view che combacia con la URL

    def test_url_view_about(self):

        resolver = resolve('/about/')
        self.assertEqual(resolver.view_name, 'about')

    def test_url_view_logout(self):

        resolver = resolve('/logout/')
        self.assertEqual(resolver.view_name, 'logout')

    def test_url_view_dashboard(self):

        resolver = resolve('/dashboard/')
        self.assertEqual(resolver.view_name, 'dashboard')

    def test_url_view_board(self):

        resolver = resolve('/board/1/')
        self.assertEqual(resolver.view_name, 'board')

    def test_url_view_burndown(self):

        resolver = resolve('/burndown/1/')
        self.assertEqual(resolver.view_name, 'burndown')

    def test_url_view_add_board(self):

        resolver = resolve('/add_board/')
        self.assertEqual(resolver.view_name, 'add_board')

    def test_url_view_modify_or_delete_board(self):

        resolver = resolve('/modify_or_delete_board/1/')
        self.assertEqual(resolver.view_name, 'modify_or_delete_board')

    def test_url_view_add_or_remove_user_to_board_1(self):

        resolver = resolve('/add_or_remove_user_to_board/1/')
        self.assertEqual(resolver.view_name, 'add_or_remove_user_to_board')

    def test_url_view_add_or_remove_user_to_board_2(self):

        resolver = resolve('/add_or_remove_user_to_board/1/1')
        self.assertEqual(resolver.view_name, 'add_or_remove_user_to_board')

    def test_url_view_add_column(self):

        resolver = resolve('/add_column/1/')
        self.assertEqual(resolver.view_name, 'add_column')

    def test_url_view_modify_or_delete_column(self):

        resolver = resolve('/modify_or_delete_column/1/1/')
        self.assertEqual(resolver.view_name, 'modify_or_delete_column')

    def test_url_view_add_card(self):

        resolver = resolve('/add_card/1/1/')
        self.assertEqual(resolver.view_name, 'add_card')

    def test_url_view_modify_or_delete_card(self):

        resolver = resolve('/modify_or_delete_card/1/1/')
        self.assertEqual(resolver.view_name, 'modify_or_delete_card')

    def test_url_view_add_or_remove_user_to_card(self):

        resolver = resolve('/modify_or_delete_card/add_or_remove_user_to_card/1/1/')
        self.assertEqual(resolver.view_name, 'add_or_remove_user_to_card')

    def test_url_view_search_user_board(self):

        resolver = resolve('/search_user_board/')
        self.assertEqual(resolver.view_name, 'search_user_board')

    def test_url_view_search_user_card(self):

        resolver = resolve('/search_user_card/')
        self.assertEqual(resolver.view_name, 'search_user_card')


# comando python per far partire i test di una singola classe: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse

# comando python per far partire i test di una singola funzione specifica: python manage.py test progetto_isw.tests.test_models.NomeDellaClasse.nome_del_test

# comando python per far partire i soltanto i test di questo file: python manage.py test --pattern="test_urls.py

# comando python per far partire tutti i test della cartella tests: python manage.py test
