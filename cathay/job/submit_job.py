import logging
logger = logging.getLogger(__name__)


class SubmitJob(object):

    def __init__(self, config, exec_date):
        self.config = config
        self.exec_date = exec_date

    def start(self):
        try:
            logger.info(self.config.get('hippo.name'))
            logger.info('exec_date: {}'.format(self.exec_date))
            # TODO write code for the job

        except Exception:
            raise
