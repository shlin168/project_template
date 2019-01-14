import time
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class Timer(object):
    '''
        Use for timing certain code block.
        Example:
            with Timer("your_text"):
                ...
    '''

    def __init__(self, text=None):
        self.text = text

    def __enter__(self):
        self.time = time.time()
        if self.text:
            logger.info("=== {} ===".format(self.text))
        return self

    def __exit__(self, *args):
        if self.text:
            logger.info("=== exec time: {} ===".format(
                timedelta(seconds=time.time() - self.time)))
