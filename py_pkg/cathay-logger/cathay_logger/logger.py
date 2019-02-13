from __future__ import print_function
from __future__ import unicode_literals

import logging
from logging import config


class Logger(object):

    def __init__(self, config_path='logging_config.ini'):
        self.config_path = config_path

    def __set_log_config(self, logfilename):
        logging.logfilename = logfilename
        config.fileConfig(
            self.config_path, disable_existing_loggers=False)

    def get_logger(self, logfilename, template_name='root', extra={}):
        self.__set_log_config(logfilename)
        return logging.LoggerAdapter(logging.getLogger(template_name), extra)
