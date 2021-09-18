from argparse import ArgumentParser
import yaml
from os import path

CONFIG = "default_url.yaml"


def read_yaml_config(filename):
    try:
        with open(filename, "r") as stream:
            config = yaml.safe_load(stream)
    except yaml.YAMLError:
        config = False
    return config


def read_command_line(parser):
    parser.add_argument("yaml_filename", help="name of the yaml configuration file", nargs='?', default=CONFIG)
    parameter = parser.parse_args()
    file_name = parameter.yaml_filename
    dir_path = path.dirname(path.realpath(__file__))
    return dir_path + '/' + file_name


def get_url(parser):
    filename = read_command_line(parser)
    fetched_url = read_yaml_config(filename)
    return fetched_url


def read_config():
    parser = ArgumentParser()
    url = list(get_url(parser).values())[0]
    return url