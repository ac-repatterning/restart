"""Module headers.py"""

import boto3
import requests

import src.functions.secret


class Headers:
    """
    This class creates an access token header.
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        self.__secret = src.functions.secret.Secret(connector=connector)

    def __call__(self) -> dict:
        """
        This function sets up an ephemeral data retrieval token dict via a client's key.

        :return:
        """

        token_url = 'https://timeseries.sepa.org.uk/KiWebPortal/rest/auth/oidcServer/token'
        access_key = self.__secret.exc(secret_id='HydrographyProject', node='sepa')
        headers =  {'Authorization':'Basic ' + access_key}
        response_token= requests.post(token_url, headers=headers, data='grant_type=client_credentials', timeout=600)
        access_token = response_token.json()['access_token']

        return {'Authorization':'Bearer ' + access_token}
