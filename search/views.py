from django.shortcuts import render
from documents.models import File
from django.http import JsonResponse
from django.conf import settings
from BuscaSemantica.openIAService import OpenIAService

def search(request):
    if not request.user.is_authenticated:
        return render(request, "BuscaSemantica/about.html")

    if request.POST:
        results = {}
        try:
            items = []
            text = request.POST.get('text',None)
            dataFrame = OpenIAService().search(text)
            for index, row in dataFrame.iterrows():
                if (dataFrame['similarities'][index] >= settings.DF_ACCURACY):
                    json_instance = File.objects.get(id = row['id']).to_json()
                    json_instance['type'] = row['type']
                    json_instance['similarity'] = dataFrame['similarities'][index]
                    json_instance['text'] = row['text']
                    items.append(json_instance)
            results['items'] = items
        except Exception as a:
            results['error'] = str(a)
        return JsonResponse(results)
    return render(request, 'search/search.html' )