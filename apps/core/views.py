from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import UploadCsvForm

from apps.core.services import data_conversion, statistics

@login_required(login_url='login')
def dashboard(request):
    arquivos = CsvFile.objects.filter(user=request.user)

    arquivo0 = arquivos[2].file
    csv = data_conversion.csv_to_df(arquivo0)
    media = statistics.outliers_df(csv)

    print(media)

    context = {'form': UploadCsvForm(), 'files': arquivos}
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def upload(request):
    if request.method == "POST":
        CsvFile.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            file=request.FILES['file'])
        messages.success(request, "Arquivo enviado com sucesso!")
        return HttpResponseRedirect('/upload')
    else:
        context = {'form': UploadCsvForm()}
        return render(request, 'upload.html', context)

@login_required(login_url='login')
def statistics(request):
    return render(request, 'statistics.html')
