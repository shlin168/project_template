from __future__ import print_function
from __future__ import unicode_literals

import logging

from cathay_time_utils.time_utils import TimeUtils

from basic import BasicMessage

logger = logging.getLogger(__name__)


class HippoFinish:

    def __init__(self, name):
        self.name = name

    def msg_handler(self, msg):
        return Message(msg)


class Message(BasicMessage):

    def __init__(self, msg):
        super(Message, self).__init__(msg)
        self.offset_sec = 7200
        self.offset_day = 2

    def match(self, pattern):
        logger.debug("receive message: {}".format(self.msg))
        logger.debug("pattern: {}".format(pattern))

        # TODO write code for check(mapping) receive and need message.
        '''
            example message:
                self.msg : receive message (from kafka)
                            ex: {"job_id": "job0",
                                "finish_time": 1531747697,
                                "duration_time": 5831,
                                "hippo_name": "hn0",
                                "is_success": true,
                                "job_name": "jn0"
                                }
                pattern : pattern (from hippo.conf)
                            ex: {topic:hippo-finish, hippo_name:hn0, job_name:jn0}

            example code:
                self.msg.get('hippo_name') == need_msg['hippo_name']
                self.msg.get('job_name') == need_msg['job_name']
        '''
        if self.msg['is_success']:
            if self.msg.get('hippo_name') == pattern['hippo_name'] and \
                    self.msg.get('job_name') == pattern['job_name']:
                logger.debug("Get this message.")
                return True

        logger.debug("Pass this message.")
        return False

    def set_timeout(self, frequency):
        timeout = super(Message, self).set_timeout(frequency)
        if frequency == "D":
            return timeout - self.offset_sec
        elif frequency == "M":
            return timeout - self.offset_sec + (self.offset_day * 24 * 60 * 60)
