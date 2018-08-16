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
    return render(request, 'about.html')


# login_signup page
def login_signup(request):
    # se l'utente e' gia' loggato
    if str(request.user) != 'AnonymousUser':
        print('User \"' + request.user.username + '\" already authenticated.')
        return HttpResponseRedirect("/dashboard/", {
            "user": request.user,
        })

    # se e' stata effettuata una richiesta POST
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        login_form = LoginForm(request.POST)

        if request.POST.get('submit') == 'log_in':
            print ('submit value = ' + str(request.POST.get('submit')))     # log
            if login_form.is_valid():
                print ('login form is valid')
                username = login_form.cleaned_data['login_username']
                password = login_form.cleaned_data['login_password']

                # autenticazione dell'utente
                user = authenticate(username=username, password=password)
                # se l'utente esiste ed user.is_active == true
                if user is not None:
                    # se l'utente e' attivo si effettua il login e lo si ridireziona alla dashboard
                    if user.is_active:
                        login(request, user)
                        global new_user
                        new_user = False
                        return HttpResponseRedirect("/dashboard/", {
                            "user": user,
                        })
                    # se l'utente non e' attivo vuol dire che e' stato bloccato e si stampa un messaggio di errore
                    else:
                        error_message = 'The user \"' + login_form.cleaned_data['login_username'] + '\" has been banned.'
                        return render(request, "login_signup.html", {
                            "login_form": login_form, "signup_form": signup_form, 'login_error_message': error_message
                        })
                # se l'utente non esiste si stampa un messaggio di errore
                else:
                    error_message = 'Wrong username or password. Try again!'
                    return render(request, "login_signup.html", {
                        "login_form": login_form, "signup_form": signup_form, 'login_error_message': error_message
                    })

        # se viene fatto il submit del form di registrazione
        # "submit" e' l'attributo "name" del button del form
        elif request.POST.get('submit') == 'sign_up' and signup_form.is_valid():
            # creazione nuovo utente
            user = User()
            user_tmp = User.objects.all().filter(username=signup_form.cleaned_data['signup_username'])

            if user_tmp.__len__() > 0:
                error_message = 'The user \"' + signup_form.cleaned_data['signup_username'] + '\" already exists. Did you want to login instead?'
                signup_form.fields['signup_username'].widget.attrs['class'] = 'forms_field-input form-error-outline'
                return render(request, "login_signup.html", {
                    'login_form': login_form, 'signup_form': signup_form, 'form_class': 'signup-click', "signup_error_message": error_message
                })

            if signup_form.cleaned_data['signup_password'] == signup_form.cleaned_data['signup_password_confirm']:
                user.username = signup_form.cleaned_data['signup_username']
                user.set_password(signup_form.cleaned_data['signup_password'])
                user.save()
                login(request, user)
                print('new user registered')
                global new_user
                new_user = True
                return HttpResponseRedirect("/dashboard/")
            else:
                error_message = "Passwords do not match"
                signup_form.fields['signup_password_confirm'].widget.attrs['class'] = 'forms_field-input form-error-outline'
                return render(request, "login_signup.html", {
                    'login_form': login_form, 'signup_form': signup_form, 'form_class': 'signup-click', "signup_error_message": error_message
                })

    # se non e' stata effettuata nessuna richiesta POST
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


def log_out(request):
    print ('Logging out user: \"' + request.user.username + '\"...')
    if request.user.is_authenticated():
        logout(request)
        print ('Logged out')

    return HttpResponseRedirect("/login_signup/")


def dashboard(request):
    if str(request.user) != 'AnonymousUser':
        if request.user :
            boards = Board.objects.all().filter(users=request.user)

        if new_user is True:
            return render(request, 'dashboard.html', {
                'user': request.user,
                'message': 'Hey ' + request.user.username + ', all is working like a fuckin\' charm. Yeah! \\m/',
            })
        else:
            return render(request, 'dashboard.html', {
                'user': request.user,
                'message': 'Hey ' + request.user.username + ', all is working like a fuckin\' charm. Yeah! \\m/',
            })
    else:
        print('Unauthorized access. Redirecting user to login page')
        return HttpResponseRedirect("/login_signup/")


def add_board(request):
    return render(request, 'add_board_form.html', {
        'name': request.name,
    })
