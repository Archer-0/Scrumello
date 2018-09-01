# coding=utf-8
import random
import sys
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime

from forms import *

welcomeTexts = ['pandas 🐼!', 'cookies!', 'RGB!', 'the force!', 'ice cream!', 'cmd.exe', 'sudo makeprrr 🐱']
new_user = False


# about page
def about(request):
    # redirezione alla pagine tra apici
    return render(request, 'about.html')


# login_signup page
def login_signup(request):
    # se l'utente e' gia' loggato request.user sara' diverso
    # da 'AnonymousUser' (standard utilizzato da django per idetificare
    # gli utenti non autenticati)
    if str(request.user) != 'AnonymousUser':
        # stampa log nella console
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') User \"' + request.user.username + '\" already authenticated.')
        # redirezione alla dashboard dell'utente loggato
        return HttpResponseRedirect("/dashboard/", {
            "user": request.user,
        })

    if request.method == "POST":            # se e' stata effettuata una richiesta POST
        # salvataggio dei form presenti nella pagina in variabili
        signup_form = SignupForm(request.POST)
        login_form = LoginForm(request.POST)

        if request.POST.get('submit') == 'log_in':                          # se il valore della submt e' 'log_in'
            print ('submit value = ' + str(request.POST.get('submit')))     # log
            if login_form.is_valid():
                print ('login form is valid')   #log
                # salvataggio dei dati del form di login in delle variabili
                username = login_form.cleaned_data['login_username']
                password = login_form.cleaned_data['login_password']

                user = authenticate(username=username, password=password)   # autenticazione dell'utente
                # se l'utente esiste ed user.is_active == true
                if user is not None:
                    # se l'utente e' attivo si effettua il login e lo si ridireziona alla dashboard
                    if user.is_active:
                        login(request, user)        # si effettua il login dell'utente con la funzione di django
                        global new_user             # per non mostrare il tutorial
                        new_user = False

                        # redirezione dell'utente alla sua dashboard
                        return HttpResponseRedirect("/dashboard/", {
                            "user": user,
                        })

                    # se l'utente non e' attivo vuol dire che e' stato bloccato e si stampa un messaggio di errore
                    else:
                        # si confeziona un messaggio di errore
                        error_message = 'The user \"' + login_form.cleaned_data[
                            'login_username'] + '\" has been banned.'

                        # ricarica la pagina di login e signup caricando anche l'errore verificatosi
                        return render(request, "login_signup.html", {
                            "login_form": login_form, "signup_form": signup_form, 'login_error_message': error_message
                        })
                # se l'utente non esiste si stampa un messaggio di errore
                else:
                    # come sopra
                    error_message = 'Wrong username or password. Try again!'
                    return render(request, "login_signup.html", {
                        "login_form": login_form, "signup_form": signup_form, 'login_error_message': error_message
                    })

        # se viene fatto il submit del form di registrazione
        # "submit" e' l'attributo "name" del button del form
        # se il valore di submit e' 'sign_up' si esegue la procedura di registrazione
        elif request.POST.get('submit') == 'sign_up' and signup_form.is_valid():
            user = User()            # creazione nuovo utente

            # verifica che non ci sia un altro utente on lo stesso username
            user_tmp = User.objects.all().filter(username=signup_form.cleaned_data['signup_username'])
            if user_tmp.__len__() > 0:          # se esiste un altro username uguale
                # si confeziona il messaggio di errore
                error_message = 'The user \"' + signup_form.cleaned_data[
                    'signup_username'] + '\" already exists. Did you want to login instead?'

                # (per il CSS della pagina di login & signup per fare in modo che la finestra sia posizionata
                # su signup)
                signup_form.fields['signup_username'].widget.attrs['class'] = 'forms_field-input form-error-outline'

                # si ricarica la pagina di signup con errore verificatosi
                return render(request, "login_signup.html", {
                    'login_form': login_form, 'signup_form': signup_form, 'form_class': 'signup-click',
                    "signup_error_message": error_message
                })

            # se non esiste nessun altro utente con lo stesso username si verificano
            # che le password inserite siano uguali (in caso positivo si salva l'utente,
            # si esegue il login dello stesso e lo si ridireziona alla sua dashboard)
            if signup_form.cleaned_data['signup_password'] == signup_form.cleaned_data['signup_password_confirm']:
                user.username = signup_form.cleaned_data['signup_username']
                user.set_password(signup_form.cleaned_data['signup_password'])
                user.save()
                login(request, user)
                print('new user registered')
                global new_user
                new_user = True
                return HttpResponseRedirect("/dashboard/")
            else:       # se le password non sono uguali
                # solita prcedura per visualizzazione errore
                error_message = "Passwords do not match"
                signup_form.fields['signup_password_confirm'].widget.attrs[
                    'class'] = 'forms_field-input form-error-outline'
                return render(request, "login_signup.html", {
                    'login_form': login_form, 'signup_form': signup_form, 'form_class': 'signup-click',
                    "signup_error_message": error_message
                })

    # se non e' stata effettuata nessuna richiesta POST si carica la pagina con i form vuoti
    else:
        login_form = LoginForm()
        signup_form = SignupForm()

    return render(request, 'login_signup.html', {
        'login_form': login_form,
        'signup_form': signup_form,
        'welcomeText': welcomeTexts[random.randrange(0, len(welcomeTexts))],
        # 'signup_error_message': 'This is an error for the god of the yedsakjldasd asasjdhas dkjdhad askjdhsd askdjhas dkajsdha kdasjdhas',
        # 'login_error_message': 'This is a error'
    })


