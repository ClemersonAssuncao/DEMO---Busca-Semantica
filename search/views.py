from django.shortcuts import render
from . import tests 
# Create your views here.

def search(request):

    if not request.user.is_authenticated:
        return render(request, "BuscaSemantica/about.html")

    return render(request, 'search/search.html', {'list' : tests.getTestData()})

def index(request):

    if not request.user.is_authenticated:
        return render(request, "BuscaSemantica/about.html")

    return render(request, 'search/index.html', {'list' : tests.getTestData()})