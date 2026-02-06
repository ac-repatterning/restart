"""Module setup.py"""
import logging
import sys

import dask
import dask.distributed

import src.elements.partitions as prt
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.cache
import src.functions.directories
import src.s3.bucket
import src.s3.keys
import src.s3.prefix


class Cloud:
    """
    Description
    -----------

    Sets up local & cloud environments
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters, arguments: dict,
                 partitions: list[prt.Partitions]):
        """

        :param service: A suite of services for interacting with Amazon Web Services.<br>
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.<br>
        :param arguments: A set of arguments vis-à-vis computation & storage objectives.<br>
        :param partitions
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__arguments = arguments
        self.__partitions = partitions

        # Bucket
        self.__bucket_name = self.__s3_parameters.internal

    def __clear_prefix(self, prefix: str) -> bool:
        """

        :return:
        """

        # An instance for interacting with objects within an Amazon S3 prefix
        instance = src.s3.prefix.Prefix(service=self.__service, bucket_name=self.__bucket_name)

        # Get the keys therein
        keys: list[str] = instance.objects(prefix=prefix)

        if len(keys) > 0:
            objects = [{'Key' : key} for key in keys]
            state = instance.delete(objects=objects)
            return bool(state)

        return True

    def __s3(self) -> bool | list[bool]:
        """
        Prepares an Amazon S3 (Simple Storage Service) bucket.

        :return:
        """

        # An instance for interacting with Amazon S3 buckets.
        bucket = src.s3.bucket.Bucket(service=self.__service,
                                      location_constraint=self.__s3_parameters.location_constraint,
                                      bucket_name=self.__bucket_name)

        # Strategy Switch: If the bucket exist, do not clear the target prefix, overwrite files instead.
        if bucket.exists():

            __prefix = ['data/series'] if self.__arguments.get('reacquire') else [
                f'data/series/{partition.catchment_id}/{partition.ts_id}' for partition in self.__partitions]

            return [self.__clear_prefix(prefix=prefix) for prefix in __prefix]

        return bucket.create()

    def exc(self) -> bool:
        """

        :return:
        """

        states = self.__s3()
        logging.info(type(states))
        logging.info(states)

        if all(states):
            return True

        src.functions.cache.Cache().exc()
        sys.exit('Unable to set up an Amazon S3 (Simple Storage Service) section.')