# effettua il logout dell'utente che ne fa richiesta
# viene utilizzata la funzione messa a disposizione da django
# alla fine l'utente viene ridirezionato alla pagina di login & signup
def log_out(request):
    print ('Logging out user: \"' + request.user.username + '\"...')
    if request.user.is_authenticated():
        logout(request)
        print ('Logged out')

    return HttpResponseRedirect("/login_signup/")


# carica la dashboard dell'utente loggato
# nella dashboard sono presenti tutte le board tra i cui utenti compare l'utente loggato
# e' anche presente un form per creare nuove board
def dashboard(request):
    if str(request.user) != 'AnonymousUser':        # solito controllo sull'utente autenticato o meno

        personal_boards = Board.objects.all().filter(creator=request.user)    # filtraggio delle board in base all'utente loggato
        owned_boards = Board.objects.all().filter(owners=request.user).exclude(creator=request.user)    # filtraggio delle board in base all'utente loggato
        boards = Board.objects.all().filter(users=request.user).exclude(owners=request.user)     # filtraggio delle board in base all'utente loggato

        board_creation_form = BoardCreationForm()       # form creazione nuove board

        # viene visualizzata la dashboard, viene caricata la
        # lista di boards a cui partecipa l'utente e il form di creazione
        # board vuoto
        return render(request, 'dashboard.html',  {
            'user': request.user,
            'boards': boards,
            'owned_boards': owned_boards,
            'boards_created_by_user': personal_boards,
            'board_creation_form': board_creation_form,
        })
    # se l'utente che cerca di accedere alla pagina non e' autenticato viene
    # rediretto alla pagina di login
    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


