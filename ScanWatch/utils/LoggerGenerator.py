import logging
import os
from typing import Optional

from ScanWatch.utils.paths import get_data_path


class LoggerGenerator:
    """
    This class is a utility to facilitate the creation of loggers for the different classes / files
    """
    LOGS_FOLDER_PATH = get_data_path() / "logs"

    _default_log_level = logging.WARNING
    _default_write_file = False
    _logger_count = 0

    @staticmethod
    def set_global_log_level(log_level: int):
        """
        set the default log level for loggers creation

        :param log_level: threshold to display the message
        :type log_level: logging enum (ex: logging.WARNING)
        :return: None
        :rtype: None
        """
        LoggerGenerator._default_log_level = log_level

    @staticmethod
    def set_default_write_file(write_file: bool):
        """
        set the default write level for loggers creation

        :param write_file: if the logger should save the message in a file
        :type write_file: bool
        :return: None
        :rtype: None
        """
        LoggerGenerator._default_write_file = write_file

    @staticmethod
    def get_logger(logger_name: str, write_file: Optional[bool] = None,
                   log_level: Optional[int] = None) -> logging.Logger:
        """
        create a logger that will display messages according to the log level threshold. If specified, it will
        also save the messages in a file inside the logs folder

        :param logger_name: name of the logger (a unique logger id will be added after the name)
        :type logger_name: str
        :param write_file: if the logger should save the message in a file
        :type write_file: bool
        :param log_level: threshold to display the message
        :type log_level: logging enum (ex: logging.WARNING)
        :return: the logger object
        :rtype: logging.Logger
        """
        if log_level is None:
            log_level = LoggerGenerator._default_log_level
        if write_file is None:
            write_file = LoggerGenerator._default_write_file

        # create logger
        logger = logging.getLogger(f"lg_{LoggerGenerator._logger_count}_{logger_name}")
        logger.setLevel(level=log_level)
        LoggerGenerator._logger_count += 1

        # create formatter and add it to the handlers
        log_format = '[%(asctime)s %(name)s %(levelname)s] %(message)s [%(pathname)s:%(lineno)d in %(funcName)s]'
        formatter = logging.Formatter(log_format)

        if write_file:
            # create file handler for logger.
            log_file_path = LoggerGenerator.LOGS_FOLDER_PATH / f"{logger_name}.log"
            fh = logging.FileHandler(log_file_path)
            fh.setLevel(level=log_level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        # create console handler for logger.
        ch = logging.StreamHandler()
        ch.setLevel(level=log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger


try:  # create logs folder
    os.makedirs(LoggerGenerator.LOGS_FOLDER_PATH)
except FileExistsError:
    pass
