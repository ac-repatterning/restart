
import os

import pandas as pd

class Persist:
    """
    
    """

    def __init__(self, data: pd.DataFrame, catchment_id: int, ts_id: int):
        """

        :param data:
        :param catchment_id:
        :param ts_id:
        """

        self.__data = data

        self.__path = os.path.join(os.getcwd(), str(catchment_id), str(ts_id))
        os.makedirs(self.__path)

    def __persist(self, group: int):
        """

        :param group:
        :return:
        """

        section: pd.DataFrame = self.__data.loc[self.__data['group'] == group, :]
        values = section.sort_values(by='timestamp', ignore_index=True)
        values.to_csv(os.path.join(self.__path, f'{group}-01-01.csv'), header=True, encoding='utf-8', index=False)

        return True

    def exc(self):
        """

        :return:
        """

        states = [self.__persist(group = group) for group in self.__data['group'].unique()]

        return all(states)
