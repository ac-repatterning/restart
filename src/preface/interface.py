"""Module interface.py"""
import argparse
import typing

import boto3

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def __get_attributes(self, connector: boto3.session.Session, args: argparse.Namespace) -> dict:
        """

        :param connector:
        :param args:
        :return:
        """

        # The baseline attributes
        attributes = src.s3.configurations.Configurations(connector=connector).objects(
            key_name=self.__configurations.attributes_key)

        # Codes
        if args.codes is not None:
            attributes['excerpt'] = args.codes
        else:
            attributes['excerpt'] = None

        return attributes

    def exc(self, args: argparse.Namespace) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :param args: Wherein -> codes: list[int] | None
        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()
        attributes: dict = self.__get_attributes(connector=connector, args=args)

        src.preface.setup.Setup(
            service=service, s3_parameters=s3_parameters).exc(reacquire=attributes['reacquire'])

        return connector, s3_parameters, service, attributes
