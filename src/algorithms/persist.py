
import os

import pandas as pd

class Persist:

    def __init__(self, blob: pd.DataFrame, catchment_id: int, ts_id: int):

        self.__blob = blob

        self.__path = os.path.join(os.getcwd(), str(catchment_id), str(ts_id))
        os.makedirs(self.__path)

    def __persist(self, group: int):

        section: pd.DataFrame = self.__blob.loc[self.__blob['group'] == group, :]
        values = section.sort_values(by='timestamp', ignore_index=True)
        values.to_csv(os.path.join(self.__path, f'{group}-01-01.csv'), header=True, encoding='utf-8', index=False)

        return True

    def exc(self):

        states = [self.__persist(group = group) for group in self.__blob['group'].unique()]

        return all(states)
