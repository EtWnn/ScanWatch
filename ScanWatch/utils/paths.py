import os
from pathlib import Path
from appdirs import AppDirs

_app_dirs = AppDirs("BinanceWatch", "EtWnn")


def get_data_path():
    """
    Return the folder path where to store the data created by this project
    It uses the library appdirs to follow the conventions across multi OS(MAc, Linux, Windows)

    https://pypi.org/project/appdirs/

    :return: path of the folder to use for data saving
    :rtype: pathlib.Path
    """
    return Path(_app_dirs.user_data_dir)


try:  # create the data folder path
    os.makedirs(get_data_path())
except FileExistsError:
    pass


