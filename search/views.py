from django.shortcuts import render
from . import tests 
# Create your views here.
def search_index(request):

    return render(request, 'search/index.html', {'list' : tests.getTestData()})