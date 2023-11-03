from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from .forms import FileForm, FolderForm
from rest_framework.decorators import api_view
from django.http import JsonResponse
from BuscaSemantica.openIAService import OpenIAService
from asgiref.sync import sync_to_async
# Create your views here.

@login_required(redirect_field_name="users:login")
def document_list(request):
    metadata = {
        'columns': File.getColumnsToGrid(),
        'content': File.objects.all()
    }
    return render(request, 'documents/list.html', {'metadata' : metadata,'formFolder': FolderForm(),'folders': Folder.create_folder_tree(), 'folders_list' : Folder.objects.all()})


@login_required(redirect_field_name="users:login")
def document_add_edit(request, pk = None):
    if request.POST or request.FILES:
        if (pk is None):
            form = FileForm(data = request.POST)
        else: 
            documentModel = get_object_or_404(File, pk=pk)
            form = FileForm(data = request.POST, instance= documentModel)
        if (form.is_valid()):
            document = form.save(commit=False)
            filepath = request.FILES.get('file', False)
            if (filepath):
                document.file = filepath
                print(filepath)
            document.user_created = request.user
            document.save()
            OpenIAService().appendInstance(document )
            return JsonResponse({'saved': True})
    else:
        if (pk is None):
            form = FileForm()
            setattr(form, 'form_url', '/documents/add/')
            setattr(form, 'form_title', 'Adicionar documento ')
        else:
            documentModel = get_object_or_404(File, pk=pk)
            form = FileForm(instance = documentModel)
            setattr(form, 'form_url', f'/documents/edit/{pk}')
            setattr(form, 'form_title', 'Editar documento ')
    return render(request, "documents/add_edit.html", {"form": form, 'folders': Folder.create_folder_tree(), 'folders_list' : Folder.objects.all()})   

@login_required()
@api_view(('POST',))
def folder_add_edit(request, pk = None):

    folder, created = Folder.objects.get_or_create(id=pk)
    folder.name = request.POST.get('name','')
    try:
        folder.id_parent_dir =  Folder.objects.get(id=request.POST.get('id_parent_dir', None))
    except Folder.DoesNotExist:
        pass
    
    folder.save()
    return JsonResponse({'created': created, 'id': folder.id})

@login_required()
@api_view(('POST',))
def delete_folder(request, pk = None):

    folder =  get_object_or_404(Folder, pk=pk)
    folder.delete()
    return JsonResponse({'deleted': True})

@login_required()
@api_view(('POST',))
def document_delete(request, pk = None):

    file =  get_object_or_404(File, pk=pk)
    OpenIAService().deleteInstance(file)
    file.delete()

    return redirect("documents:list" )

