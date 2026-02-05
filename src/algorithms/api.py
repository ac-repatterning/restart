"""Module api.py"""
import boto3
import pandas as pd

import src.algorithms.content


class API:
    """
    All gauges
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector:
        """

        self.__data = src.algorithms.content.Content(connector=connector)

        # renaming
        self.__rename = {'Timestamp': 'timestamp', 'Value': 'value', 'Quality Code': 'quality_code'}

    def __get_frame(self, content: dict | list[dict]) -> pd.DataFrame:

        # The data in data frame form
        columns = content[0]['columns'].split(',')
        frame = pd.DataFrame.from_records(data=content[0]['data'], columns=columns)
        frame.rename(columns=self.__rename, inplace=True)

        # The identification codes of the time series
        frame = frame.assign(ts_id=content[0]['ts_id'])

        # Group
        frame['group'] = pd.to_datetime(frame['timestamp'], unit='ms').dt.year

        return frame

    def __call__(self, ts_id: int, starting: str, ending: str):
        """
        https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0
        &request=getTimeseriesValues&ts_id=52438010
        &from=2003-01-01&to=2012-12-31&returnfields=Timestamp,Value,Quality Code&metadata=true
        &md_returnfields=ts_id,ts_name,ts_unitname,ts_unitsymbol,station_id,
        catchment_id,parametertype_id,parametertype_name,river_name&dateformat=UNIX&format=json


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

        content: dict | list[dict] = self.__data.exc(
            url=url.format(ts_id=ts_id, starting=starting, ending=ending))

        return self.__get_frame(content=content)
