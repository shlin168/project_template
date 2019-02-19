from frontier_adw import FrontierAdw
from hippo_finish import HippoFinish
from hippo_schedule import HippoSchedule

from basic import BasicMessage


def topic_factory(topic_name):
    if topic_name.endswith('frontier-adw'):
        topic = FrontierAdw
    elif topic_name.endswith('hippo-finish'):
        topic = HippoFinish
    else:
        raise ValueError('No kafka topic.')

    return topic(topic_name)
