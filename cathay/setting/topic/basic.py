from __future__ import print_function
from __future__ import unicode_literals

from cathay_time_utils.time_utils import TimeUtils


class BasicMessage(object):

    def __init__(self, msg):
        self.msg = msg

    def match(self, pattern):
        raise NotImplementedError

    def set_timeout(self, frequency):
        if frequency == "D":  # Daily
            # timeout is receive day
            return TimeUtils.cvt_datetime2timestamp(
                TimeUtils.get_now().replace(hour=23, minute=59, second=59))
        elif frequency == "M":  # Monthly
            # timeout is receive month
            return TimeUtils.cvt_datetime2timestamp(
                TimeUtils.add_month(TimeUtils.get_now(), 1).replace(day=1, hour=0, minute=0, second=0)) - 1
        else:
            raise ValueError('Frequency is none.')