# aggiunge una board al database e associa
# automaticamente l'utente che la sta creando ad essa
def add_board(request):
    if str(request.user) != 'AnonymousUser':        # solito controllo
        if request.method == 'POST':
            if request.POST.get('submit') == 'create_board':
                board_form = BoardCreationForm(request.POST)
                # convalida del form e salvataggio
                if board_form.is_valid():
                    board_name = board_form.cleaned_data['board_name']
                    new_board = Board()
                    new_board.name = board_name
                    new_board.n_users = 1
                    # il salvataggio dell aboard avviene prima dell'aggiunta dell'utente attivo
                    # alla lista di utenti della board, perche' facendo al contrario viene
                    # lanciata un'eccezione dal database. A quanto pare deve essere salvata sul database
                    # prima di farla interagire con altri oggetti gia' presenti (nel database)
                    new_board.creator = request.user
                    new_board.save()
                    new_board.owners.add(request.user.id)
                    new_board.users.add(request.user.id)
                    # new_board.save()
                    print('New board created. Name: ' + new_board.name + '. creator: ' + new_board.creator.username)     # log

                    # redirezione alla pagina della board appena creata
                    return HttpResponseRedirect("/board/" + str(new_board.id) + "/")

        board_form = BoardCreationForm()            # non ci vanno i punti e virgola su pyrhon!

        return render(request, 'dashboard.html', {
            'user': request.user,
            'board_creation_form': board_form,
        })

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def add_or_remove_user_to_board(request, board_id, user_id=''):
    if str(request.user) != 'AnonymousUser':
        board_to_modify = Board.objects.get(pk=board_id)

        if request.user in board_to_modify.owners.all():                        # controllo per owner

            if request.method == 'POST':
                if request.POST.get('submit') == 'add_user_request':
                    if user_id is not None:
                        user_to_add = User.objects.get(pk=user_id)
                        print ('Adding user ' + user_to_add.username + ' to board ' + str(board_to_modify.id))

                        if board_to_modify.users.all().filter(pk=user_id).count() <= 0:
                            board_to_modify.users.add(user_to_add)
                            board_to_modify.n_users += 1
                            board_to_modify.save()
                            print ('Added user ' + user_to_add.username + ' to board ' + str(board_to_modify.id))

                elif request.POST.get('submit') == 'delete_user_request':
                    if user_id is not None:
                        user_to_delete = User.objects.get(pk=user_id)
                        print ('Deleting user ' + user_to_delete.username + ' from board ' + str(board_to_modify.id))

                        if board_to_modify.users.all().filter(pk=user_id).count() > 0:
                            board_to_modify.users.remove(user_to_delete)
                            board_to_modify.n_users -= 1
                            board_to_modify.save()
                            print ('Deleted user ' + user_to_delete.username + ' from board ' + str(board_to_modify.id))

                elif request.POST.get('submit') == 'add_user_to_admins_request':
                    if user_id is not None:
                        user_to_make_admin = User.objects.get(pk=user_id)
                        print ('Adding user ' + user_to_make_admin.username + ' as admin to board ' + str(board_to_modify.id))

                        if board_to_modify.owners.all().filter(pk=user_id).count() <= 0:
                            board_to_modify.owners.add(user_to_make_admin)
                            board_to_modify.save()
                            print ('Added user ' + user_to_make_admin.username + 'as admin to board ' + str(board_to_modify.id))

                elif request.POST.get('submit') == 'remove_user_from_admins_request':
                    if user_id is not None:
                        user_to_remove_from_admins = User.objects.get(pk=user_id)
                        print ('Removing user ' + user_to_remove_from_admins.username + ' from admins of board ' + str(board_to_modify.id))

                        if board_to_modify.owners.all().filter(pk=user_id).count() > 0:
                            board_to_modify.owners.remove(user_to_remove_from_admins)
                            board_to_modify.save()
                            print ('Added user ' + user_to_remove_from_admins.username + 'as admin to board ' + str(board_to_modify.id))

        else:   # se l'utente non e' admin
            error_message = 'You do not have enough permissions to add/remove users to/from this board.'
            error_suggestions = [
                'If you just created the board, try to create another one. If problem persists contact us. We apologize for the inconvenience.',
                'If you know other users that can access the board, ask them to add you to admin users.',
                'If you got here \"accidentally\" just go back to your Dashboard.']

            return raise_error_page(request, error_message, error_suggestions)

        search_user_form = SearchUserForm()
        board_name_modification_form = BoardNameModificationForm()
        board_owners = board_to_modify.owners.all()

        return render(request, 'board_user_management.html', {
            'user': request.user,
            'board_to_modify': board_to_modify,
            'board_owners': board_owners,
            'board_name_modification_form': board_name_modification_form,
            'search_user_form': search_user_form,
        })

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def modify_or_delete_board(request, board_id):
    if str(request.user) != 'AnonymousUser':        # solito controllo

        if request.user in Board.objects.get(pk=board_id).owners.all():                        # controllo per owner

            if request.method == 'POST':
                if request.POST.get('submit') == 'change_board_name_request':
                    new_board_name_form = BoardNameModificationForm(request.POST)
                    if new_board_name_form.is_valid():
                        new_board_name = new_board_name_form.cleaned_data['new_board_name']
                        board_to_modify = Board.objects.get(pk=board_id)

                        if board_to_modify.name != new_board_name:
                            board_to_modify.name = new_board_name
                            board_to_modify.save()


                elif request.POST.get('submit') == 'delete_board_request':
                    board_to_delete = Board.objects.get(pk=board_id)
                    if request.user == board_to_delete.creator:
                        board_to_delete.delete()
                    else:
                        error_message = 'You do not have enough permissions to delete this board.'
                        error_suggestions = [
                            'Only the Creator of the board can delete it. If you have created this board, try deleting the cache of the browser and reloading the page, then try again. If problem persists contact us. We apologize for the inconvenience.',
                            '',
                            'If you got here \"accidentally\" just go back to your Dashboard.']

                        return raise_error_page(request, error_message, error_suggestions)

                    return HttpResponseRedirect("/dashboard/")
        else:
            error_message = 'You do not have enough permissions to modify this board.'
            error_suggestions = [
                'If you created the board, try to create another one. If problem persists contact us. We apologize for the inconvenience.',
                'If you know other users that can access the board, ask them to add you as admin user.',
                'If a psychopathic artificial intelligence is trying to kill you, well, stand still, stay calm and scream: \"THIS STATEMENT IS FALSE!\" or \"DOES A SET OF ALL SETS CONTAIN ITSELF?\".',
                'If you got here \"accidentally\" just go back to your Dashboard.']

            return raise_error_page(request, error_message, error_suggestions)

        return HttpResponseRedirect("/board/" + str(board_id) + "/")

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def search_user_board(request):
    if str(request.user) != 'AnonymousUser':

        if request.method == 'POST':
            if request.POST['username_to_search'] != '':
                user_searched = request.POST['username_to_search']
            else:
                user_searched = ''
        else:
            user_searched = ''

        board_to_modify = None

        if user_searched != '':
            search_match_users = User.objects.filter(username__contains=user_searched)
        else:
            search_match_users = []

        found_users_without_access = []
        found_users_with_access = []
        found_owners = []

        if request.POST['board_to_modify'] is not None:
            board_to_modify = Board.objects.get(pk=request.POST['board_to_modify'])

            for user in search_match_users:
                if user != request.user and not user.is_superuser:
                    if user not in board_to_modify.users.all():
                        found_users_without_access.append(user)

            for user in board_to_modify.users.all():
                if user != request.user and not user.is_superuser:
                    if user not in board_to_modify.owners.all():
                        found_users_with_access.append(user)

            for user in board_to_modify.owners.all():
                if user != request.user and not user.is_superuser and user != board_to_modify.creator:
                        found_owners.append(user)

        board_creator = board_to_modify.creator

        return render(request, 'user_search_result-board.html', {
            'user': request.user,
            'board_creator': board_creator,
            'board_owners': found_owners,
            'found_users_without_access': found_users_without_access,
            'found_users_with_access': found_users_with_access,
            'query_text': user_searched,
            'object_to_modify': board_to_modify,
        })

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


