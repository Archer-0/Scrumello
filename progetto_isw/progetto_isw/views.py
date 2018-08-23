# coding=utf-8
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

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
        print('User \"' + request.user.username + '\" already authenticated.')
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
        if request.user:
            boards = Board.objects.all().filter(users=request.user)     # filtraggio delle board in base all'utente loggato

        board_creation_form = BoardCreationForm()       # form creazione nuove board

        # return render(request, 'dashboard.html', {
        #     'user': request.user,
        #     'message': 'Hey ' + request.user.username + ', all is working',
        #     'board_creation_form': board_creation_form,
        # })

        # viene visualizzata la dashboard, viene caricata la
        # lista di boards a cui partecipa l'utente e il form di creazione
        # board vuoto
        return render(request, 'dashboard.html',  {
            'user': request.user,
            'boards': boards,
            'board_creation_form': board_creation_form,
        })
    # se l'utente che cerca di accedere alla pagina non e' autenticato viene
    # rediretto alla pagina di login
    else:
        print('Unauthorized access. Redirecting user to login page')    # log
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
                    new_board.save()
                    new_board.users.add(request.user.id)
                    print('New board created. Name: ' + new_board.name)     # log

                    # redirezione alla pagina della board appena creata
                    return HttpResponseRedirect("/board/" + str(new_board.id) + "/")
        else:
            board_form = BoardCreationForm();

        return render(request, 'dashboard.html', {
            'user': request.user,
            'message': 'Hey ' + request.user.username + ', all is working',
            'board_creation_form': board_form,
        })

    else:
        print('Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


# visualizzazione di una board
# l'id della board che si vuole visualizzare viene scritto nell'url
def board_view(request, board_id):
    if str(request.user) != 'AnonymousUser':        # solito controllo sull'utente

        # per intercettare l'eccezione della board non trovata si racchiude l'operazione di ricerca in un blocco try/catch
        try:
            board = Board.objects.get(pk=board_id)       # ricerca della board nel database
        except Board.DoesNotExist:
            error_message = 'The board you are trying to access does not exist.'
            error_suggestions = ['If you got here following a link present in your Dashboard, then delete cookies and clean the cache of the browser, reload the page and try again. If problem persists contact us. We apologize for the inconvenience.',
                                 'If you created the board recently, try to create another one. If problem persists contact us. We apologize for the inconvenience.',
                                 'If a psychopathic artificial intelligence is trying to kill you, well, stand still, stay calm and scream: \"THIS STATEMENT IS FALSE!\" or \"DOES A SET OF ALL SETS CONTAIN ITSELF?\".',
                                 'If you got here accidentally just go back to your Dashboard.']

            return raise_error_page(request, error_message, error_suggestions)      # si ridireziona all apagina di errore nel caso venga lanciata una eccezione

        # si esegue una verifica che l'utente sia autorizzato ad accedere alla board richiesta
        is_user_authorized = False
        for board_user in board.users.all():
            if board_user == request.user:
                is_user_authorized = True

        if is_user_authorized == False:
            print('Unauthorized access. Redirecting user to unauthorized_access page.')      # log
            error_message = 'You do not have sufficient permission to access the requested board.'
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

        # carica la pagina con la lista di colonne e cards presenti nella board
        return render(request, 'board.html', {
            'user': request.user,
            'board': board,
            'columns': columns,
            'cards': cards,
            'show_tutorial': show_tutorial,
            'new_column_form': new_column_form,
        })

    else:
        print('Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


# aggiunge una colonna ad una board
def add_column(request, board_id):
    if str(request.user) != 'AnonymousUser':
        if request.method == 'POST':
            print('New add column POST request')        # log
            if (request.POST.get('submit') == 'new_column_create_request'):
                new_column_form = ColumnCreationForm(request.POST)

                # se il form e' valido creo la nova colonna associata alla
                # board in cui e' stato compilato il form
                if new_column_form.is_valid():
                    new_column_name = new_column_form.cleaned_data['column_name'];

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
        print('Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def add_card(request, board_id):
    return None


def raise_error_page(request, error_message, error_suggestions):

    return render(request, 'unauthorized_access.html', {
        'user': request.user,
        'error_message': error_message,
        'error_suggestions': error_suggestions,
    })


    # if str(request.user) != 'AnonymousUser':
    # #     blabla
    # else:
    #     print('Unauthorized access. Redirecting user to login page')
    #     return HttpResponseRedirect("/login_signup/")