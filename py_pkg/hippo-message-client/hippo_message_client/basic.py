from __future__ import print_function
from __future__ import unicode_literals

import time
import json
from threading import Thread
from kafka import KafkaConsumer, KafkaProducer

from need_msg import NeedMsgQueue, NeedMsg
from persistence import Persistence


class BasicClient(Thread):
    daemon = True

    def __init__(self, config):
        Thread.__init__(self)
        self.config = config

        # hippo
        self.hippo_name = config.get('hippo.name')
        self.sub_topics = config.get('hippo.subscribe_topic')
        self.start_topic = config.get('hippo.start_topic')
        self.finish_topic = config.get('hippo.finish_topic')

        persist_need_msgs = Persistence.load("need_msgs")
        if persist_need_msgs is not None:
            self.need_msgs = persist_need_msgs
        else:
            self.need_msgs = NeedMsgQueue(self.hippo_name, [NeedMsg(hippo_msg)
                                                            for hippo_msg in config.get('hippo.msg')])

        # kafka
        self.kafka_host = config.get('kafka.bootstrap_servers')
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_host)

        # hippo msg
        self.hippo_start = None
        self.hippo_finish = None

    def start_consumer(self):
        self.consumer = KafkaConsumer(bootstrap_servers=self.kafka_host,
                                      auto_offset_reset='latest',
                                      group_id=self.hippo_name)
        self.consumer.subscribe(self.sub_topics + ["hippo-schedule"])

    def should_submit(self, js_value, message):
        raise NotImplementedError

    def parse_value(self, js_value):
        return js_value

    def call_job_on_system(self, command):
        raise NotImplementedError

    def basic_job_msg(self):
        basic_msg = {
            'hippo_name': self.hippo_name
        }
        return basic_msg

    def run(self):
        while True:
            self.start_consumer()
            for message in self.consumer:
                try:
                    js_value = json.loads(message.value)
                    if self.should_submit(js_value, message):
                        command = self.parse_value(js_value)
                        self.consumer.close()
                        self.call_job_on_system(command)
                        break
                except Exception as e:
                    print('Error:')
                    print(e)
