# coding=utf-8
import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from forms import *

welcomeTexts = ['pandas 🐼!', 'cookies!', 'RGB!', 'the force!', 'ice cream!', 'cmd.exe', 'sudo makeprrr🐱']


# about page
def about(request):
    return render(request, 'about.html')


# login_signup page
def login_signup(request):
    # se e' stata effettuata una richiesta POST
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        signup_form = SignupForm(request.POST)
        if request.POST.get('submit') == 'log_in' and login_form.is_valid():
            username = login_form.cleaned_data['login_username']
            password = login_form.cleaned_data['login_password']

            # autenticazione dell'utente
            user = authenticate(username=username, password=password)

            # se l'utente e' esiste gia' si effettua il login e lo si ridireziona al dashboard
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponseRedirect("/dashboard/")
                    return HttpResponseRedirect("/login_signup/")
                else:
                    return render(request, "login_signup.html", {
                        "login_form": login_form, "signup_form": signup_form,
                    })

            else:
                return render(request, "login_signup.html", {
                    "login_form": login_form, "signup_form": signup_form,
                })

        # se viene fatto il submit del form di registrazione
        elif request.POST.get('submit') == 'sign_up' and signup_form.is_valid():
            # creazione nuovo utente
            user = User()
            user_tmp = User.objects.all().filter(username=signup_form.cleaned_data['signup_username'])
            if user_tmp.__len__() > 0:
                error_message = "The user %s already exists. Do you want to login instead?", signup_form.cleaned_data['signup_username']
                return render(request, "login_signup.html", {
                    'login_form': login_form, 'signup_form': signup_form, "error_message": error_message
                })
            if signup_form.cleaned_data['signup_password'] == signup_form.cleaned_data['signup_password_confirm']:
                user.username = signup_form.cleaned_data['signup_username']
                user.set_password(signup_form.cleaned_data['signup_password'])
                user.save()
                login(request, user)
                return HttpResponseRedirect("/dashboard/")
            else:
                error_message = "Passwords do not match"
                return render(request, "login_signup.html", {
                    'login_form': login_form, 'signup_form': signup_form, "signup_error_message": error_message
                })

    # se non e' stata effettuata nessuna richiesta POST
    else:
        login_form = LoginForm()
        signup_form = SignupForm()

    return render(request, 'login_signup.html', {
        'login_form': login_form,
        'signup_form': signup_form,
        'welcomeText': welcomeTexts[random.randrange(0, len(welcomeTexts))],
        # 'signup_error_message': 'This is an error for the god of the yedsakjldasd asasjdhas dkjdhad askjdhsd askdjhas dkajsdha kdasjdhas kdjashd akdjhasd kasjdh askdjahd askjdhas kdjashd kjasdhas kjdhad as',
        # 'login_error_message': 'This is an error'
    })