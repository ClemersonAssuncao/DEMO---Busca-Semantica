from django.shortcuts import render
from . import tests
import pandas as pd
import numpy as np
from documents.models import File
from django.conf import settings
from BuscaSemantica.openIAService import OpenIAService

def search(request):
    if not request.user.is_authenticated:
        return render(request, "BuscaSemantica/about.html")

    if request.POST:
        files =  File.objects.all()
        # df = pd.read_csv(settings.DF_FILE_NAME)
        # df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)
        # new_df = OpenIAService().search(text, df)
        # print(new_df.drop_duplicates(subset=['file_name'], keep='first'))

    return render(request, 'search/search.html', {'files' : File.objects.all()})

def index(request):

    if not request.user.is_authenticated:
        return render(request, "BuscaSemantica/about.html")

    return render(request, 'search/index.html', {'list' : tests.getTestData()})