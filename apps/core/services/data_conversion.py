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

    try:
        result = pd.read_csv(data)
    except:
        result = ''' Certifique-se de que o arquivo enviado está de acordo com os seguintes requisitos:
        1. O arquivo enviado deve ser do tipo ".csv" e suas colunas devem ser separadas por vírgulas.
        2. Todas as colunas do arquivo devem começar na linha um.
        3. A primeira linha do arquivo deve conter os nomes das colunas presentes.
        4. Todas as colunas, com excessão do nome, devem ser numéricas, garantindo que as estatísticas sejam calculadas corretamente.
        5. Não devem existir na planilha dados incoerentes e que não façam parte do conjunto de dados a ser analisado.
        '''
        

    return result


def df_to_json(data):
    """ 
        Converts a pandas dataframe to json
        params:
            data: {pandas.DataFrame, pandas.Series}
        returns:
            {json}
    """
    return data.to_json()

