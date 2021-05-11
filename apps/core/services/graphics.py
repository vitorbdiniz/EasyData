from EasyData.apps.core.services.statistics import *
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
    plot.update_layout(title={'text': "Boxplots",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    i,j=1,1
    for col in df:
        plot.add_box(y=df[col], row=i, col=j, name=col)
        j+=1
        if j>ncols:
            j=0
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
    plot.update_layout(title={'text': "Histogramas",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})
    
    i,j=1,1
    for col in df:
        plot.add_histogram(x=df[col].values, row=i, col=j, name=col, histnorm='probability')
        j+=1
        if j>ncols:
            j=0
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
    df = df[[col1, col2]]
    if remove_outliers:
        df = outliers_df(df)
    plot = px.scatter(df, x=col1, y=col2, title=f'Dispersão: {col1} X {col2}')

    return plot