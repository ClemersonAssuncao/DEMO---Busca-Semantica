from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Folder, File

# Create your views here.

@login_required(redirect_field_name="users:login")
def document_list(request):
    metadata = {
        'columns': File.getColumnsToGrid(),
        'content': File.objects.all()
    }
    return render(request, 'documents/list.html', {'metadata' : metadata,'folders': Folder.create_folder_tree()})
# {'metadata' : metadata, 'dc_tree': Folder.create_folder_tree()}