from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Folder(models.Model):
    id = models.AutoField(verbose_name="PK", primary_key=True, auto_created=True)
    name = models.CharField(verbose_name='Nome', max_length=50)
    id_parent_dir = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def create_folder_tree():
        
        def get_child(parent):
            children = Folder.objects.all().filter(id_parent_dir=parent['id'])
            for child in children:
                if ('children' not in parent):
                    parent['children'] = []
                parent['children'].append(get_child({'id': child.id, 'name': child.name}))
                
            return parent
        directories = Folder.objects.all().filter(id_parent_dir=None)
        dirTree = []
        for dir in directories:
            dirTree.append(get_child({'id': dir.id, 'name': dir.name}))
        
        return dirTree

class File(models.Model):

    id = models.AutoField(verbose_name="PK", primary_key=True, auto_created=True)
    name = models.CharField(verbose_name='Nome', max_length=255)
    file = models.FileField(verbose_name='file')
    description = models.TextField(verbose_name='Descrição', max_length=255)
    id_folder = models.ForeignKey(Folder, on_delete=models.PROTECT)

    # Audit
    dt_created = models.DateTimeField(verbose_name='Data de criação', auto_now_add=True, null=True)
    dt_updated = models.DateTimeField(verbose_name='Data de atualização', auto_now=True, null=True)
    user_created = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Criado por: ', related_name='usuario_criacao', null=True)
    user_updated = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Atualizado por: ', related_name='usuario_atualizacao', null=True)
    
    def __str__(self):
        return self.name
    
    def getColumnsToGrid():
        fields = ['id','name', 'description', 'id_folder']
        newList =[]
        for genObject in ((x) for x in File._meta.get_fields() if x.attname in fields):
            newList.append({'attname': genObject.attname, 'verbose_name': genObject.verbose_name})
        return newList