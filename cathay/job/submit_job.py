import logging
logger = logging.getLogger(__name__)


class SubmitJob(object):

    def __init__(self, config):
        self.config = config

    def start(self):
        try:
            logger.info(self.config.get('hippo.name'))
            # TODO write code for the job

        except Exception:
            raise
