import pandas as pd

from backend.src.app.services.data_conversion import json_to_df

class data():
    def __init__(self, json_data):
        self.data = json_to_df(json_data)
        
    def get_data(self):
        return self.data
    def set_data(self, data):
        if type(data) == pd.DataFrame:
            self.data = data
        else:
            self.data = json_to_df(data)