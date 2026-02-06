"""Module api.py"""
import boto3
import pandas as pd

import src.algorithms.content
import src.functions.objects


class Data:
    """
    Data
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector:
        :param arguments:
        """

        self.__arguments = arguments

        # pylint: disable=W0238
        self.__content = src.algorithms.content.Content(connector=connector)
        self.__objects = src.functions.objects.Objects()

        # renaming
        self.__rename = {'Timestamp': 'timestamp', 'Value': 'value', 'Quality Code': 'quality_code'}

    def __restructure(self, content: dict | list[dict]):
        """

        :param content:
        :return:
        """

        # The data in data frame form
        columns = content[0]['columns'].split(',')
        frame = pd.DataFrame.from_records(data=content[0]['data'], columns=columns)

        if frame.empty:
            return frame

        # Renaming
        frame.rename(columns=self.__rename, inplace=True)

        # The identification codes of the time series
        frame = frame.assign(ts_id=content[0]['ts_id'])
        frame['group'] = pd.to_datetime(frame['timestamp'], unit='ms').dt.year

        return frame

    def __get_temporary(self, url: str):
        """

        :param url:
        :return:
        """

        content: dict | list[dict] = self.__objects.api(url=url)

        return self.__restructure(content=content)

    def __get_frame(self, content: dict | list[dict]) -> pd.DataFrame:
        """

        :param content:
        :return:
        """

        return self.__restructure(content=content)

    def __call__(self, ts_id: int, starting: str, ending: str) -> pd.DataFrame:
        """


        :param ts_id: The identification code of a gauge's time series.
        :param starting: Format yyyy-mm-dd
        :param ending: Format yyyy-mm-dd
        :return:
        """

        url = ('https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0'
               '&request=getTimeseriesValues&ts_id={ts_id}'
               '&from={starting}&to={ending}&returnfields=Timestamp,Value,Quality Code&metadata=true'
               '&md_returnfields=ts_id,ts_name,ts_unitname,ts_unitsymbol,station_id,'
               'catchment_id,parametertype_id,parametertype_name,river_name&dateformat=UNIX&format=json')

        if self.__arguments.get('via-key'):
            content: dict | list[dict] = self.__content.exc(
                url=url.format(ts_id=ts_id, starting=starting, ending=ending))

            return self.__get_frame(content=content)

        return self.__get_temporary(
            url=url.format(ts_id=ts_id, starting=starting, ending=ending))
