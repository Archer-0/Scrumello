from django.test import LiveServerTestCase

from selenium.webdriver import Chrome

import time

import datetime

from ..models import Board, Column, Card
from django.contrib.auth.models import User


time_to_wait = 0

is_css_javascript_working = False


class TestSelenium(LiveServerTestCase):

    def setUp(self):

        self.browser = Chrome()

        self.browser.implicitly_wait(10)

        self.browser.get(self.live_server_url)

        """
            inizzializzazione database temporaneo
        """

        User.objects.create_user(username='utente_di_prova_1',
                                 password='password_di_prova_1')

        User.objects.create_user(username='utente_di_prova_2',
                                 password='password_di_prova_2')

    def test_1(self):

        print('sono nella test_1')

        bot = self.browser

        bot.get(self.live_server_url)

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        # Crea una board

        search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
        search.send_keys('board_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

        """
            test per aggiungere un utente alla board corrente
        """

        if is_css_javascript_working == True:
            search = bot.find_element_by_css_selector("body > div > div > div > a")  # cerca il pulsante per gestire gli utenti                ###################################################################################################################
            search.click()
        else:
            search = bot.find_element_by_xpath("/html/body/div/div/ul/li[1]/a")  # cerca il pulsante per gestire gli utenti
            search.click()

        time.sleep(time_to_wait)

        time.sleep(5)

        search = bot.find_element_by_css_selector("#id_user_name")  # cerca la barra di ricerca degli utenti                                ##################################################################################################################
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('utente_di_prova_2')

        time.sleep(time_to_wait)


        if is_css_javascript_working == True:

            search = bot.find_element_by_css_selector("#results > li:nth-child(1) > form > button > i")  # cerca il pulsante per aggiungere l'utente
            search.click()

        time.sleep(time_to_wait)

        time.sleep(60)

    def tearDown(self):

        self.browser.refresh()
        self.browser.quit()

"""
    if is_css_javascript_working == True:
        search = bot.find_element_by_xpath("/html/body/main/ul/li/div/form/button")  # trova la posizione dell'elemento per far comparire il tasto di cancellazione board  # #############################################################################################################################################################
        search.click()
"""

"""
    /html/body/div/div/div/a
"""


class TestSeleniumRegistrazione(LiveServerTestCase):

    """
        Test riguardanti la registrazione
    """

    def setUp(self):

        self.browser = Chrome()  # dico a selenium di usare Chrome

        self.browser.implicitly_wait(5)  # attesa implicita, attende tot secondi fino al caricamento di un componente della pagina WEB

        self.browser.get(self.live_server_url)  # il driver apre la pagina del server di django contenente il progetto

        """
            Inizzializzazione database temporaneo 
        """
        board = Board.objects.create(name='board_di_prova_1',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        colonna = Column.objects.create(name='colonna_di_prova_1',
                                        mother_board=board,
                                        n_cards=1)

        carta = Card.objects.create(title='carta_di_prova_1',
                                    description='descrizione_di_prova_1',
                                    expire_date=datetime.datetime(2018, 9, 1),
                                    story_points=5,
                                    mother_column=colonna,
                                    n_users=2)

        carta.users.add(user1)
        carta.users.add(user2)

    def test_registrazione(self):

        bot = self.browser  # bot prende il driver di selenium per il browser

        time.sleep(time_to_wait)  # metto il thread in attesa per vedere fisicamente le operazioni eseguite da selenium(DEBUG)

        """
            Test per la registrazione
        """

        search = bot.find_element_by_name('signup_username')  # cerca la textbox per immettere l'username
        search.send_keys('test')  # immette il testo nel campo

        search = bot.find_element_by_name('signup_password')  # cerca la textbox per immettere la password
        search.send_keys('provaprova')

        search = bot.find_element_by_name('signup_password_confirm')  # cerca la textbox per immettere la conferma della password
        search.send_keys('provaprova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('signup_button')  # cerca il bottone corretto
        search.click()  # preme il bottone

        time.sleep(time_to_wait)

    def tearDown(self):

        self.browser.refresh()  # refresh alla pagina per evitare problemi con la quit()
        self.browser.quit()  # chiude tutte le schede, il browser e termina il test in sicurezza


class TestSeleniumLogin(LiveServerTestCase):

    """
        Test riguardanti il login
    """

    def setUp(self):

        self.browser = Chrome()

        self.browser.implicitly_wait(5)

        self.browser.get(self.live_server_url)

        """
            inizzializzazione database temporaneo
        """
        board = Board.objects.create(name='board_di_prova_1',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        colonna = Column.objects.create(name='colonna_di_prova_1',
                                        mother_board=board,
                                        n_cards=1)

        carta = Card.objects.create(title='carta_di_prova_1',
                                    description='descrizione_di_prova_1',
                                    expire_date=datetime.datetime(2018, 9, 1),
                                    story_points=5,
                                    mother_column=colonna,
                                    n_users=2)

        carta.users.add(user1)
        carta.users.add(user2)

    def test_login(self):

        bot = self.browser

        time.sleep(time_to_wait)

        """
            Test per il login
        """

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

    def tearDown(self):

        self.browser.refresh()
        self.browser.quit()


class TestSeleniumLogout(LiveServerTestCase):

    """
        Test riguardanti il logout
    """

    def setUp(self):

        self.browser = Chrome()

        self.browser.implicitly_wait(5)

        self.browser.get(self.live_server_url)

        """
            inizzializzazione database temporaneo
        """
        board = Board.objects.create(name='board_di_prova_1',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        colonna = Column.objects.create(name='colonna_di_prova_1',
                                        mother_board=board,
                                        n_cards=1)

        carta = Card.objects.create(title='carta_di_prova_1',
                                    description='descrizione_di_prova_1',
                                    expire_date=datetime.datetime(2018, 9, 1),
                                    story_points=5,
                                    mother_column=colonna,
                                    n_users=2)

        carta.users.add(user1)
        carta.users.add(user2)

    def test_logout(self):

        bot = self.browser

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        """
            Test per il logout
        """

        time.sleep(time_to_wait)

        search = bot.find_element_by_link_text('logout')  # cerca il pulsante per il logout
        search.click()

        time.sleep(time_to_wait)

    def tearDown(self):

        self.browser.refresh()
        self.browser.quit()


class TestSeleniumBoard(LiveServerTestCase):

    """
        Test riguardanti le board
    """

    def setUp(self):

        self.browser = Chrome()

        self.browser.implicitly_wait(5)

        self.browser.get(self.live_server_url)

        """
            inizzializzazione database temporaneo
        """
        board = Board.objects.create(name='board_di_prova_1',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        colonna = Column.objects.create(name='colonna_di_prova_1',
                                        mother_board=board,
                                        n_cards=1)

        carta = Card.objects.create(title='carta_di_prova_1',
                                    description='descrizione_di_prova_1',
                                    expire_date=datetime.datetime(2018, 9, 1),
                                    story_points=5,
                                    mother_column=colonna,
                                    n_users=2)

        carta.users.add(user1)
        carta.users.add(user2)

    def test_create_board(self):

        bot = self.browser

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

        """
            Test per creare una board
        """

        search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
        search.send_keys('board_di_prova_creata_ora')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

    def test_delete_board(self):

        bot = self.browser

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        # Crea una board

        search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
        search.send_keys('board_di_prova_creata_ora')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

        """
            Test per cancellare una board
        """

        if is_css_javascript_working == True:
            search = bot.find_element_by_xpath("/html/body/header/div/div[2]/form/a[1]/i")  # trova la posizione dell'elemento per far comparire il tasto di cancellazione board  # #############################################################################################################################################################
            search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/header/div/div[2]/form/button[2]")  # cerca il pulsante per cancellare la board
        search.click()

        time.sleep(time_to_wait)

    def tearDown(self):

        self.browser.refresh()
        self.browser.quit()


class TestSeleniumColumn(LiveServerTestCase):

    """
        Test riguardanti le colonne
    """

    def setUp(self):

        self.browser = Chrome()

        self.browser.implicitly_wait(5)

        self.browser.get(self.live_server_url)

        """
            inizzializzazione database temporaneo
        """
        board = Board.objects.create(name='board_di_prova_1',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        colonna = Column.objects.create(name='colonna_di_prova_1',
                                        mother_board=board,
                                        n_cards=1)

        carta = Card.objects.create(title='carta_di_prova_1',
                                    description='descrizione_di_prova_1',
                                    expire_date=datetime.datetime(2018, 9, 1),
                                    story_points=5,
                                    mother_column=colonna,
                                    n_users=2)

        carta.users.add(user1)
        carta.users.add(user2)

    def test_create_column(self):

        bot = self.browser

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        # Crea una board

        search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
        search.send_keys('board_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

        """
            Test per creare una colonna in una board
        """

        search = bot.find_element_by_name('column_name')  # cerca la textbox per immettere il nome della colonna
        search.send_keys('colonna_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/main/ul/li/div/form/button")  # cerca il pulsante per creare la colonna
        search.click()

        time.sleep(time_to_wait)

    def test_delete_column(self):

        bot = self.browser

        bot.get(self.live_server_url)

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        # Crea una board

        search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
        search.send_keys('board_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

        # Crea una colonna

        search = bot.find_element_by_name('column_name')  # cerca la textbox per immettere il nome della colonna
        search.send_keys('colonna_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/main/ul/li/div/form/button")  # cerca il pulsante per creare la colonna
        search.click()

        time.sleep(time_to_wait)

        """
            Test per cancellare una colonna
        """

        if is_css_javascript_working == True:
            search = bot.find_element_by_xpath("/html/body/main/ul/li[1]/div[1]/form/a[1]/i")  # trova la posizione dell'elemento per far comparire il tasto di cancellazione board  # #############################################################################################################################################################
            search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/main/ul/li[1]/div[1]/form/button[2]")  # cerca il pulsante per canellare la colonna
        search.click()

        time.sleep(time_to_wait)

    def tearDown(self):

        self.browser.refresh()
        self.browser.quit()


class TestSeleniumCard(LiveServerTestCase):

    def setUp(self):
        self.browser = Chrome()

        self.browser.implicitly_wait(5)

        self.browser.get(self.live_server_url)

        """
            inizzializzazione database temporaneo
        """
        board = Board.objects.create(name='board_di_prova_1',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        colonna = Column.objects.create(name='colonna_di_prova_1',
                                        mother_board=board,
                                        n_cards=1)

        carta = Card.objects.create(title='carta_di_prova_1',
                                    description='descrizione_di_prova_1',
                                    expire_date=datetime.datetime(2018, 9, 1),
                                    story_points=5,
                                    mother_column=colonna,
                                    n_users=2)

        carta.users.add(user1)
        carta.users.add(user2)

    def test_create_card(self):

        bot = self.browser

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        # Crea una board

        search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
        search.send_keys('board_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

        """
            Test per creare una carta in una colonna
        """

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()


################################################################################################################################
class TestSeleniumUser(LiveServerTestCase):

    """
        Test riguardanti gli utenti
    """

    def setUp(self):
        self.browser = Chrome()

        self.browser.implicitly_wait(5)

        self.browser.get(self.live_server_url)

        """
            inizzializzazione database temporaneo
        """
        board = Board.objects.create(name='board_di_prova_1',
                                     n_users=2,
                                     n_columns=1,
                                     n_cards=1)

        user1 = User.objects.create_user(username='utente_di_prova_1',
                                         password='password_di_prova_1')

        user2 = User.objects.create_user(username='utente_di_prova_2',
                                         password='password_di_prova_2')

        board.users.add(user1)
        board.users.add(user2)

        colonna = Column.objects.create(name='colonna_di_prova_1',
                                        mother_board=board,
                                        n_cards=1)

        carta = Card.objects.create(title='carta_di_prova_1',
                                    description='descrizione_di_prova_1',
                                    expire_date=datetime.datetime(2018, 9, 1),
                                    story_points=5,
                                    mother_column=colonna,
                                    n_users=2)

        carta.users.add(user1)
        carta.users.add(user2)

    def test_add_user_to_board(self):

        print('sono nella test_1')

        bot = self.browser

        bot.get(self.live_server_url)

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        # Crea una board

        search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
        search.send_keys('board_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

        """
            test per aggiungere un utente alla board corrente
        """

        if is_css_javascript_working == True:
            search = bot.find_element_by_css_selector("body > div > div > div > a")  # cerca il pulsante per gestire gli utenti                ###################################################################################################################
            search.click()
        else:
            search = bot.find_element_by_xpath("/html/body/div/div/ul/li[1]/a")  # cerca il pulsante per gestire gli utenti
            search.click()

        time.sleep(time_to_wait)

        time.sleep(5)

        search = bot.find_element_by_css_selector("#id_user_name")  # cerca la barra di ricerca degli utenti                                ##################################################################################################################
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('utente_di_prova_2')

        time.sleep(time_to_wait)

        if is_css_javascript_working == True:

            search = bot.find_element_by_css_selector("#results > li:nth-child(1) > form > button > i")  # cerca il pulsante per aggiungere il primo utente
            search.click()

        time.sleep(time_to_wait)

    def test_remove_user_to_board(self):

        print('sono nella test_1')

        bot = self.browser

        bot.get(self.live_server_url)

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova_1')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
        search.click()

        # Crea una board

        search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
        search.send_keys('board_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

        # Aggiunge un utente alla board

        if is_css_javascript_working == True:
            search = bot.find_element_by_css_selector("body > div > div > div > a")  # cerca il pulsante per gestire gli utenti                ###################################################################################################################
            search.click()
        else:
            search = bot.find_element_by_xpath("/html/body/div/div/ul/li[1]/a")  # cerca il pulsante per gestire gli utenti
            search.click()

        time.sleep(time_to_wait)

        time.sleep(5)

        search = bot.find_element_by_css_selector("#id_user_name")  # cerca la barra di ricerca degli utenti                                ##################################################################################################################
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('utente_di_prova_2')

        time.sleep(time_to_wait)

        if is_css_javascript_working == True:

            search = bot.find_element_by_css_selector("#results > li:nth-child(1) > form > button > i")  # cerca il pulsante per aggiungere il primo utente
            search.click()

        """
            Test per rimuovere un utente dalla board corrente        
        """

        if is_css_javascript_working == True:

            search = bot.find_element_by_css_selector("#results > li > form > button.delete_user_button > i")  # cerca il pulsante per aggiungere il primo utente
            search.click()

        time.sleep(time_to_wait)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()


# comando python per far partire i soltanto i test di questo file: python manage.py test --pattern="test_selenium_acceptance_tests.py

# comando python per far partire tutti i test della cartella tests: python manage.py test
