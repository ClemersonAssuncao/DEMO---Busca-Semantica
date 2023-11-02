from django.contrib import admin
from .models import Folder, File

# Register your models here.
@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass