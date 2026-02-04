"""Module interface.py"""
import logging
import sys

import pandas as pd

import src.assets.partitions
import src.elements.partitions as prt
import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.cache
import src.functions.streams


class Interface:
    """
    Interface
    """

    def __init__(self, s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        :param arguments: A set of data acquisition arguments.
        """

        self.__s3_parameters = s3_parameters
        self.__arguments = arguments
        self.__streams = src.functions.streams.Streams()

    def __get_assets(self) -> pd.DataFrame:
        """
        #
        :return:
        """

        store: dict = self.__arguments.get('list_of_gauges_store')
        bucket = self.__s3_parameters._asdict()[store.get('bucket_class')]
        prefix = store.get('prefix')

        uri = f's3://{bucket}/{prefix}'
        text = txa.TextAttributes(uri=uri, header=0, date_fields=['from', 'to'])

        return self.__streams.read(text=text)

    def __in_focus(self, assets: pd.DataFrame) -> pd.DataFrame:
        """

        :param assets:
        :return:
        """

        assets = assets.loc[assets['ts_id'].isin(self.__arguments.get('excerpt')), :]

        return assets

    def exc(self) -> list[prt.Partitions]:
        """

        :return:
        """

        # Assets that have points that span a core period.
        assets = self.__get_assets()
        logging.info(assets)
        logging.info(assets[['ts_id', 'from', 'to']])
        assets.info()

        # If not starting from scratch
        if not self.__arguments.get('reacquire'):
            assets = self.__in_focus(assets=assets.copy())
        logging.info(assets)

        # Empty
        if assets.empty:
            logging.info('No gauge assets. Set-up:\nReacquire -> %s\nLength of gauge assets list: %s',
                         self.__arguments.get('reacquire'), assets.shape[0])
            src.functions.cache.Cache().exc()
            sys.exit()

        # Partitions for parallel data retrieval; for parallel computing.
        partitions = src.assets.partitions.Partitions(data=assets).exc()
        logging.info(partitions)

        return partitions
