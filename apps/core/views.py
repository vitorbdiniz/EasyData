from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import UploadCsvForm

from apps.core.services import data_conversion
from apps.core.services.statistics import *

from apps.core.services.graphics import *

@login_required(login_url='login')
def dashboard(request):
    arquivos = CsvFile.objects.filter(user=request.user)

    arquivo0 = arquivos[3].file
    # print(arquivo0)
    dataframe = data_conversion.csv_to_df(arquivo0)
    # print(dir(statistics))
    # stats = outliers_df(csv)

    media = mean(dataframe)
    mediana = median(dataframe)
    # moda = mode(dataframe)
    variancia = variance(dataframe)
    desvio = standard_deviation(dataframe)
    
    boxplot = boxplot_completo(dataframe).to_html()
    histogram = histograma_completo(dataframe).to_html()
    heatmap = correlation_heatmap(dataframe).to_html()

    colunas = list(dataframe.columns)

    if request.method == "POST":
        colunas_enviadas = request.POST.dict()
        coluna1 = colunas_enviadas['coluna1']
        coluna2 = colunas_enviadas['coluna2']
    else:
        coluna1 = list(dataframe.columns)[0]
        coluna2 = list(dataframe.columns)[1]
    scatter = scatter_plot(dataframe, coluna1, coluna2).to_html()

    context = {
        'form': UploadCsvForm(),
        'files': arquivos,
        'boxplot': boxplot,
        'histogram': histogram,
        'heatmap': heatmap,
        'scatter': scatter,
        'mean': dict(media),
        'median': dict(mediana),
        # 'mode': dict(moda),
        'variance': dict(variancia),
        'std': dict(desvio),
        'columns': colunas,

    }
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
