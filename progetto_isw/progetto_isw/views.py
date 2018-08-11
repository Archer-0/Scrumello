from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from forms import *


# about page
def about(request):
    return render(request, 'about.html')


# se
def login_signup(request):
    # logica login e registrazione
    return render(request, 'login_signup.html')
