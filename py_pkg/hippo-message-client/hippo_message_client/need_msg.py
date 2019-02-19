from __future__ import print_function
from __future__ import unicode_literals

import time


class NeedMsgQueue(object):

    def __init__(self, name, msgs=[]):
        self.name = name
        self.msgs = msgs

    def refresh(self):
        for msg in self.msgs:
            msg.refresh()

    def show(self):
        return "Queue:\n" + "\n".join(["need_msg[{}]: {}".format(idx, msg) for idx, msg in enumerate(self.msgs)])

    def check_status(self):
        now = int(time.time())
        for msg in self.msgs:
            # check timeout
            if now > msg.timeout:
                msg.status = False


class NeedMsg(object):

    def __init__(self, pattern):
        self.refresh()
        self.pattern = pattern
        try:
            self.frequency = pattern.get("frequency")
        except:
            # default
            self.frequency = "D"

    def __str__(self):
        return "status={}, frequency={}, timeout={}, receive_time={}, pattern={}" \
            .format(self.status, self.frequency, self.timeout, self.receive_time, self.pattern)

    def refresh(self):
        self.status = False
        self.receive_time = []
        self.timeout = -1
