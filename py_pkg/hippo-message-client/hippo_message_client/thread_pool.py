from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import json
import logging
from concurrent import futures

from basic import BasicClient

logger = logging.getLogger(__name__)


class ThreadPoolClient(BasicClient):

    def __init__(self, config, max_workers):
        super(ThreadPoolClient, self).__init__(config)
        self.executor = futures.ThreadPoolExecutor(max_workers=max_workers)
        # consumer
        self.start_consumer()

    def run(self):
        for message in self.consumer:
            try:
                js_value = json.loads(message.value)
                if self.should_submit(js_value, message):
                    command = self.parse_value(js_value)
                    self.executor.submit(self.call_job_on_system, command)
            except Exception as e:
                logger.error('Error:')
                logger.error(e)
