"""Module algorithms/interface.py"""
import logging

import boto3
import dask
import pandas as pd

import src.algorithms.data
import src.algorithms.persist
import src.elements.partitions as prt


class Interface:
    """
    The interface to the src/algorithms' programs.
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector:
        """

        self.__connector = connector

    @dask.delayed
    def __persist(self, data: pd.DataFrame, partition: prt.Partitions):
        """

        :param data:
        :param partition:
        :return:
        """

        return src.algorithms.persist.Persist(
            data=data, partition=partition).exc()

    def exc(self, partitions: list[prt.Partitions]):
        """

        :param partitions:
        :return:
        """

        __data = dask.delayed(src.algorithms.data.Data(connector=self.__connector).__call__)

        computations = []
        for partition in partitions:
            data = __data(ts_id=partition.ts_id, starting=partition.starting, ending=partition.ending)
            message = self.__persist(data=data, partition=partition)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        logging.info(sum(messages, []))