# visualizzazione di una board
# l'id della board che si vuole visualizzare viene scritto nell'url
def board_view(request, board_id):
    if str(request.user) != 'AnonymousUser':        # solito controllo sull'utente

        # per intercettare l'eccezione della board non trovata si racchiude l'operazione di ricerca in un blocco try/catch
        try:
            this_board = Board.objects.get(pk=board_id)       # ricerca della board nel database
        except Board.DoesNotExist:
            error_message = 'The board you are trying to access does not exist.'
            error_suggestions = ['If you got here following a link present in your Dashboard, then delete cookies and clean the cache of the browser, reload the page and try again. If problem persists contact us. We apologize for the inconvenience.',
                                 'If you created the board recently, try to create another one. If problem persists contact us. We apologize for the inconvenience.',
                                 'If a psychopathic artificial intelligence is trying to kill you, well, stand still, stay calm and scream: \"THIS STATEMENT IS FALSE!\" or \"DOES A SET OF ALL SETS CONTAIN ITSELF?\".',
                                 'If you got here accidentally just go back to your Dashboard.']

            return raise_error_page(request, error_message, error_suggestions)      # si ridireziona all apagina di errore nel caso venga lanciata una eccezione

        # si esegue una verifica che l'utente sia autorizzato ad accedere alla board richiesta
        is_user_authorized = False
        for board_user in this_board.users.all():
            if board_user == request.user:
                is_user_authorized = True

        if is_user_authorized == False:
            print('Unauthorized access. Redirecting user to unauthorized_access page.')      # log
            error_message = 'You do not have enough permissions to access the requested board.'
            error_suggestions = ['If you created the board, try to create another one. If problem persists contact us. We apologize for the inconvenience.',
                                 'If you know other users that can access the board, ask them to add you to authorized users.',
                                 'If you got here accidentally just go back to your Dashboard.']

            return raise_error_page(request, error_message, error_suggestions)      # solito messaggio di errore

        # per i nuovi utenti viene visualizzato un mini tutorial per la toolbar
        global new_user
        show_tutorial = False
        if new_user is True:
            show_tutorial = True
            new_user = False

        # creazione variabili da caricare nella pagina
        columns = Column.objects.filter(mother_board=board_id)
        cards = []
        for column in columns:
            cards += Card.objects.all().filter(mother_column=column.id)

        new_column_form = ColumnCreationForm()

        new_card_form = CardCreationForm()

        column_name_modification_form = ColumnNameModificationForm()

        board_name_modification_form = BoardNameModificationForm()

        board_owners = Board.objects.get(pk=board_id).owners.all()

        # carica la pagina con la lista di colonne e cards presenti nella board
        return render(request, 'board.html', {
            'user': request.user,
            'board_owners': board_owners,
            'board': this_board,
            'columns': columns,
            'cards': cards,
            'show_tutorial': show_tutorial,
            'new_column_form': new_column_form,
            'new_card_form': new_card_form,
            'column_name_modification_form': column_name_modification_form,
            'board_name_modification_form' : board_name_modification_form,
        })

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


