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
    import datetime
    from django.utils.timezone import now
    one_hour_ago = now() + datetime.timedelta(minutes=-1200)
    arquivos = CsvFile.objects.filter(user=request.user, created_at__gte=one_hour_ago)

    context = {
        'form': UploadCsvForm(),
        'files': arquivos,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def statistics(request, file_id):
    arquivo = CsvFile.objects.get(user=request.user, id=file_id)
    dataframe = data_conversion.csv_to_df(arquivo.file, sep=";")

    if request.method == "POST":
        colunas_enviadas = request.POST.dict()
        arquivo = colunas_enviadas['arquivo']
    else:
        arquivo = None

    if request.method == "POST":
        colunas_enviadas = request.POST.dict()
        coluna1 = colunas_enviadas['coluna1']
        coluna2 = colunas_enviadas['coluna2']
    else:
        print(list(dataframe.columns))
        coluna1 = list(dataframe.columns)[0]
        coluna2 = list(dataframe.columns)[1]
    
    # print(dir(statistics))
    # stats = outliers_df(csv)
    print(dataframe)

    media = mean(dataframe)
    mediana = median(dataframe)
    moda = mode(dataframe)
    variancia = variance(dataframe)
    desvio = standard_deviation(dataframe)
    
    boxplot = boxplot_completo(dataframe).to_html()
    histogram = histograma_completo(dataframe).to_html()
    heatmap = correlation_heatmap(dataframe).to_html()

    cabecalhos = dataframe.select_dtypes(include=np.number).columns.tolist()
    # print(dataframe.columns)
    # cabecalhos = get_quant_var(dataframe.columns)
    # print(cabecalhos)
    colunas = list(dataframe.columns)
    scatter = scatter_plot(dataframe, coluna1, coluna2).to_html()


    print(request.GET)
    print('---- OUT')
    elements = request.GET.getlist('statistics_names')
    if not elements:
        elements = cabecalhos
    a = dataframe.columns.intersection(elements)
    print(a)
    data = dataframe[dataframe.columns.intersection(a)]
    print(data)
    boxplot = boxplot_completo(data).to_html()


    # moda = {'CountryID': 'Não há moda na amostra', '2021 Score': [5650000.0, 58180.0], 'Property Rights': 4610000.0, 'Judical Effectiveness': 2820000.0}

    context = {
        'form': UploadCsvForm(),
        'boxplot': boxplot,
        'histogram': histogram,
        'heatmap': heatmap,
        'scatter': scatter,
        'mean': list(media),
        'median': list(mediana),
        'mode': dict(moda),
        'variance': list(variancia),
        'std': list(desvio),
        'columns': colunas,
        'columns_num': cabecalhos,
    }
    return render(request, 'statistics.html', context)

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
