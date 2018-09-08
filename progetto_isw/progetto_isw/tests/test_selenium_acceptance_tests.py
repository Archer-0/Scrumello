from django.test import TestCase, RequestFactory, Client

from django.urls import reverse

import datetime

from ..models import Board, Column, Card
from django.contrib.auth.models import User, AnonymousUser

from .. import views


from django.test import LiveServerTestCase

from selenium.webdriver import Chrome


import time


time_to_wait = 5


class TestSelenio(LiveServerTestCase):

    def setUp(self):

        self.browser = Chrome()  # dico a selenium di usare Chrome

        self.browser.implicitly_wait(5)  # attesa implicita, attende tot secondi fino al caricamento di un componente della pagina WEB

        self.browser.get(self.live_server_url)  # il driver apre la pagina del server di django contenente il progetto

    def tearDown(self):

        self.browser.quit()  # chiude tutte le schede, il browser e termina il test in sicurezza

    def test_prova_selenio(self):

        bot = self.browser  # bot prende il driver di selenium per il browser

        # time.sleep(tempo_di_attesa)  # metto il thread in attesa per vedere fisicamente le operazioni eseguite da selenium(DEBUG)

        # self.browser.get('http://google.com')

        """
            Test per il login
        """

        search = bot.find_element_by_name('login_username')  # cerca l'elemento col nome indicato
        search.send_keys('test')  # immette il testo nel campo

        search = bot.find_element_by_name('login_password')
        search.send_keys('provaprova')

        # time.sleep(5)  # attende
        bot.find_element_by_xpath('//button[normalize-space()="Log in"]').click()  # cerca il bottone corretto

        """
            Test per la registrazione
        """

        search = bot.find_element_by_name('signup_username')
        search.send_keys('test')

        search = bot.find_element_by_name('signup_password')
        search.send_keys('provaprova')

        search = bot.find_element_by_name('signup_password_confirm')
        search.send_keys('provaprova')

        # time.sleep(5)  # attende
        bot.find_element_by_xpath('//button[normalize-space()="Sign up"]').click()

        time.sleep(time_to_wait)  # attende
