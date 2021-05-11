from django import forms
from apps.core.models import CsvFile


class UploadCsvForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label="Nome")
    file = forms.FileField(label="Arquivo")

    class Meta:
        model = CsvFile
        fields = '__all__'
