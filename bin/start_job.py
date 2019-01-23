import os
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


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--conf', help='config')
def receive(conf):
    logger.info("======== Start Submit Job ... ========")
    start = TimeUtils.get_now('ts')

    # load configs
    logger.info("Load configs...")
    configs = merge_env_configs(conf)

    # job
    logger.info("Start submit job...")
    try:
        submitJob = SubmitJob(config=configs)
        submitJob.start()
    except Exception:
        logger.error(traceback.format_exc())
        exit(2)

    end = TimeUtils.get_now('ts')
    execution_time = end - start
    logger.info(
        "======== Successfully! Execution time: {} sec ========".format(execution_time))
    logger.info(
        "======== Execution time: {}  ========".format(TimeUtils.cvt_second2timeformat(execution_time)))


if __name__ == '__main__':
    receive()
