"""Module interface.py"""
import json
import logging
import os

import pandas as pd

import src.elements.partitions as prt
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.ingress
import src.s3.unload
import src.transfer.cloud
import src.transfer.dictionary


class Interface:
    """
    Class Interface
    """

    def __init__(self, service: sr.Service,  s3_parameters: s3p, arguments: dict, partitions: list[prt.Partitions]):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        :param arguments:
        :param partitions:
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__arguments = arguments
        self.__partitions = partitions

    def __metadata(self) -> dict:
        """
       s3:// {bucket.name} / key = prefix + file name (including extension)

       :return:
       """

        key_name = 'data/metadata.json'

        buffer = src.s3.unload.Unload(s3_client=self.__service.s3_client).exc(
            bucket_name=self.__s3_parameters.configurations, key_name=key_name)

        return json.loads(buffer)

    def exc(self):
        """

        :return:
        """

        metadata = self.__metadata()

        # The strings for transferring data to Amazon S3 (Simple Storage Service)
        dictionary = src.transfer.dictionary.Dictionary(metadata=metadata)
        strings: pd.DataFrame = dictionary.exc(
            path=os.path.join(os.getcwd(), 'warehouse'), extension='*', prefix='')
        logging.info(strings)

        # Prepare storage areas
        src.transfer.cloud.Cloud(
            service=self.__service, s3_parameters=self.__s3_parameters, arguments=self.__arguments,
            partitions=self.__partitions).exc()

        # Transfer
        if not strings.empty:
            messages = src.s3.ingress.Ingress(
                service=self.__service, bucket_name=self.__s3_parameters.internal).exc(
                strings=strings, tags={'project': 'hydrography'})
            logging.info(messages)
        else:
            logging.info('Empty')
