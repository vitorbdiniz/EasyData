import pandas as pd


def json_to_df(data):
    """ 
        Converts json data to pandas dataframe
        params:
            data: {json, json_string}

        returns:
            {pandas.dataframe}
    """
    return pd.read_json(data)


def csv_to_df(data):
    return pd.read_csv(data)


def df_to_json(data):
    """ 
        Converts a pandas dataframe to json
        params:
            data: {pandas.DataFrame, pandas.Series}
        returns:
            {json}
    """
    return data.to_json()

