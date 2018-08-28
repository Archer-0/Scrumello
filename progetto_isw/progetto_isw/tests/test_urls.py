from django.test import TestCase

from django.urls import reverse


class UrlTests(TestCase):

    def test_url_login_signup(self):
        """
            test per validare il nome della URL

            il test deve passare
        """

        url = reverse('login_signup')  # reverse('test') restituisce '/test/'
        self.assertEqual(url, '/')  # assertEqual verifica se i due parametri sono uguali

    def test_url_about(self):

        url = reverse('about')
        self.assertEqual(url, '/about/')

    def test_url_dashboard(self):

        url = reverse('dashboard')
        self.assertEqual(url, '/dashboard/')

    def test_url_logout(self):

        url = reverse('logout')
        self.assertEqual(url, '/logout/')

# comando python per far partire il test: python manage.py test
