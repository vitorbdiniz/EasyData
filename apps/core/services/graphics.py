from apps.core.services.statistics import *
import pandas as pd
import numpy as np
import statistics as st
import datetime as dt

#plotly imports
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def boxplot_comparando_outliers(df:pd.DataFrame):
    plot = make_subplots(rows=2, cols=df.shape[1], subplot_titles=df.columns.tolist()*2)
    plot.update_layout(title={'text': "Boxplots",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})

    i=1
    for col in df:
        plot.add_box(y=df[col], row=1, col=i, name=col)
        i+=1
    df = outliers_df(df)
    i=1
    for col in df:
        plot.add_box(y=df[col], row=2, col=i, name=col)
        i+=1

    return plot

def boxplot_dados_originais(df:pd.DataFrame):
    nrows = 1 if df.shape[1] <= 5 else int(df.shape[1]/5) +1
    ncols = df.shape[1] if df.shape[1] <= 5 else 5

    plot = make_subplots(rows=nrows, cols=ncols, subplot_titles=df.columns)
    plot.update_layout(title={'text': "Boxplots",'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    i,j=1,1
    for col in df:
        plot.add_box(y=df[col], row=i, col=j, name=col)
        j+=1
        if j>ncols:
            j=1
            i+=1

    return plot

def boxplot_completo(df:pd.DataFrame, compare_outliers=False,dropna=True, dropinf=True):
    df = df[get_quant_var(df)]
    if dropna:
        df = df.dropna()
    if dropinf:
        df = remove_inf(df)

    plot = boxplot_dados_originais(df) if not compare_outliers else boxplot_comparando_outliers(df)

    return plot


def histograma_comparando_outliers(df:pd.DataFrame):
    plot = make_subplots(rows=2, cols=df.shape[1], subplot_titles=df.columns.tolist()*2)
    plot.update_layout(title={'text': "Histogramas",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    i=1
    for col in df:
        plot.add_histogram(x=df[col].values, row=1, col=i, name=col, histnorm='probability')
        i+=1
    df = outliers_df(df)
    i=1
    for col in df:
        plot.add_histogram(x=df[col].values, row=2, col=i, name=col, histnorm='probability')
        i+=1
    return plot

def histograma_dados_originais(df:pd.DataFrame):

    nrows = 1 if df.shape[1] <= 5 else int(df.shape[1]/5) +1
    ncols = df.shape[1] if df.shape[1] <= 5 else 5

    plot = make_subplots(rows=nrows, cols=ncols, subplot_titles=df.columns)
    plot.update_layout(title={'text': "Histogramas",'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    i,j=1,1
    for col in df:
        plot.add_histogram(x=df[col].values, row=i, col=j, name=col, histnorm='probability')
        j+=1
        if j>ncols:
            j=1
            i+=1

    return plot

def histograma_completo(df:pd.DataFrame, compare_outliers=False,dropna=True, dropinf=True):
    df = df[get_quant_var(df)]
    if dropna:
        df = df.dropna()
    if dropinf:
        df = remove_inf(df)

    plot = histograma_dados_originais(df) if not compare_outliers else histograma_comparando_outliers(df)

    return plot

#Plot de heatmap de correlações

def correlation_heatmap(df:pd.DataFrame, removeDuplicates = False, method='pearson'):
    corr = df.corr(method=method)
    if removeDuplicates:
        corr = corr.mask(np.tril(np.ones(corr.shape)).astype(np.bool))
    plot = go.Figure(data=go.Heatmap(
                   z=corr,
                   x=corr.columns,
                   y=corr.index))
    return plot



def scatter_plot(df, col1, col2, remove_outliers=False):
    s1 = df[col1]
    s2 = df[col2]

    if col1==col2:
        col2 += ' '
    df = pd.DataFrame({col1:s1, col2:s2})
    if remove_outliers:
        df = outliers_df(df)
    plot = px.scatter(df, x=col1, y=col2, title=f'Dispersão: {col1} X {col2}')

    return plot




def make_line(array, a, b):
    return [a*x+b for x in array ]
    
def regression_plot(df:pd.DataFrame, target_var, independent_variables=[], dropna=True, dropinf=True):
    quantitative_variables = set(get_quant_var(df))
    df = df[quantitative_variables]

    if len(independent_variables)==0:
        independent_variables = list(df.columns)

    independent_variables = [var for var in independent_variables if var in quantitative_variables and var != target_var]

    if dropna:
        df = df.dropna()
    if dropinf:
        df = remove_inf(df)

    model = linear_regression(df, target_var, independent_variables)
    if type(model) == str:
        return model
    params = { var: coef for var, coef in zip(independent_variables, model.coef_)}

    nrows = 1 if len(independent_variables) <= 5 else int((len(independent_variables))/5) +1
    ncols = (len(independent_variables)) if (len(independent_variables)) <= 5 else 5

    plot = make_subplots(rows=nrows, cols=ncols, subplot_titles= [ coef for coef in independent_variables ] ) 
    plot.update_layout(title={'text': "Gráfico de Dispersão + Regressão",'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    i,j=1,1
    for p in independent_variables:
        plot.add_trace(go.Scatter( x=df[p], y=df[target_var], mode='markers', name=f'{p} X {target_var}'  ), row=i, col=j )
        plot.add_trace( go.Scatter(x=df[p], y = make_line(df[p], params[p], model.intercept_), name=f'Regressão: {p} X {target_var}' ), row=i, col=j )

        j+=1
        if j>ncols:
            j=1
            i+=1
    return plot




def plot_p_values(df, columns=[]):
    fig = go.Figure()
    fig.update_layout(title={'text': "P-Valores",'x':0.5,'xanchor': 'center','yanchor': 'top'})

    quant_var = set(get_quant_var(df))
    if len(columns) == 0:
        columns = list(quant_var)
    else:
        columns = [ col for col in columns if col in quant_var ]

    if len(columns) < 2:
        return 'Menos que 2 variaveis quantitativas selecionadas'

    x_axis = []
    for i in range( len(columns) ):
        col1 = columns[i]
        for j in range( i+1, len(columns) ):
            col2 = columns[j]
            x_axis.append(f'p-valor: {col1} X {col2}')

            fig.add_trace(go.Bar(
                x = [x_axis[-1]],
                y=[p_value(df, col1, col2, quant_var=columns)],
                name=x_axis[-1]
            ))

    fig.add_trace( go.Scatter(x=x_axis, y = [0.05 for i in x_axis], name=f'Fronteira de Significância' ) )

    return fig


def plot_t_statistic(df, columns=[]):
    fig = go.Figure()
    fig.update_layout(title={'text': "Estatística-T",'x':0.5,'xanchor': 'center','yanchor': 'top'})

    quant_var = set(get_quant_var(df))
    if len(columns) == 0:
        columns = list(quant_var)
    else:
        columns = [ col for col in columns if col in quant_var ]

    if len(columns) < 2:
        return 'Menos que 2 variaveis quantitativas selecionadas'

    x_axis = []
    for i in range( len(columns) ):
        col1 = columns[i]
        for j in range( i+1, len(columns) ):
            col2 = columns[j]
            x_axis.append(f'Estatística-T: {col1} X {col2}')

            fig.add_trace(go.Bar(
                x = [x_axis[-1]],
                y=[t_statistic(df, col1, col2, quant_var=columns)],
                name=x_axis[-1]
            ))

    fig.add_trace( go.Scatter(x=x_axis, y = [2 for i in x_axis], name=f'Fronteira de Significância (+)' ) )
    fig.add_trace( go.Scatter(x=x_axis, y = [-2 for i in x_axis], name=f'Fronteira de Significância (-)' ) )

    return fig