# aggiunge una colonna ad una board
def add_column(request, board_id):
    if str(request.user) != 'AnonymousUser':
        if request.method == 'POST':
            print('New add column POST request')        # log
            if request.POST.get('submit') == 'new_column_create_request':
                new_column_form = ColumnCreationForm(request.POST)

                # se il form e' valido creo la nova colonna associata alla
                # board in cui e' stato compilato il form
                if new_column_form.is_valid():
                    new_column_name = new_column_form.cleaned_data['column_name']

                    # ritorna un oggetto di tipo QuerySet ma occorrsolo un elemento quindi aggiungo [0]
                    new_column_mother_board = Board.objects.all().filter(pk=board_id)[0]

                    # salvataggio della nuova colonna
                    new_column = Column(name=new_column_name, mother_board=new_column_mother_board)
                    new_column.save()

                    # aggiorna il valore del numero di card
                    board = Board.objects.get(pk=board_id)
                    board.n_columns = Column.objects.all().filter(mother_board=board_id).count()
                    board.save()

                    # ricarica la board
                    return HttpResponseRedirect("/board/" + str(board_id) + "/")

                else:
                    print('new column form invalid. Reloading page...')

        return HttpResponseRedirect("/board/" + str(board_id) + "/")

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def modify_or_delete_column(request, column_id, board_id):
    if str(request.user) != 'AnonymousUser':

        if request.method == 'POST':

            if request.POST.get('submit') == 'change_column_name_request':
                new_column_name_form = ColumnNameModificationForm(request.POST)

                if new_column_name_form.is_valid():
                    new_column_name = new_column_name_form.cleaned_data['new_column_name']
                    column_to_modify = Column.objects.get(pk=column_id)

                    # controllo se il nuovo nome e' diverso dal precedente per risparmiare nu accesso al database
                    if column_to_modify.name != new_column_name:
                        column_to_modify.name = new_column_name
                        column_to_modify.save()

                    # ricarica la board
                    # return HttpResponseRedirect("/board/" + str(board_id) + "/")

                else:
                    print('new column form invalid. Reloading page...')

            elif request.POST.get('submit') == 'delete_column_request':
                column_to_delete = Column.objects.get(pk=column_id)
                mother_board = Board.objects.get(pk=column_to_delete.mother_board.id)
                card_in_column = column_to_delete.n_cards

                column_to_delete.delete()

                mother_board.n_columns -= 1
                mother_board.n_cards -= card_in_column
                mother_board.save()

        return HttpResponseRedirect("/board/" + str(board_id) + "/")

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def add_card(request, board_id, column_id):
    if str(request.user) != 'AnonymousUser':
        if request.method == 'POST' and request.POST.get('submit') == 'new_card_create_request':
            new_card_form = CardCreationForm(request.POST)

            # se il orm e' valido creo la nuova card associata alla colonna in cui e' stata compilata
            if new_card_form.is_valid():
                new_card_title = new_card_form.cleaned_data['new_card_title']
                new_card_description = new_card_form.cleaned_data['new_card_description']
                new_card_expire_date = new_card_form.cleaned_data['new_card_expire_date']
                new_card_story_points = new_card_form.cleaned_data['new_card_story_points']

                new_card_moteher_column = Column.objects.all().filter(pk=column_id)[0]


                card = Card(title=new_card_title,
                            description=new_card_description,
                            expire_date=new_card_expire_date,
                            story_points=new_card_story_points,
                            n_users=1,
                            mother_column=new_card_moteher_column)

                card.save()
                card.users.add(request.user)

                # aggiorna il numero di card della colonna
                if new_card_moteher_column.n_cards == 0:
                    n_cards = 0
                    for card in Card.objects.all().filter(mother_column=new_card_moteher_column):
                        n_cards += 1

                    new_card_moteher_column.n_cards = n_cards

                else:
                    board = Board.objects.get(pk=board_id)
                    new_card_moteher_column.n_cards += 1

                new_card_moteher_column.save()

                # aggiorna il numero di card della board
                board = Board.objects.get(pk=board_id)

                if board.n_cards == 0:
                    n_cards = 0
                    for column in Column.objects.all().filter(mother_board=board):
                        n_cards += column.n_cards

                    board.n_cards = n_cards

                else:
                    board.n_cards += 1

                board.save()
                return HttpResponseRedirect("/board/" + str(board_id) + "/")

            else:
                print('new column form invalid. Reloading page...')

        return HttpResponseRedirect("/board/" + str(board_id) + "/")

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def modify_or_delete_card(request, card_id, board_id):
    if str(request.user) != 'AnonymousUser':
        # html = "<html><body>Ssshhhhhh. Trust me, it\'s gone. The ugly card is gone.</body></html>"
        # return HttpResponse(html)
        if request.method == 'POST':

            if request.POST.get('submit') == 'modify_card_request':
                card_to_modify = Card.objects.get(pk=card_id)
                previous_board = Board.objects.get(pk=board_id)

                card_modification_form = CardModificationForm(board_id, card_id)
                search_user_form = SearchUserForm(request.POST or None)

                return render(request, 'modify_card.html', {
                    'user': request.user,
                    'card_to_modify': card_to_modify,
                    'previous_board': previous_board,
                    'search_user_form': search_user_form,
                    'card_modification_form': card_modification_form,
                })

            elif request.POST.get('submit') == 'save_card_changes_request':
                card_to_modify = Card.objects.get(pk=card_id)
                modified_card_form = CardModificationForm(board_id, card_id, request.POST)

                if modified_card_form.is_valid():

                    new_card_title = modified_card_form.cleaned_data['new_card_title']
                    new_card_description = modified_card_form.cleaned_data['new_card_description']
                    new_card_expire_date = modified_card_form.cleaned_data['new_card_expire_date']
                    new_card_story_points = modified_card_form.cleaned_data['new_card_story_points']
                    new_card_mother_column = modified_card_form.cleaned_data['new_card_mother_column']


                    # si eseguono  controlli per risparmiare accessi al database nel caso non ci siano modifiche
                    if card_to_modify.title != new_card_title and new_card_title != '':
                        card_to_modify.title = new_card_title
                        card_to_modify.save()

                    if card_to_modify.description != new_card_description and new_card_description != '':
                        card_to_modify.description = new_card_description
                        card_to_modify.save()

                    if card_to_modify.expire_date != new_card_expire_date:
                        card_to_modify.expire_date = new_card_expire_date
                        card_to_modify.save()

                    if card_to_modify.story_points != new_card_story_points:
                        card_to_modify.story_points = new_card_story_points
                        card_to_modify.save()

                    if str(card_to_modify.mother_column.id) != new_card_mother_column:
                        old_column_mother = Column.objects.get(pk=card_to_modify.mother_column.id)
                        new_column_mother = Column.objects.get(pk=new_card_mother_column)
                        new_column_mother.n_cards += 1
                        old_column_mother.n_cards -= 1
                        new_column_mother.save()
                        old_column_mother.save()
                        card_to_modify.mother_column = Column.objects.get(pk=new_card_mother_column)
                        card_to_modify.save()
                        print('modificando mother column')

                    return HttpResponseRedirect("/board/" + str(board_id) + "/")
                else:
                    print ('not valid aiai')

            elif request.POST.get('submit') == 'delete_card_request':
                card_to_delete = Card.objects.get(pk=card_id)
                mother_column = Column.objects.get(pk=card_to_delete.mother_column.id)
                mother_board = Board.objects.get(pk=mother_column.mother_board.id)
                card_to_delete.delete()
                mother_column.n_cards -= 1
                mother_column.save()
                mother_board.n_cards -= 1
                mother_board.save()

                return HttpResponseRedirect("/board/" + str(board_id) + "/")

        card_to_modify = Card.objects.get(pk=card_id)
        previous_board = Board.objects.get(pk=board_id)

        print ('non ci arriva')
        search_user_form = SearchUserForm(request.POST or None)
        card_modification_form = CardModificationForm(board_id, card_id)

        return render(request, 'modify_card.html', {
            'user': request.user,
            'card_to_modify': card_to_modify,
            'previous_board': previous_board,
            'search_user_form': search_user_form,
            'card_modification_form': card_modification_form,
        })

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def add_or_remove_user_to_card(request, user_id, card_id):
    if str(request.user) != 'AnonymousUser':

        card_to_modify = Card.objects.get(pk=card_id)

        if request.method == 'POST':
            if request.POST.get('submit') == 'add_user_request':
                user_to_add = User.objects.get(pk=user_id)
                print ('Adding user ' + user_to_add.username + ' to card ' + str(card_to_modify.id))

                if card_to_modify.users.all().filter(pk=user_id).count() <= 0:
                    card_to_modify.users.add(user_to_add)
                    card_to_modify.n_users += 1
                    card_to_modify.save()
                    print ('Added user ' + user_to_add.username + ' to card ' + str(card_to_modify.id))

            elif request.POST.get('submit') == 'delete_user_request':
                user_to_delete = User.objects.get(pk=user_id)
                print ('Deleting user ' + user_to_delete.username + ' from card ' + str(card_to_modify.id))

                if card_to_modify.users.all().filter(pk=user_id).count() > 0:
                    card_to_modify.users.remove(user_to_delete)
                    card_to_modify.n_users -= 1
                    card_to_modify.save()
                    print ('Deleted user ' + user_to_delete.username + ' from card ' + str(card_to_modify.id))

        board_id = Board.objects.get(pk=Column.objects.get(pk=card_to_modify.mother_column.id).mother_board.id).id

        return HttpResponseRedirect( "/modify_or_delete_card/" + str(card_id) + '/' + str(board_id) + '/')

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def search_user_card(request):
    if str(request.user) != 'AnonymousUser':

        if request.method == 'POST':
            if request.POST['username_to_search'] != '':
                user_searched = request.POST['username_to_search']
            else:
                user_searched = ''
        else:
            user_searched = ''

        card_to_modify = None

        if user_searched != '':
            search_match_users = User.objects.filter(username__contains=user_searched)
        else:
            search_match_users = []

        found_users_without_access = []
        found_users_with_access = []

        if request.POST['card_to_modify'] is not None:
            card_to_modify = Card.objects.get(pk=request.POST['card_to_modify'])

            for user in search_match_users:
                if user != request.user and not user.is_superuser:
                    if user not in card_to_modify.users.all():
                        found_users_without_access.append(user)

            for user in card_to_modify.users.all():
                if user != request.user and not user.is_superuser:
                    found_users_with_access.append(user)

        return render(request, 'user_search_result-card.html', {
            'found_users_without_access': found_users_without_access,
            'found_users_with_access': found_users_with_access,
            'query_text': user_searched,
            'object_to_modify': card_to_modify,
        })

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")




