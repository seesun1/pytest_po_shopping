import configparser

import yaml

from utils.get_filepath import get_yaml_path, get_ini_path

path = get_yaml_path()
ini_path = get_ini_path()


def read_yaml():
    with open(path, encoding="utf8") as f:
        data = yaml.safe_load(f)
        return data


def read_ini():
    config = configparser.ConfigParser()
    config.read(ini_path, encoding='utf8')
    return config


if __name__ == '__main__':
    print(read_yaml()['user_login'])
    # print(read_ini()['mysql']['HOST'])