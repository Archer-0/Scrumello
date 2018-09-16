from django.test import LiveServerTestCase

from selenium.webdriver import Chrome

import time

import datetime

from ..models import Board, Column, Card
from django.contrib.auth.models import User

time_to_wait = 0.6

''' 
    IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE 
    
        - ricordarsi di fare: python manage.py collectstatic se non lo si e' gia' fatto per far funzionare javascript e il css
        
        - comando python per far partire i soltanto i test di questo file: python manage.py test --pattern="test_selenium_acceptance_tests.py"
        
        - comando python per far partire tutti i test della cartella tests: python manage.py test
    
    IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE 
'''

# class TestSelenium(LiveServerTestCase):
#
#     """
#         Prove varie
#     """
#
#     def setUp(self):
#
#         self.browser = Chrome()
#
#         self.browser.implicitly_wait(10)
#
#         self.browser.get(self.live_server_url)
#
#         """
#             inizzializzazione database temporaneo
#         """
#
#         User.objects.create_user(username='utente_di_prova_1',
#                                  password='password_di_prova_1')
#
#         User.objects.create_user(username='utente_di_prova_2',
#                                  password='password_di_prova_2')
#
#     def test_1(self):
#
#         print('\nTEST VARI\n')
#
#         bot = self.browser
#
#         bot.get(self.live_server_url)
#
#         time.sleep(time_to_wait)
#
#         search = bot.find_element_by_name('login_username')  # cerca la textbox per immettere l'username
#         search.send_keys('utente_di_prova_1')
#
#         time.sleep(time_to_wait)
#
#         search = bot.find_element_by_name('login_password')  # cerca la textbox per immettere la password
#         search.send_keys('password_di_prova_1')
#
#         time.sleep(time_to_wait)
#
#         search = bot.find_element_by_id('login_button')  # cerca il pulsante per confermare
#         search.click()
#
#         time.sleep(time_to_wait)
#
#         # Crea una board
#
#         search = bot.find_element_by_xpath("/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
#         search.click()
#
#         time.sleep(time_to_wait)
#
#         search = bot.find_element_by_name('board_name')  # cerca la textbox per immettere il nome della nuova board
#         search.send_keys('board_di_prova')
#
#         time.sleep(time_to_wait)
#
#         search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
#         search.click()
#
#         time.sleep(time_to_wait)
#
#         # Aggiunge un utente alla board
#
#         if is_css_javascript_working == True:
#             search = bot.find_element_by_css_selector("body > div > div > div > a")  # cerca il pulsante per gestire gli utenti                ###################################################################################################################
#             search.click()
#         else:
#             search = bot.find_element_by_xpath("/html/body/div/div/ul/li[1]/a")  # cerca il pulsante per gestire gli utenti
#             search.click()
#
#         time.sleep(time_to_wait)
#
#         search = bot.find_element_by_css_selector("#id_user_name")  # cerca la barra di ricerca degli utenti                                ##################################################################################################################
#         search.click()
#
#         time.sleep(time_to_wait)
#
#         search.send_keys('utente_di_prova_2')
#
#         time.sleep(time_to_wait)
#
#         if is_css_javascript_working == True:
#             search = bot.find_element_by_css_selector("#results > li:nth-child(1) > form > button > i")  # cerca il pulsante per aggiungere il primo utente           #################################################################
#             search.click()
#
#         """
#             Test per rimuovere un utente dalla board corrente
#         """
#
#         if is_css_javascript_working == True:
#             search = bot.find_element_by_css_selector("#results > li > form > button.delete_user_button > i")  # cerca il pulsante per eliminare il primo utente                  #######################################################
#             search.click()
#
#         time.sleep(9999)
#
#     def tearDown(self):
#
#         self.browser.refresh()
#         self.browser.quit()


