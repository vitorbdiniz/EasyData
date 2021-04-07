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
        avg = data.median()
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return avg

def mode(data):
    """


    """
    data_df = pd.DataFrame(data)
    if data_df.shape[1] > 0:
        avg = data.mode()
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return avg    

def quantile(data, q):
    """

    """    
    data_df = pd.DataFrame(data)
    if data_df.shape[1] > 0:
        quantiles = [np.quantile(data_df[col], q=q) for col in data_df.columns]
    else:
        raise ValueError(f"Empty data received. data should have shape (1,1) or higher and it has {data_df.shape}")
    return pd.Series(quantiles, index=data_df.columns)


