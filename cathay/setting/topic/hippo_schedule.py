from __future__ import print_function
from __future__ import unicode_literals

import logging
from cathay_time_utils.time_utils import TimeUtils

from basic import BasicMessage

logger = logging.getLogger(__name__)


class HippoSchedule:

    def __init__(self, name):
        self.name = name

    def msg_handler(self, msg):
        return Message(msg)


class Message(BasicMessage):

    def __init__(self, msg):
        super(Message, self).__init__(msg)

    def match(self, pattern):
        logger.debug("receive message: {}".format(self.msg))
        logger.debug("pattern: {}".format(pattern))

        if self.msg.get('hippo_name') == pattern['hippo_name'] and \
                self.msg.get('job_name') == pattern['job_name']:
            logger.info("schedule submit the job !!")
            return True

        return False
