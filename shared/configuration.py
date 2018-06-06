from io import StringIO
import os
import re
import yaml


class ConfigurationError(Exception):
    pass


class Configuration:
    """
    Class for reading configuration from a YAML file
    """
    def __init__(self, config_dict):
        self.configuration = config_dict

    @classmethod
    def from_file(cls, filename: str):
        """
        :param filename: YAML configuration filename
        :return: :class:`Configuration` object
        """
        with open(filename) as fp:
            config_content = ''.join(fp.readlines())
            config_dict = yaml.load(StringIO(cls._replace_placeholders(config_content)))

        return cls(config_dict)

    @staticmethod
    def _replace_placeholders(text) -> str:
        """
        Replaces place holders like `$VAR_NAME` in YAML configuration with values of environment variables
        :param text: text content of the configuration file with placeholders
        :return: text content of the configuration file with actual values from environment variables
        """
        for match in re.findall('\$[A-Z_]+', text):
            env_var_name = match[1:]
            try:
                text = text.replace(match, os.environ[env_var_name])
            except KeyError as e:
                raise ConfigurationError('Environment variable not defined: ' + env_var_name) from e
        return text

    def get(self, key: str):
        """
        Returns value from the configuration according to configuration file
        :param key: configuration key
        :return: configuration value
        """
        try:
            return self.configuration[key]
        except KeyError as e:
            raise ConfigurationError('Key not defined in configuration file: ' + key) from e

    def __getitem__(self, key):
        return self.get(key)

    def __repr__(self):
        return str(self.configuration)
