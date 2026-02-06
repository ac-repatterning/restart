"""Module main.py"""
import argparse
import logging
import os
import sys

import boto3


def main():
    """
    Entry point
    """

    # Logging
    logger: logging.Logger = logging.getLogger(__name__)
    logger.info(__name__)

    # Data acquisition
    partitions: list[prt.Partitions] = src.assets.interface.Interface(
        s3_parameters=s3_parameters, arguments=arguments).exc()

    src.algorithms.interface.Interface(
        connector=connector).exc(partitions=partitions)

    src.transfer.interface.Interface(
        service=service, s3_parameters=s3_parameters, arguments=arguments, partitions=partitions).exc()

    # Deleting __pycache__
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    # Setting-up
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.algorithms.interface
    import src.assets.interface
    import src.elements.s3_parameters as s3p
    import src.elements.service as sr
    import src.elements.partitions as prt
    import src.functions.cache
    import src.functions.service
    import src.s3.s3_parameters
    import src.preface.setup
    import src.specific
    import src.transfer.interface
    import src.preface.interface

    specific = src.specific.Specific()
    parser = argparse.ArgumentParser()
    parser.add_argument('--codes', type=specific.codes,
                        help='Expects a string of one or more comma separated gauge time series codes.')
    parser.add_argument('--reacquire', type=specific.reacquire, default=0,
                        help='Expects -> 1; false, 0 or != 0; true')
    args: argparse.Namespace = parser.parse_args()

    connector: boto3.session.Session
    s3_parameters: s3p.S3Parameters
    service: sr.Service
    arguments: dict
    connector, s3_parameters, service, arguments = src.preface.interface.Interface().exc(args=args)

    main()
