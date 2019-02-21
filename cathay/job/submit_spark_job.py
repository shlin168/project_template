import logging
from cathay_time_utils.time_utils import TimeUtils

from cathay.setting.spark.spark_session import SparkSession as CathaySparkSession
from cathay.job.submit_job import SubmitJob

logger = logging.getLogger(__name__)


class SubmitSparkJob(SubmitJob, CathaySparkSession):

    def __init__(self, config, exec_date):
        super(SubmitSparkJob, self).__init__(config, exec_date)

    def start(self):
        try:
            # set spark session, use it through self.spark
            self.set_spark_session()

            # ===  test start ===
            logger.info(TimeUtils.get_now())
            logger.info(self.config.get('hippo.name'))
            logger.info('exec_date: {}'.format(self.exec_date))
            # ===  test end ===

            # TODO load config

            # TODO write code for the job

        except Exception:
            raise
        finally:
            # close spark session
            self.close_spark_session()