def raise_error_page(request, error_message, error_suggestions):
    # giusto per sicurezza
    if str(request.user) != 'AnonymousUser':

        return render(request, 'unauthorized_access.html', {
            'user': request.user,
            'error_message': error_message,
            'error_suggestions': error_suggestions,
        })

    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def burndown(request, board_id):
    if str(request.user) != 'AnonymousUser':

        try:
            this_board = Board.objects.get(pk=board_id)
        except Board.DoesNotExist:
            error_message = 'The board you are trying to access does not exist. The burndown can not be retrieved.'
            error_suggestions = ['If you just clicked in burndown button, then try deleting cookies and cleaning the cache of the browser, reload the page and try again. If problem persists contact us. We apologize for the inconvenience.',
                                 'If you just created the board, try waiting a few minutes and try again. If problem persists contact us. We apologize for the inconvenience.',
                                 'If a psychopathic artificial intelligence is trying to kill you, well, stand still, stay calm and scream: \"THIS STATEMENT IS FALSE!\" or \"DOES A SET OF ALL SETS CONTAIN ITSELF?\".']

            return raise_error_page(request, error_message, error_suggestions)

        user_can_access = False
        for user in this_board.users.all():
            if request.user == user:
                user_can_access = True

        if user_can_access == False:
            error_message = 'You do not have enough permission to access the requested board.'
            error_suggestions = [
                'If you just clicked in burndown button, then try deleting cookies and cleaning the cache of the browser, reload the page and try again. We apologize for the inconvenience.',
                'If you know other users that can access the board, ask them to add you to authorized users then try again.',
                'If you got here \"accidentally\" just go back to your Dashboard.']

            return raise_error_page(request, error_message, error_suggestions)

        columns_in_this_board = Column.objects.all().filter(mother_board=board_id)
        cards_in_this_board = []
        for column in columns_in_this_board:
            cards_in_this_board += Card.objects.all().filter(mother_column=column.id)

        # calcolo delle statistiche
        tot_story_points = 0
        tot_expired_cards = 0

        for card in cards_in_this_board:
            tot_story_points += card.story_points
            if card.expire_date < datetime.date.today():
                tot_expired_cards += 1

        return render(request, 'burndown.html', {
            'user': request.user,
            'board_to_modify': this_board,
            'columns': columns_in_this_board,
            'tot_story_points': tot_story_points,
            'tot_expired_cards': tot_expired_cards,
        })


    else:
        this_function_name = sys._getframe().f_code.co_name
        print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")

    # if str(request.user) != 'AnonymousUser':
    # #     blabla
    #     pass
    # else:
    #     this_function_name = sys._getframe().f_code.co_name
    #     print('(' + this_function_name + ') ' + 'Unauthorized access. Redirecting user to login page')
    #     return HttpResponseRedirect("/login_signup/")
