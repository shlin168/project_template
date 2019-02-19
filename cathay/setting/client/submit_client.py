from __future__ import print_function
from __future__ import unicode_literals

import json
import subprocess
import traceback
import logging

from cathay_time_utils.time_utils import TimeUtils
from hippo_message_client.fsm import FSMClient

from cathay.setting.topic import topic_factory
from cathay.setting.topic import HippoSchedule

logger = logging.getLogger(__name__)

# Aim to collect all the required messages before submit job


class SubmitClient(FSMClient):

    def __init__(self, config):
        super(SubmitClient, self).__init__(config)
        self.spark_script = config.get('spark.bash_path')
        self.test_mode = config.get('option.test_mode')
        self.job_name = config.get('job.name')

        if self.test_mode:
            logger.debug(
                "====================== Test Mode ======================")

    # check schedule submit the job
    def schedule_submit(self, js_value, message):
        if message.topic.endswith('hippo-schedule'):
            topic = HippoSchedule(message.topic)
            msg_handler = topic.msg_handler(js_value)
            return msg_handler.match(
                {
                    "hippo_name": self.hippo_name,
                    "job_name": self.job_name
                }
            )

        return False

    # check received message context is need by topic
    def should_submit(self, js_value, message):
        # check the new message.topic is subscribed
        for sub_topic_name in self.sub_topics:
            if message.topic.endswith(sub_topic_name):
                topic = topic_factory(sub_topic_name)
                for need_msg in [need_msg for need_msg in self.need_msgs.msgs
                                 if need_msg.pattern.get('topic').endswith(message.topic)]:
                    msg_handler = topic.msg_handler(js_value)

                    # check pattern
                    if msg_handler.match(need_msg.pattern):
                        need_msg.status = True
                        need_msg.receive_time.append(TimeUtils.get_now('ts'))
                        need_msg.timeout = msg_handler.set_timeout(
                            need_msg.frequency)
                        return True

        return False

    def basic_job_msg(self):
        basic_msg = super(SubmitClient, self).basic_job_msg()
        basic_msg['job_name'] = self.job_name
        basic_msg['job_id'] = self.job_id
        return basic_msg

    # send kafka message when job start
    def pub_job_start(self):
        logger.info("send pub_job_start.")

        self.job_start = self.basic_job_msg()
        self.job_start['start_time'] = TimeUtils.get_now('ts')

        logger.info("pub_job_start: {}".format(json.dumps(self.job_start)))

        self.producer.send(self.start_topic, json.dumps(self.job_start))

    # send kafka message when job finish
    def pub_job_finish(self, code):
        logger.info("send pub_job_finish.")

        self.job_finish = self.basic_job_msg()
        self.job_finish['is_success'] = code == 0
        self.job_finish['finish_time'] = TimeUtils.get_now('ts')
        self.job_finish['duration_time'] = self.job_finish['finish_time'] - \
            self.job_start['start_time']

        logger.info("pub_job_finish: {}".format(json.dumps(self.job_finish)))

        self.producer.send(self.finish_topic, json.dumps(self.job_finish))

    # call the job when all messages are received
    def call_job_on_system(self):
        self.job_id = '{}_{}'.format(self.job_name, TimeUtils.get_now('ts'))
        self.pub_job_start()

        if self.test_mode:
            code = 0
        else:
            logger.info("call spark job. (job_id = {})".format(self.job_id))
            code = subprocess.call([
                '/bin/sh',
                self.spark_script
            ])

        self.pub_job_finish(code)

    def receive_msg(self, msg):
        self.need_msgs.check_status()
        super(SubmitClient, self).receive_msg(msg)

    def run(self):
        while True:
            self.start_consumer()
            for message in self.consumer:
                try:
                    js_value = json.loads(message.value)
                    if self.schedule_submit(js_value, message):
                        self.consumer.close()
                        self.call_job_on_system()
                        break

                    if self.should_submit(js_value, message):
                        self.receive_msg(message.value)

                    if self.state == 'submitting':
                        self.consumer.close()
                        self.submit_job()
                        break
                except Exception:
                    logger.error(traceback.format_exc())
