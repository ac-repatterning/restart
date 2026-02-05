"""Module api.py"""
import boto3

import src.algorithms.data


class API:
    """
    All gauges
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector:
        """

        self.__data = src.algorithms.data.Data(connector=connector)

    def __call__(self, ts_id: int, starting: str, ending: str) -> dict | list[dict]:
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

        return self.__data.exc(
            url=url.format(ts_id=ts_id, starting=starting, ending=ending))

