import pandas as pd
import numpy as np

def get_dataframe_columns_as_dictionary(dataframe):
    '''
    Dictionary example:
    {'column1': dtype('O'), 'column2': dtype('int64'), 'column3': dtype('O'), 'column4': dtype('float64')}
    key = column
    value = type
    '''
    dictionary = dict(dataframe.dtypes)
    return dictionary

def get_data_type_of_column(dataframe, column):
    '''
    Column example: 'Age'
    '''
    dataTypeObj = dataframe.dtypes[column]
    return dataTypeObj

# Check the type of column is int64
def is_column_int(dataframe, column):
    '''
    Column example: 'Age'
    '''
    return get_data_type_of_column(dataframe, column) == np.int64

# Check the type of column is Object (string)
'''
    Column example: 'Age'
    '''
def is_column_string(dataframe, column):
    return get_data_type_of_column(dataframe, column) == np.object

# Check the type of column is Float64
'''
    Column example: 'Age'
    '''
def is_column_float(dataframe, column):
    return get_data_type_of_column(dataframe, column) == np.float64