from django import forms
from .models import Folder, File


class FileForm(forms.ModelForm ):
    id = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Nome', max_length=255)
    description = forms.CharField(label='Descrição', max_length=255, widget= forms.Textarea())
    file = forms.FileField(label='Arquivo', required=False)
    id_folder = forms.ModelChoiceField(queryset=Folder.objects.all())


    class Meta:
        model = File
        exclude = ['dt_created', 'dt_updated', 'user_created', 'user_updated']


    # dt_updated = models.DateTimeField(verbose_name='Data de atualização', auto_now=True)
    # user_created = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Criado por: ', related_name='usuario_criacao')
    # user_updated = models.ForeignKey(User, on_delete= models.CASCADE, verbose_name='Atualizado por: ', related_name='usuario_atualizacao')
    # id_folder = models.ForeignKey(Folder, on_delete=models.PROTECT)