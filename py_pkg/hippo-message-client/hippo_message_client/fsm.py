from __future__ import print_function
from __future__ import unicode_literals

import time
import logging

from transitions import Machine
from threading import Timer

from basic import BasicClient
from persistence import Persistence

logger = logging.getLogger(__name__)
# Aim to collect all the required messages before submit job


class FSMClient(BasicClient):
    states = ['idle', 'waiting', 'submitting']

    def __init__(self, config, wait_secs=None):
        super(FSMClient, self).__init__(config)

        # fsm related
        persist_curr_msgs = Persistence.load("curr_msgs")
        if persist_curr_msgs is not None:
            self.curr_msgs = persist_curr_msgs
        else:
            self.curr_msgs = []
        self.machine = Machine(model=self, states=self.states, initial='idle')

        # timeout
        self.timer = None
        self.wait_secs = wait_secs

        # idle -> waiting
        self.machine.add_transition(
            'new_msg', '*', 'waiting', conditions=['shoud_wait'], after='refresh_timer')
        self.machine.add_transition(
            'new_msg', '*', 'submitting', conditions=['is_ready'])
        self.machine.add_transition('finish', '*', 'idle', after='refresh')

    def stop_timer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def on_timeout(self):
        logger.info('timeout!!')
        self.finish()

    def refresh_timer(self):
        self.stop_timer()
        if self.wait_secs is not None:
            self.timer = Timer(self.wait_secs, self.on_timeout)
            self.timer.start()

    def shoud_wait(self):
        return len([need_msg for need_msg in self.need_msgs.msgs if not need_msg.status]) > 0

    def is_ready(self):
        return len([need_msg for need_msg in self.need_msgs.msgs if not need_msg.status]) == 0

    def refresh(self):
        self.stop_timer()
        self.curr_msgs = []
        self.need_msgs.refresh()

    def receive_msg(self, msg):
        self.curr_msgs.append(msg)
        self.new_msg()

        self.print_status()
        self.__snapshot()

    def print_status(self):
        logger.info("state: {}, curr_msgs: {}".format(
            self.state, self.curr_msgs))
        logger.info(self.need_msgs.show())

    def submit_job(self):
        logger.info("call submit job ...")
        self.stop_timer()
        self.call_job_on_system()
        self.finish()
        logger.info("finish submit job .")

        self.__snapshot()

    def __snapshot(self):
        Persistence.save("need_msgs", self.need_msgs)
        Persistence.save("curr_msgs", self.curr_msgs)

    def run(self):
        while True:
            self.start_consumer()
            for message in self.consumer:
                m = message.value
                self.receive_msg(m)
                self.print_status()

                if self.state == 'submitting':
                    self.consumer.close()
                    self.submit_job()
                    break
