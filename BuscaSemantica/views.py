from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from search import tests  
from django.urls import reverse

def about(request):
    return render(request, "BuscaSemantica/about.html")

def controll(request):
    return render(request, "BuscaSemantica/controll.html")

def reset_password(request, uid, token):
    print(uid)
    print(token)
    return render(request, 'users/password_confirm.html')

