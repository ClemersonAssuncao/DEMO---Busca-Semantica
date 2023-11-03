from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from search import tests  
from django.urls import reverse

def about(request):
    return render(request, "BuscaSemantica/about.html")

def controll(request):
    return render(request, "BuscaSemantica/controll.html")

