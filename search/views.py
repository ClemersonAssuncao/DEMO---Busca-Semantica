from django.shortcuts import render
from documents.models import File
from django.http import JsonResponse
from django.conf import settings
from BuscaSemantica.openIAService import OpenIAService

def search(request):
    if not request.user.is_authenticated:
        return render(request, "BuscaSemantica/about.html")

    if request.POST:
        text = request.POST.get('text',None)
        dataFrame = OpenIAService().search(text)
        for register in dataFrame['id'].values:
            print(register)
        return JsonResponse({'finding...': text})
        # df = pd.read_csv(settings.DF_FILE_NAME)
        # df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)
        # new_df = OpenIAService().search(text, df)
        # print(new_df.drop_duplicates(subset=['file_name'], keep='first'))

    return render(request, 'search/search.html', {'files' : File.objects.all()})