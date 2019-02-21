import sys
import traceback

import click
import logging
from cathay_time_utils.time_utils import TimeUtils

from cathay.setting.config.config_utils import merge_env_configs
from cathay.job.submit_spark_job import SubmitSparkJob as SubmitJob

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

today = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y-%m-%d')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--conf', help='config')
@click.option('-d', '--exec-date', default=today, help='execution date, default {}, format:YYYY-MM-DD'.format(today))
def receive(conf, exec_date):
    # check input date
    try:
        TimeUtils.validate_dtfmt(exec_date, fmt='%Y-%m-%d')
    except:
        raise

    try:
        logger.info("======== Start Submit Job ... ========")
        start = TimeUtils.get_now('ts')

        # load configs
        logger.info("Load configs...")
        configs = merge_env_configs(conf)

        # job
        logger.info("Start submit job...")
        submitJob = SubmitJob(config=configs, exec_date=exec_date)
        submitJob.start()

        end = TimeUtils.get_now('ts')
        execution_time = end - start
        logger.info(
            "======== Successfully! Execution time: {} sec ========".format(execution_time))
        logger.info(
            "======== Execution time: {}  ========".format(TimeUtils.cvt_second2timeformat(execution_time)))

    except Exception:
        logger.error(traceback.format_exc())
        exit(2)


if __name__ == '__main__':
    receive()
