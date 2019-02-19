from __future__ import print_function
from __future__ import unicode_literals

import logging
from cathay_jinja.jinja_injector import JinjaInjector

from cathay_time_utils.time_utils import TimeUtils

from basic import BasicMessage

logger = logging.getLogger(__name__)


class FrontierAdw:

    def __init__(self, name):
        self.name = name

    def msg_handler(self, msg):
        """
        :type msg: dict object
        """
        return Message(msg)


class Message(BasicMessage):

    def __init__(self, msg):
        super(Message, self).__init__(msg)
        self.offset_sec = 7200
        self.offset_day = 2

    def _get_exec_partition(self):
        offset_date = TimeUtils.add_second(
            TimeUtils.get_now(), int(self.offset_sec))
        exec_dt = TimeUtils.cvt_datetime(TimeUtils.add_day(offset_date, -(self.offset_day)))

        logger.info("exec_partition = {}".format(exec_dt))
        return exec_dt

    def match(self, pattern):
        logger.debug("receive message: {}".format(self.msg))
        logger.debug("pattern: {}".format(pattern))

        # TODO write code for check(mapping) receive and need message.
        '''
            example message:
                self.msg : receive message (from kafka)
                           ex: {"exec_date": 1531747697,
                                "partition_values": ["201807"],
                                "db": "btd",
                                "partition_fields": ["yyyymm"],
                                "table": "agreement_drv_pln_apply_m",
                                "method": "overwrite_partition"
                                }
                pattern : pattern (from hippo.conf)
                        ex: {frequency:D, topic:frontier-adw, db:btd, table:agreement_drv_pln_apply_m, partition_values:%(yyyymm)}

            example code:
                self.msg.get('db') == need_msg['db']
        '''
        if self.msg.get('db') == pattern['db'] and self.msg.get('table') == pattern['table']:

            # check partition_values
            expected_value = JinjaInjector.string_render_args(
                content=pattern['partition_values'], yyyymm=self._get_exec_partition())

            logger.info("expected partition value: {}".format(expected_value))

            if self.msg.get('partition_values')[0] == expected_value:
                logger.info("Get this message.")
                logger.info("pattern['partition_values'] render after: {}".format(expected_value))
                return True

        logger.debug("Pass this message.")
        return False

    def set_timeout(self, frequency):
        timeout = super(Message, self).set_timeout(frequency)
        if frequency == "D":
            return timeout - self.offset_sec
        elif frequency == "M":
            return timeout - self.offset_sec + (self.offset_day * 24 * 60 * 60)
