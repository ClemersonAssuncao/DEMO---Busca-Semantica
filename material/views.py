from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from search import tests  
from django.urls import reverse
from .models import Folder, File
from .forms import FileForm


def material_list(request):
    metadata = {
        'columns': File.getColumnsToGrid(),
        'content': File.objects.all()
    }
    return render(request, 'documents/list.html', {'metadata' : metadata, 'dc_tree': Folder.create_folder_tree()})

def material_list(request):
    metadata = {
        'columns': File.getColumnsToGrid(),
        'content': File.objects.all()
    }
    return render(request, 'material/material_list.html', {'metadata' : metadata, 'dc_tree': Folder.create_folder_tree()})

def material_add(request):
    if request.POST or request.FILES:
        form = FileForm(data = request.POST)
        if (form.is_valid()):
            material = form.save(commit=False)
            filepath = request.FILES.get('file', False)
            if (filepath):
                material.file = filepath
            material.user_created = request.user
            material.save()
            return redirect("material:material_edit", pk = material.id )
    else:
        form = FileForm()

    setattr(form, 'url_save', 'material_add')
    return render(request, "material/material_register.html", {"form": form, 'dc_tree': Folder.create_folder_tree()})   

def material_edit(request, pk):
    if not pk:
        return HttpResponseRedirect(reverse("material:material_add"))
    
    material = get_object_or_404(File,pk=pk)
    
    if request.POST or request.FILES:
        form = FileForm(data = request.POST, instance=material)
        if (form.is_valid()):
            material = form.save(commit=False)
            filepath = request.FILES.get('file', False)
            if (filepath):
                material.file = filepath
            material.user_updated = request.user
            material.save()
            return redirect("material:material_edit", pk = material.id )
        
    form = FileForm(instance=material)
    setattr(form, 'url_save', 'material_edit')
    return render(request, "material/material_register.html", {"form": form, 'dc_tree': Folder.create_folder_tree()})

