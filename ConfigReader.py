from argparse import ArgumentParser
import yaml
from os import path

CONFIG = "default_url.yaml"


def read_yaml_config():
    """
    :return: the url contained in the default_url.yaml config file
    """
    yaml_file = path.dirname(path.realpath(__file__)) + "/" + CONFIG
    with open(yaml_file, "r") as stream:
        config = yaml.safe_load(stream)
    url = list(config.values())
    return url[0]


def read_command_line(parser):
    """
    read the command line and expect a valid url
    :param parser:
    :return: url if there is one passed in command line, None if there is nothing
    """
    parser.add_argument("url", help="url of the website to download and explore", nargs='?')
    parameter = parser.parse_args()
    url = parameter.url
    return url


def get_url():
    """
    :return: url passed in command line or contained in the config file if there is no command line argument
    """
    parser = ArgumentParser()
    url = read_command_line(parser)
    if url is not None:
        return url
    return read_yaml_config()
