import os
import logging

from cathay.setting.config.config_utils import load_config
from cathay.setting.spark.spark_session import SparkSession

logger = logging.getLogger(__name__)


class JupyterSparkSession(SparkSession):

    def __init__(self):
        super(JupyterSparkSession, self).__init__()

    def _set_config(self):
        self.config = load_config()

    def _set_spark_app_name(self):
        super(JupyterSparkSession, self)._set_spark_app_name()
        if os.environ['APP_TYPE'] == 'jupyter':
            self.app_name = '{prefix}-{app_name}'.format(
                prefix=self.config.get('jupyter.test.prefix'), app_name=self.app_name)