# self.browser.refresh()  # refresh alla pagina per evitare problemi con la quit()  # funziona solo su alcuni test, altri non ne hanno bisogno
class TestSeleniumSignUp(LiveServerTestCase):

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

    def test_sign_up(self):

        print('\nTEST REGISTRAZIONE\n')

        bot = self.browser  # bot prende il driver di selenium per il browser

        time.sleep(time_to_wait)  # metto il thread in attesa per vedere fisicamente le operazioni eseguite da selenium(DEBUG)

        """
            Test per la registrazione
        """

        search = bot.find_element_by_id('signup-button')
        search.click()
        time.sleep(2)

        search = bot.find_element_by_name('signup_username')  # cerca la textbox per immettere l'username
        search.send_keys('utente_di_prova')  # immette il testo nel campo

        search = bot.find_element_by_name('signup_password')  # cerca la textbox per immettere la password
        search.send_keys('password_di_prova')

        search = bot.find_element_by_name('signup_password_confirm')  # cerca la textbox per immettere la conferma della password
        search.send_keys('password_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('signup_button')  # cerca il bottone corretto
        search.click()  # preme il bottone

        time.sleep(time_to_wait)

    def tearDown(self):

        # self.browser.refresh()  # NO
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

        print('\nTEST LOGIN\n')

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

        self.browser.refresh()  # OK
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

        print('\nTEST LOGOUT\n')

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
        time.sleep(2)

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('logout_link')  # cerca il pulsante per il logout
        search.click()

        time.sleep(2)

        time.sleep(time_to_wait)

    def tearDown(self):

        # self.browser.refresh()  # NO
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

        print('\nTEST CREATE BOARD\n')

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
        search.send_keys('board_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('create_board_button')  # cerca il pulsante per confermare
        search.click()

        time.sleep(time_to_wait)

    def test_delete_board(self):

        print('\nTEST DELETE BOARD\n')

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
            Test per cancellare una board
        """

        search = bot.find_element_by_xpath("/html/body/header/div/div[2]/form/a[1]/i")  # trova la posizione dell'elemento per far comparire il tasto di cancellazione board  # #############################################################################################################################################################
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/header/div/div[2]/form/button[2]")  # cerca il pulsante per cancellare la board
        search.click()

        time.sleep(time_to_wait)

    def tearDown(self):

        self.browser.refresh()  # OK
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

    def test_1_create_column(self):

        print('\nTEST CREATE COLUMN\n')

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
            Test per creare una colonna
        """

        search = bot.find_element_by_name('column_name')  # cerca la textbox per immettere il nome della colonna
        search.send_keys('colonna_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/main/ul/li/div/form/button")  # cerca il pulsante per creare la colonna
        search.click()

        time.sleep(2)

    def test_2_edit_column(self):

        print('\nTEST EDIT COLUMN\n')

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

        # Crea una colonna

        search = bot.find_element_by_name('column_name')  # cerca la textbox per immettere il nome della colonna
        search.send_keys('colonna_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/main/ul/li/div/form/button")  # cerca il pulsante per creare la colonna
        search.click()

        time.sleep(2)

        """
            Test per modificare una colonna
        """

        search = bot.find_element_by_xpath("/html/body/main/ul/li[1]/div[1]/form/a[1]/i")  # cerca il pulsante per modificare la colonna
        search.click()

        time.sleep(2)

        search = bot.find_element_by_css_selector("#id_new_column_name")  # cerca la textbox per modificare il nome della colonna
        search.click()

        time.sleep(2)

        search.send_keys('colonna_di_prova_modificata')

        time.sleep(5)

        search = bot.find_element_by_xpath("/html/body/main/ul/li[1]/div[1]/form/button[1]")  # cerca il bottone per confermare le modifiche alla colonna
        search.click()

        time.sleep(time_to_wait)

        bot.refresh()  # il tearDown creava qualche problema senza un refresh

    def test_3_delete_column(self):

        print('\nTEST DELETE COLUMN\n')

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

        search = bot.find_element_by_xpath("/html/body/main/ul/li[1]/div[1]/form/a[1]/i")  # trova la posizione dell'elemento per far comparire il tasto di cancellazione board  # #############################################################################################################################################################
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/main/ul/li[1]/div[1]/form/button[2]")  # cerca il pulsante per canellare la colonna
        search.click()

        time.sleep(time_to_wait)

    def tearDown(self):

        # self.browser.refresh()  # NO
        self.browser.quit()


class TestSeleniumCard(LiveServerTestCase):

    """
        Test riguardanti le carte
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

    def test_1_create_card(self):

        print('\nTEST CREATE CARD\n')

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

        # Crea una colonna

        search = bot.find_element_by_name('column_name')  # cerca la textbox per immettere il nome della colonna
        search.send_keys('colonna_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/main/ul/li/div/form/button")  # cerca il pulsante per creare la colonna
        search.click()

        """
            Test per creare una carta
        """

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("#id_new_card_title")  # cerca la textbox per creare una nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('carta_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("#id_new_card_description")  # cerca la text box per immettere la descrizione della nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('descrizione_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("#id_new_card_expire_date")  # cerca il pulsante per immettere la data di scadenza alla nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('2019')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("#id_new_card_story_points")  # cerca il pulsante per immettere il valore dei punti storia
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('2')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("body > main > ul > li:nth-child(1) > div.card-container.last_card > form > div.card-content.new_card.hidden > div.new_card_button-set > button.new_card_submit_button")  # cerca il pulsante per creare la nuova carta
        search.click()

        time.sleep(time_to_wait)

        bot.refresh()

    def test_2_edit_card(self):

        print('\nTEST EDIT CARD')

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

        search = bot.find_element_by_xpath(
            "/html/body/main/div[1]/button/span")  # cerca il pulsante per far apparire la textbox per immettere il nome di una nuova board
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

        search = bot.find_element_by_xpath(
            "/html/body/main/ul/li/div/form/button")  # cerca il pulsante per creare la colonna
        search.click()

        time.sleep(time_to_wait)

        # Crea una carta

        search = bot.find_element_by_css_selector("#id_new_card_title")  # cerca la textbox per creare una nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('carta_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "#id_new_card_description")  # cerca la text box per immettere la descrizione della nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('descrizione_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "#id_new_card_expire_date")  # cerca il pulsante per immettere la data di scadenza alla nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('2019')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "#id_new_card_story_points")  # cerca il pulsante per immettere il valore dei punti storia
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('2')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "body > main > ul > li:nth-child(1) > div.card-container.last_card > form > div.card-content.new_card.hidden > div.new_card_button-set > button.new_card_submit_button")  # cerca il pulsante per creare la nuova carta
        search.click()

        time.sleep(time_to_wait)

        # Crea un'altra colonna

        search = bot.find_element_by_css_selector("#id_column_name") # cerca la textbox per immettere il nome della colonna
        search.send_keys('colonna_di_prova_2')

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath(
            "/html/body/main/ul/li[2]/div/form/button")  # cerca il pulsante per creare la colonna
        search.click()

        time.sleep(time_to_wait)

        # Modifica una carta

        search = bot.find_element_by_css_selector(
            "body > main > ul > li:nth-child(1) > ul > li:nth-child(1) > div.card-title-container > form > h1 > span > button"
        )
        search.click()

        search = bot.find_element_by_css_selector("#id_new_card_title")
        search.send_keys("carta_modificata")

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "#id_new_card_description")
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('descrizione_modificata')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "#id_new_card_expire_date")
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('2020')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "#id_new_card_story_points")
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('3')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "#id_new_card_mother_column"
        )
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "#id_new_card_mother_column > option:nth-child(2)"
        )
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector(
            "body > main > form > div > button"
        )
        search.click()

        time.sleep(time_to_wait)

        bot.refresh()

    def test_3_delete_card(self):

        print('\nTEST DELETE CARD\n')

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

        # Crea una colonna

        search = bot.find_element_by_name('column_name')  # cerca la textbox per immettere il nome della colonna
        search.send_keys('colonna_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_xpath("/html/body/main/ul/li/div/form/button")  # cerca il pulsante per creare la colonna
        search.click()

        time.sleep(time_to_wait)

        # Crea una carta

        search = bot.find_element_by_css_selector("#id_new_card_title")  # cerca la textbox per creare una nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('carta_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("#id_new_card_description")  # cerca la text box per immettere la descrizione della nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('descrizione_di_prova')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("#id_new_card_expire_date")  # cerca il pulsante per immettere la data di scadenza alla nuova carta
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('2019')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("#id_new_card_story_points")  # cerca il pulsante per immettere il valore dei punti storia
        search.click()

        time.sleep(time_to_wait)

        search.send_keys('2')

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("body > main > ul > li:nth-child(1) > div.card-container.last_card > form > div.card-content.new_card.hidden > div.new_card_button-set > button.new_card_submit_button")  # cerca il pulsante per creare la nuova carta
        search.click()

        time.sleep(time_to_wait)

        """
            Test per cancellare una carta
        """
        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector("body > main > ul > li:nth-child(1) > ul > li > div.card-title-container > form > div > button")  # cerca il pulsante per cancellare la carta
        search.click()

        time.sleep(time_to_wait)

    def tearDown(self):

        # self.browser.refresh()  # NO
        self.browser.quit()


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

    def test_1_add_user_to_board(self):

        print('\nTEST ADD USER TO A BOARD\n')

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

        time.sleep(2)

        """
            test per aggiungere un utente alla board corrente
        """

        time.sleep(2)

        search = bot.find_element_by_css_selector('#open_toolbar')
        search.click()
        time.sleep(2)

        search = bot.find_element_by_id('manage_users_button')
        search.click()
        time.sleep(2)

        search = bot.find_element_by_css_selector("#id_user_name")  # cerca la barra di ricerca degli utenti
        search.click()
        time.sleep(2)

        search.send_keys('utente_di_prova_2')

        time.sleep(2)

        search = bot.find_element_by_css_selector("#results > li:nth-child(1) > form > button > i")  # cerca il pulsante per aggiungere il primo utente
        search.click()

        time.sleep(2)

        time.sleep(time_to_wait)

        bot.refresh()

    def test_2_remove_user_from_board(self):

        print('\nTEST REMOVE USER FROM A BOARD\n')

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

        time.sleep(time_to_wait)

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

        search = bot.find_element_by_css_selector('#open_toolbar')
        search.click()

        time.sleep(2)

        search = bot.find_element_by_id('manage_users_button')
        search.click()

        time.sleep(2)

        search = bot.find_element_by_css_selector("#id_user_name")  # cerca la barra di ricerca degli utenti
        search.click()

        time.sleep(2)

        search.send_keys('utente_di_prova_2')

        time.sleep(2)

        search = bot.find_element_by_css_selector("#results > li:nth-child(1) > form > button > i")  # cerca il pulsante per aggiungere il primo utente
        search.click()

        time.sleep(2)

        """
            Test per rimuovere un utente dalla board corrente
        """

        search = bot.find_element_by_css_selector("#results > li > form > button.delete_user_button > i")  # cerca il pulsante per eliminare il primo utente
        search.click()

        time.sleep(2)

        time.sleep(time_to_wait)

        bot.refresh()

    def test_3_burndown(self):

        print('\nTEST BURNDOWN\n')

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

        time.sleep(2)

        """
            test per aprire il burndown della board corrente
        """

        time.sleep(time_to_wait)

        search = bot.find_element_by_css_selector('#open_toolbar')
        search.click()

        time.sleep(time_to_wait)

        search = bot.find_element_by_id('burndown_button')
        search.click()

        time.sleep(2)

        time.sleep(time_to_wait)

    def tearDown(self):

        # self.browser.refresh()  # NO
        self.browser.quit()
