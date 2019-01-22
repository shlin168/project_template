from __future__ import print_function
from __future__ import unicode_literals

from pyspark.sql import SparkSession


class SparkBuilder(object):

    spark_builder = None

    def __init__(self, app_name, mode, config=None):
        self.app_name = app_name
        self.mode = mode
        self.config = config

    def get_spark(self):
        # init spark session
        self.spark_builder = SparkSession \
            .builder \
            .appName(self.app_name) \
            .master(self.mode) \
            .enableHiveSupport() \
            .config('hive.exec.dynamic.partition.mode', 'nonstrict') \
            .config('spark.sql.parquet.compression.codec', 'uncompressed')

        # set spark config before SparkSession Object create
        self.set_extra_config()

        # create SparkSession object
        spark = self.spark_builder.getOrCreate()
        SparkBuilder.get_logger(spark)
        return spark

    def set_extra_config(self):
        if self.config:
            for k, v in self.config.items():
                self.spark_builder.config(k, v)

    @staticmethod
    def get_logger(spark):
        logger = spark.sparkContext._jvm.org.apache.log4j
        logger.LogManager.getLogger('org').setLevel(logger.Level.INFO)
        logger.LogManager.getLogger('akka').setLevel(logger.Level.ERROR)
        logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)

        return logger
