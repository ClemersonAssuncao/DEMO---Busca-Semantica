from django.shortcuts import render
from django.http import HttpResponseForbidden
from search import tests  
from .models import Folder, File
from .forms import FileForm


# Create your views here.
def material_list(request):
    metadata = {
        'columns': File.getColumnsToGrid(),
        'content': File.objects.all()
    }
    print(metadata['content'])
    print('----')
    print(metadata['columns'])
    return render(request, 'material/material_list.html', {'metadata' : metadata, 'dc_tree': Folder.create_folder_tree()})

def material_add(request):
    form = FileForm()
    if request.POST or request.FILES:
        form = FileForm(data = request.POST, files = request.FILES)
        if (form.is_valid()):
            form.instance.user_created = request.user
            form.save()
    setattr(form, 'url_save', 'material_add')
    return render(request, "material/material_register.html", {"form": form, 'dc_tree': Folder.create_folder_tree()})   

# Create your views here.
def material_edit(request, pk):
    file = File.objects.get(id=pk)
    if request.POST and request.FILES:
        form = FileForm(data = request.POST, files = request.FILES)
        if (form.is_valid()):
            form.instance.user_updated = request.user
            form.save()
    else:
        form = FileForm(instance=file)
    setattr(form, 'url_save', 'material_edit')
    return render(request, "material/material_register.html", {"form": form, 'dc_tree': Folder.create_folder_tree()})

