import pandas as pd
import numpy as np
from statistics import NormalDist
from sklearn.linear_model import LinearRegression




def mean(data):
    data_df = pd.DataFrame(data)
    # print('data_df', data_df)
    data_df = data[get_quant_var(data_df)]
    try:
        if data_df.shape[1] > 0:
            avg = data.mean(skipna=True)
        else:
            avg = [None]
    except:
        avg = pd.Series([None for col in data_df.columns], index=data_df.columns)
    return avg


def median(data):
    data_df = pd.DataFrame(data)
    data_df = data[get_quant_var(data_df)]
    try:
        if data_df.shape[1] > 0:
            med = data.median()
        else:
            med = [None]
    except:
        med = pd.Series([None for col in data_df.columns], index=data_df.columns)
    return med

def mode(data):
    data_df = pd.DataFrame(data)
    data_df = data[get_quant_var(data_df)]
    mo = dict()
    for col in data_df.columns:
        serie = data_df[col].dropna()
        if serie.shape[0] > 0:
            try:
                moda = serie.mode()
                if moda.shape[0] == 1:
                    moda = [round(moda.iloc[0], 2)]
                elif moda.shape[0] > 1 and moda.shape[0] < serie.shape[0]:
                    moda = moda.tolist()
                    for i in range(len(moda)):
                        moda[i] = round(moda[i], 2)
                else:
                    moda = ['Não há moda na amostra']
            except:
                moda = ['Não há moda na amostra']
        else:
            moda = ['Não há moda na amostra']
        mo[col] = moda
    return mo

def quartile(data):
    '''
        Retorna dicionário de séries:
        {
            0.25 : quantile(data, 0.25), 
            0.5  : quantile(data, 0.5),
            0.75 : quantile(data, 0.75)
        }
    '''
    cols = get_quant_var(data)
    quartiles = dict()
    for c in cols:
        quartis = [quantile_series(data[c], q) for q in [0.25, 0.5, 0.75]]
        quartiles[c] = quartis
    return quartiles

def quantile_series(series, q):
    series.dropna(inplace=True)
    if series.shape[0] > 0:
        quant = np.quantile(series, q=q)
    else:
        quant = None
    return quant


def quantile(data, q):
    data_df = data[get_quant_var(data)]
    data_df.dropna(inplace=True)
    if data_df.shape[1] > 0:
        quantiles = [np.quantile(data_df[col], q=q) for col in data_df.columns]
    else:
        quantiles = []
    return pd.Series(quantiles, index=data_df.columns)



def linear_regression(df, target_variable, independent_variables=[]):
    quantitative_variables = set(get_quant_var(df))
    if len(independent_variables)==0:
        independent_variables = [var for var in list(df.columns) if var in quantitative_variables and var != target_variable]

    if target_variable not in quantitative_variables:
        return 'Variável alvo qualitativa'
    if len(independent_variables) == 0:
        return 'Apenas variáveis dependentes qualitativas selecionadas'

    y = df[target_variable]
    X = df[independent_variables]

    model = LinearRegression(n_jobs=-1, normalize=True).fit(X, y)
    return model



def get_quant_var(df):
    return [col for col in df if pd.api.types.is_numeric_dtype(df[col])]


def get_quali_var(df):
    return [col for col in df if col not in get_quant_var(df)]


def remove_inf(df):
    if type(df) is pd.DataFrame:
        return df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    else:
        return df[~df.isin([np.nan, np.inf, -np.inf])]


def variance(data):
    """

    """    
    data_df = pd.DataFrame(data)
    data_df = data[get_quant_var(data_df)]
    try:
        if data_df.shape[1] > 0:
            var = data_df.var()
        else:
            var = [None]
    except:
        var = pd.Series([None for col in data_df.columns], index=data_df.columns)
    return var

def standard_deviation(data):
    """

    """    
    data_df = pd.DataFrame(data)
    data_df = data[get_quant_var(data_df)]
    try:
        if data_df.shape[1] > 0:
            std = data_df.std()
        else:
            std = [None]
    except:
        std = pd.Series([None for col in data_df.columns], index=data_df.columns)
    return std

def outliers(data,q = 0.25, m = 1.5, dropinf=True, dropna=True):
    """
        q: {float} quantile
        m: {float} multiplier
        Returns an array which contains the outliers row-indexes
    """
    if dropinf:
        data = remove_inf(data)
    if dropna:
        data = data.dropna()

    std = data.std(skipna=True)
    sup = np.quantile(data, q=1-q)
    inf = np.quantile(data, q=q)
    
    sup += std*m
    inf -= std*m
    outlier_lines = [i for i in range(len(data)) if data[i] > sup or data[i] < inf]
            
    return outlier_lines

def outliers_df(data,q = 0.25, m = 1.5, dropinf=True, dropna=True):
    out = []
    if dropna:
        data = data.dropna()
    if dropinf:
        data = remove_inf(data)
    data = data[get_quant_var(data)]

    for col in data:
        out += outliers(data[col], q=q, m=m, dropinf=False, dropna=False)
    return data.drop(index=data.index[out])

def remove_inf(df):
    if type(df) is pd.DataFrame:
        return df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    else:
        return df[~df.isin([np.nan, np.inf, -np.inf])]

def confidence_interval(data, confidence):

    data_df = pd.DataFrame(data)
    data_df = data_df[get_quant_var(data_df)]
    mean_df = mean(data_df)
    standard_deviation_df = standard_deviation(data_df)

    conf = []
    for col in data_df.columns:
        z_score = NormalDist().inv_cdf((1 + confidence) / 2.)
        delta = z_score * (standard_deviation_df[col]/np.sqrt(len(data_df[col])))
        conf.append((mean_df[col] - delta, mean_df[col] + delta))
    return conf