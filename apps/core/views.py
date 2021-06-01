from django.shortcuts import get_list_or_404, render, redirect
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
    one_hour_ago = now() + datetime.timedelta(minutes=-720)
    arquivos = CsvFile.objects.filter(user=request.user, created_at__gte=one_hour_ago)

    for i in arquivos:
        try:
            # tenta abrir para ver se está dentro do filesystem do Heroku
            open(i.file.path)
        except:
            # se tiver sido apagado, retira da queryset
            i.delete()

    # refaz a queryset com os arquivos apagados
    arquivos = CsvFile.objects.filter(user=request.user, created_at__gte=one_hour_ago)

    context = {
        'form': UploadCsvForm(),
        'files': arquivos,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def statistics(request, file_id):
    arquivo = CsvFile.objects.get(user=request.user, id=file_id)
    dataframe = data_conversion.csv_to_df(arquivo.file)

    print(dataframe)
    print(dataframe.empty)

    media = mean(dataframe)
    mediana = median(dataframe)
    moda = mode(dataframe)
    variancia = variance(dataframe)
    desvio = standard_deviation(dataframe)
    quartil = quartile(dataframe)

    cabecalhos = dataframe.select_dtypes(include=np.number).columns.tolist()
    # cabecalhos = get_quant_var(dataframe)
    colunas = list(dataframe.columns)

    # get_quant_var(df)
    
    elements = request.GET.getlist('statistics_names')
    if not elements:
        elements = cabecalhos
    dataframe_sliced = dataframe.columns.intersection(elements)
    new_dataframe = dataframe[dataframe.columns.intersection(dataframe_sliced)]

    graph = request.GET.getlist('graphs')
    graph_render = None
    if len(graph) > 0:
        from math import ceil
        height = ceil(len(new_dataframe.columns)/5)
        height = 400 * height

        if graph[0] == 'boxplot':
            try:
                graph_render = boxplot_completo(new_dataframe).to_html(default_height=height)
            except:
                print("ERRO")
        elif graph[0] == 'histogram':
            graph_render = histograma_completo(new_dataframe).to_html(default_height=height)
        elif graph[0] == 'heatmap':
            graph_render = correlation_heatmap(new_dataframe).to_html(default_height=height)
        elif graph[0] == 'scatter':
            if len(new_dataframe.columns) != 2:
                messages.error(request, "Para gráficos de dispersão é necessário informar 2 campos!")
                return HttpResponseRedirect('.')
            graph_render = scatter_plot(new_dataframe, new_dataframe.columns[0], new_dataframe.columns[1]).to_html()

    # moda = {'CountryID': 'Não há moda na amostra', '2021 Score': [5650000.0, 58180.0], 'Property Rights': 4610000.0, 'Judical Effectiveness': 2820000.0}
    print(quartil)
    print(list(quartil))

    context = {
        'form': UploadCsvForm(),
        'graph': graph_render,
        'mean': list(media),
        'median': list(mediana),
        'mode': dict(moda),
        'quartil': dict(quartil),
        'variance': list(variancia),
        'std': list(desvio),
        'columns': colunas,
        'columns_num': cabecalhos,
    }
    return render(request, 'statistics.html', context)

@login_required(login_url='login')
def upload(request):
    if request.method == "POST":

        try:
            dataframe = data_conversion.csv_to_df(request.FILES['file'])
        except:
            messages.error(request, "Erro inesperado! Verifique o tipo do arquivo e siga as instruções abaixo.")
            return HttpResponseRedirect('/upload')

        if np.nan in dataframe.index:
            messages.error(request, "Índices vazios. Envie um arquivo válido!")
            return HttpResponseRedirect('/upload')

        if dataframe.empty:
            messages.error(request, "Arquivo vazio. Envie um arquivo válido!")
            return HttpResponseRedirect('/upload')

        CsvFile.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            file=request.FILES['file'])
        messages.success(request, "Arquivo enviado com sucesso!")
        return HttpResponseRedirect('/upload')
    else:
        context = {'form': UploadCsvForm()}
        return render(request, 'upload.html', context)
