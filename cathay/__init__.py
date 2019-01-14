import os
import sys

if hasattr(sys, '_called_from_test'):
    # called from within a test run
    pass
elif os.environ['APP_TYPE'] == 'jupyter':
    pass
else:
    from cathay_logger import Logger

    __log_config_path = 'conf/logging_config.ini'

    __app_type = os.environ['APP_TYPE']

    Logger(__log_config_path).get_logger(__app_type, __name__)
