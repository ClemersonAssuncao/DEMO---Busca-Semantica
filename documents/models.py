from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.fields.files import FieldFile
import os


# Create your models here.
class Folder(models.Model):
    id = models.AutoField(verbose_name="Sequência", primary_key=True, auto_created=True)
    name = models.CharField(verbose_name='Nome', max_length=50)
    id_parent_dir = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def create_folder_tree():
        
        def get_child(parent):
            children = Folder.objects.all().filter(id_parent_dir=parent['id'])
            for child in children:
                if ('children' not in parent):
                    parent['children'] = []
                parent['children'].append(get_child({'id': child.id, 'name': child.name, 'parent': parent['id']}))
                
            return parent
        directories = Folder.objects.all().filter(id_parent_dir=None)
        dirTree = []
        for dir in directories:
            dirTree.append(get_child({'id': dir.id, 'name': dir.name, 'parent': None}))
        
        return dirTree

class File(models.Model):
    
    def file_directory_path(instance, filename):

        return f"{instance.user_created}/{filename}"

    id = models.AutoField(verbose_name="Seq.", primary_key=True, auto_created=True)
    name = models.CharField(verbose_name='Nome', max_length=255)
    file = models.FileField(verbose_name='Arquivo', upload_to=file_directory_path)
    description = models.TextField(verbose_name='Descrição', max_length=255)
    id_folder = models.ForeignKey(Folder, on_delete=models.PROTECT, verbose_name='Pasta', related_name='pasta')

    # Audit
    dt_created = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True, null=True)
    dt_updated = models.DateTimeField(verbose_name='Data de atualização', auto_now=True, null=True)
    user_created = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Criado por: ', related_name='usuario_criacao', null=True)
    user_updated = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Atualizado por: ', related_name='usuario_atualizacao', null=True)
    
    def __str__(self):
        return self.name
    
    def filename(self):
        if not self.file or not os.path.isfile(self.file.path):
            return None
        return os.path.basename(self.file.name)
    
    def getColumnsToGrid():
        fields = ['id','name', 'description', 'id_folder', 'file']
        newList = [ {'attname': column, 'verbose_name': str(getattr(File,column).field._verbose_name)} for column in fields if hasattr(File, column)]
        return newList
    
    def to_json(self):
        fields = ['id','name', 'description', 'id_folder', 'file', 'dt_created', 'user_created']
        data = {}
        for column in fields:
            if hasattr(File, column):
                value = getattr(self,column)
                if (isinstance(value, Folder)):
                    data[column] = value.name
                elif (isinstance(value, FieldFile)):
                    data[column] = value.name
                elif (isinstance(value, User)):
                    data[column] = value.username
                else:
                    data[column] = value
        return data
    
        
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk :
        return False
    
    old_instance = File.objects.get(pk=instance.pk)

    if not old_instance.file:
        return False
    
    if not old_instance.file == instance.file:
        if os.path.isfile(old_instance.file.path):
            os.remove(old_instance.file.path)