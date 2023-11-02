from django import forms
from .models import Folder, File

class FolderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FolderForm, self).__init__(*args, **kwargs)
        self.fields['id_parent_dir'].queryset = Folder.objects.exclude(id=self.instance.pk)

    id = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Nome', max_length=255)
    id_parent_dir = forms.ModelChoiceField(queryset=Folder.objects.all())

    class Meta:
        model = Folder
        exclude = []

class FileForm(forms.ModelForm ):
    id = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Nome', max_length=255)
    description = forms.CharField(label='Descrição', max_length=255, widget= forms.Textarea())
    file = forms.FileField(label='Arquivo', required=False)
    id_folder = forms.ModelChoiceField(queryset=Folder.objects.all())


    class Meta:
        model = File
        exclude = ['dt_created', 'dt_updated', 'user_created', 'user_updated']
