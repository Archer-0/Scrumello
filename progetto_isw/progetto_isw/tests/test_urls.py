from django.test import TestCase

from django.urls import reverse


class UrlTests(TestCase):

    def test_url_dashboard(self):
        """
            test per validare il nome della URL

            il test deve passare
        """

        url = reverse('dashboard')  # reverse('test') restituisce '/test/'
        self.assertEqual(url, '/dashboard/')  # assertEqual verifica se i due parametri sono uguali

# comando python per far partire il test: python manage.py test
