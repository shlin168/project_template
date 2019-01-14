import os
import logging

from cathay_spark import get_spark

from cathay.setting.config.config_utils import get_full_keys

logger = logging.getLogger(__name__)


class SparkSession(object):

    spark = None
    mode = None

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

    def _init_spark_session(self):
        '''
            init spark session from default base config
        '''
        logger.info('get spark session, mode: {} ...'.format(self.mode))
        self.spark = get_spark(self.app_name, self.mode)

    def _set_spark_session_conf(self):
        '''
            set spark session from conf/spark.conf
        '''
        logger.info('set spark configuration ...')
        spark_configs = get_full_keys(self.config.get("spark", None), "spark")

        for k, v in spark_configs.items():
            logger.info("{} = {}".format(k, v))
            self.spark.conf.set(k, v)

    def set_spark_session(self):
        if self.config is None:
            self._set_config()
        self._set_spark_mode()
        self._set_spark_app_name()
        self._init_spark_session()
        self._set_spark_session_conf()

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
