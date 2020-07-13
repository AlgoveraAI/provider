"""Config data."""

#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import configparser
import logging
import os
from pathlib import Path

NAME_KEEPER_URL = 'network.url'
NAME_KEEPER_PATH = 'keeper.path'
NAME_AUTH_TOKEN_MESSAGE = 'auth_token_message'
NAME_AUTH_TOKEN_EXPIRATION = 'auth_token_expiration'
NAME_DATA_TOKEN_FACTORY_ADDRESS = 'factory.address'

NAME_AQUARIUS_URL = 'aquarius.url'
NAME_PARITY_URL = 'parity.url'
NAME_OPERATOR_SERVICE_URL = 'operator_service.url'

environ_names = {

    NAME_DATA_TOKEN_FACTORY_ADDRESS: ['DATA_TOKEN_FACTORY_ADDRESS', 'Data token factory address', 'keeper-contracts'],
    NAME_KEEPER_URL: ['KEEPER_URL', 'Keeper URL', 'keeper-contracts'],
    NAME_KEEPER_PATH: ['KEEPER_PATH', 'Path to the keeper contracts', 'keeper-contracts'],
    NAME_AUTH_TOKEN_MESSAGE: ['AUTH_TOKEN_MESSAGE',
                              'Message to use for generating user auth token', 'resources'],
    NAME_AUTH_TOKEN_EXPIRATION: ['AUTH_TOKEN_EXPIRATION',
                                 'Auth token expiration time expressed in seconds', 'resources'],
    NAME_AQUARIUS_URL: ['AQUARIUS_URL', 'Aquarius url (metadata store)', 'resources'],
    NAME_PARITY_URL: ['PARITY_URL', 'Parity URL', 'keeper-contracts'],
    NAME_OPERATOR_SERVICE_URL: ['OPERATOR_SERVICE_URL', 'Operator service URL', 'resources'],
}


class Config(configparser.ConfigParser):
    """Class to manage the squid-py configuration."""

    def __init__(self, filename=None, options_dict=None, **kwargs):
        """
        Initialize Config class.

        Options available:

        [keeper-contracts]
        network.url = http://localhost:8545                            # ocean-contracts url.
        keeper.path = artifacts                                       # Path of json abis.

        [resources]
        aquarius.url = http://localhost:5000

        :param filename: Path of the config file, str.
        :param options_dict: Python dict with the config, dict.
        :param kwargs: Additional args. If you pass text, you have to pass the plain text
        configuration.
        """
        configparser.ConfigParser.__init__(self)

        self._section_name = 'keeper-contracts'
        self._logger = logging.getLogger('config')

        if filename:
            self._logger.debug(f'Config: loading config file {filename}')
            with open(filename) as fp:
                text = fp.read()
                self.read_string(text)
        else:
            if 'text' in kwargs:
                self.read_string(kwargs['text'])

        if options_dict:
            self._logger.debug(f'Config: loading from dict {options_dict}')
            self.read_dict(options_dict)

        self._load_environ()

    def _load_environ(self):
        for option_name, environ_item in environ_names.items():
            value = os.environ.get(environ_item[0])
            if value is not None:
                self._logger.debug(f'Config: setting environ {option_name} = {value}')
                self.set(environ_item[2], option_name, value)

    @property
    def keeper_path(self):
        """Path where the keeper-contracts artifacts are allocated."""
        keeper_path_string = self.get(self._section_name, NAME_KEEPER_PATH, fallback=None)
        return Path(keeper_path_string).expanduser().resolve() if keeper_path_string else ''

    @property
    def keeper_url(self):
        """URL of the keeper. (e.g.): http://mykeeper:8545."""
        return self.get(self._section_name, NAME_KEEPER_URL, fallback=None)

    @property
    def factory_address(self):
        return self.get(
            environ_names[NAME_DATA_TOKEN_FACTORY_ADDRESS][2],
            NAME_DATA_TOKEN_FACTORY_ADDRESS,
            fallback=None
        )

    @property
    def aquarius_url(self):
        return self.get('resources', NAME_AQUARIUS_URL, fallback=None)

    @property
    def operator_service_url(self):
        """URL of the operator service component. (e.g.): http://myoperatorservice:8050."""
        return self.get('resources', NAME_OPERATOR_SERVICE_URL, fallback=None)

    @property
    def auth_token_message(self):
        return self.get('resources', NAME_AUTH_TOKEN_MESSAGE, fallback=None)

    @property
    def auth_token_expiration(self):
        return self.get('resources', NAME_AUTH_TOKEN_EXPIRATION, fallback=None)
