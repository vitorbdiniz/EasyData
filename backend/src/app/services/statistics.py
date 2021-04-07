import pandas as pd
import numpy as np
import statistics as st


def mean(data):
    """


    """
    data_df = pd.DataFrame(data)
    if data_df.shape[1] > 0:
        avg = data.mean()
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return avg


def median(data):
    """


    """
    data_df = pd.DataFrame(data)
    if data_df.shape[1] > 0:
        med = data.median()
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return med

def mode(data):
    """


    """
    data_df = pd.DataFrame(data)
    if data_df.shape[1] > 0:
        mo = data.mode()
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return mo    

def quantile(data, q):
    """

    """    
    data_df = pd.DataFrame(data)
    if data_df.shape[1] > 0:
        quantiles = [np.quantile(data_df[col], q=q) for col in data_df.columns]
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return pd.Series(quantiles, index=data_df.columns)


def variance(data):
    """

    """    
    data_df = pd.DataFrame(data)
    if data_df.shape[1] > 0:
        var = data_df.var()
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return var

def standard_deviation(data):
    """

    """    
    data_df = pd.DataFrame(data)
    if data_df.shape[1] > 0:
        std = data_df.std()
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return std

def outliers(data,q = 0.25, m = 1.5):
    """
        q: {float} quantile
        m: {float} multiplier
        Returns an array which contains the outliers row-indexes
    """
    outlier_lines = []
    sup = np.quantile(data, q=1-q)
    inf = np.quantile(data, q=q)
    sup += st.stdev(data)*m
    inf -= st.stdev(data)*m
    for i in range(len(data)):
        if data[i] > sup or data[i] < inf:
            outlier_lines.append(i)
    return outlier_lines

