from __future__ import print_function
from __future__ import unicode_literals

from pyhocon import ConfigFactory, ConfigTree


class Configger(object):

    __config_path = ''
    __conf = None

    @classmethod
    def path(cls, val):
        cls.__config_path = val
        cls.__conf = ConfigFactory.parse_file(val)

    @classmethod
    def get_config(cls):
        return cls.__conf

    @staticmethod
    def merge_configs(confs):
        configs = ConfigTree()
        for config in confs:
            # Merge config into configs
            configs = ConfigTree.merge_configs(configs, config)
        return configs
