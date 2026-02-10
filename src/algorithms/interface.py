"""Module algorithms/interface.py"""
import logging

import boto3
import dask
import pandas as pd

import src.algorithms.data
import src.algorithms.headers
import src.algorithms.persist
import src.elements.partitions as prt


class Interface:
    """
    The interface to the src/algorithms' programs.
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments: A set of computation arguments.
        """

        self.__connector = connector
        self.__arguments = arguments

    @dask.delayed
    def __persist(self, data: pd.DataFrame, partition: prt.Partitions):
        """

        :param data: A gauge's data set.
        :param partition: Refer to src/elements/partition.py
        :return:
        """

        return src.algorithms.persist.Persist(
            data=data, partition=partition).exc()

    def exc(self, partitions: list[prt.Partitions]):
        """

        :param partitions: For more about each object in the list, refer to src/elements/partition.py
        :return:
        """

        headers = src.algorithms.headers.Headers(connector=self.__connector)() \
            if self.__arguments.get('via_key') else {}
        __data = dask.delayed(src.algorithms.data.Data(headers=headers, arguments=self.__arguments).__call__)

        computations = []
        for partition in partitions:
            data = __data(ts_id=partition.ts_id, starting=partition.starting, ending=partition.ending)
            message = self.__persist(data=data, partition=partition)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        logging.info(sum(messages, []))
