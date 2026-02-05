
import dask
import boto3

import src.elements.partitions as prt
import src.algorithms.api


class Interface:

    def __init__(self, connector: boto3.session.Session):

        self.__connector = connector

    def exc(self, partitions: list[prt.Partitions]):

        __api = dask.delayed(src.algorithms.api.API(connector=self.__connector).__call__)

        computations = []
        for partition in partitions:
            data = __api(ts_id=partition.ts_id, starting=partition.starting, ending=partition.ending)
