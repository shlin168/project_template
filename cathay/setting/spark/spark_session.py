import os
import logging
import six

from cathay_spark import SparkBuilder

from cathay.setting.config.config_utils import get_full_keys

logger = logging.getLogger(__name__)


class SparkSession(object):

    spark = None
    mode = None
    spark_configs = None

    def __init__(self, config=None):
        self.config = config

    def _set_config(self):
        '''
            overwrite if reading config from elsewhere
        '''
        pass

    def _set_spark_app_name(self):
        '''
            overwrite if app name need to be changed
        '''
        assert self.config is not None, "config is None"
        self.app_name = self.config.get('hippo.name')

    def _set_spark_mode(self):
        '''
            overwrite if changing spark mode
        '''
        if os.environ['ENV'] == 'dev':
            self.mode = 'local'
        else:
            self.mode = 'yarn'

    def _set_spark_session_conf(self):
        '''
            set spark session from conf/spark.conf
        '''
        logger.info('set spark configuration ...')
        self.spark_configs = get_full_keys(self.config.get("spark", None), "spark")
        for key in self.spark_configs:
            if isinstance(self.spark_configs[key], six.string_types):
                self.spark_configs[key] = self.spark_configs[key].replace('$(APP_HOME)', os.environ['APP_HOME'])

    def _init_spark_session(self):
        '''
            init spark session from default base config
        '''
        logger.info('get spark session, mode: {} ...'.format(self.mode))
        sb = SparkBuilder(self.app_name, self.mode, self.spark_configs)
        self.spark = sb.get_spark()

    def _set_spark_logger(self):
        logger = SparkBuilder.get_logger(self.spark)

        # set custom log level after sparkSession create
        logger.LogManager.getRootLogger().setLevel(logger.Level.INFO)

    def set_spark_session(self):
        if self.config is None:
            self._set_config()
        self._set_spark_mode()
        self._set_spark_app_name()
        self._set_spark_session_conf()
        self._init_spark_session()
        self._set_spark_logger()

    def get_spark_session(self):
        if self.spark is None:
            self.set_spark_session()
        return self.spark

    def close_spark_session(self):
        logger.info('close spark session ...')
        if self.spark is not None:
            self.spark.stop()
        else:
            logger.warn('No such spark session')
