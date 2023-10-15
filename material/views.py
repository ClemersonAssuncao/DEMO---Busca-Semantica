from django.shortcuts import render
from search import tests  

# Create your views here.
def material_list(request):
    return render(request, 'material/material_list.html', {'list' : tests.getTestData(), 'dc_tree': tests.getTestTree()})

# Create your views here.
def material_register(request, pk):
    return render(request, 'material/material_register.html', {'pk': pk, 'dc_tree': tests.getTestTree()})