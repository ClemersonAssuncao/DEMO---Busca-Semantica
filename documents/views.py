from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from .forms import FileForm, FolderForm
from rest_framework.decorators import api_view
from django.http import JsonResponse
from BuscaSemantica.openIAService import OpenIAService
from django.db.models.deletion import ProtectedError
import os


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
        result = {
            'saved': False
        }
        if (pk is None):
            form = FileForm(data = request.POST)
        else: 
            documentModel = get_object_or_404(File, pk=pk)
            form = FileForm(data = request.POST, instance= documentModel)
        if (form.is_valid()):
            try:
                document = form.save(commit=False)
                if (request.POST.get('delete_file') == 'true'):
                    if document.file:
                        if os.path.isfile(document.file.path):
                            os.remove(document.file.path)
                            document.file = None

                filepath = request.FILES.get('file', False)
                if (filepath):
                    if (not filepath.name.upper().endswith('PDF')):
                        result['error'] = 'O arquivo não é um PDF.'
                        return JsonResponse(result)
                    document.file = filepath

                if (document.pk):
                    document.user_updated = request.user
                else:
                    document.user_created = request.user
                document.save()
                OpenIAService().appendInstance(document)
                if (filepath):
                    OpenIAService().appendFile(document)
                result['saved'] = True
            except Exception as a:
                result['error'] = str(a)
            return JsonResponse(result)
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
        folder.id_parent_dir = None
    folder.save()
    return JsonResponse({'created': created, 'id': folder.id, 'name': folder.name, 'id_parent_dir': request.POST.get('id_parent_dir', None)})

@login_required()
@api_view(('POST',))
def delete_folder(request, pk = None):
    error = []
    try:
        folder =  get_object_or_404(Folder, pk=pk)
        folder.delete()
        return JsonResponse({'deleted': True})
    except ProtectedError as e:
        for files in e.protected_objects:
            error.append({
                'id': files.id,
                'name': files.name
            })
        return JsonResponse({'deleted': False, 'error': error})

@login_required()
@api_view(('POST',))
def document_delete(request, pk = None):
    file =  get_object_or_404(File, pk=pk)
    OpenIAService().deleteInstance(file)
    file.delete()
    return redirect("documents:list" )

