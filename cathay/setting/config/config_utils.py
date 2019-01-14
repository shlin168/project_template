import os
import pickle
import traceback

from pyhocon import ConfigTree

import logging
from cathay_configger import Configger

logger = logging.getLogger(__name__)


def merge_env_configs(conf_paths):
    # load configs
    logger.info("Load configs...")
    try:
        confs = []
        for sub_conf in conf_paths.split(':'):
            Configger.path(sub_conf)
            confs.append(Configger.get_config())
    except Exception:
        logger.error("Parse config fail, please check your configurations.")
        raise

    else:
        # merge configs
        logger.info("Merge configs...")
        configs = Configger.merge_configs(confs)

        current_env = os.environ['ENV']
        merge_configs = get_config_by_env(configs, current_env)
        return merge_configs


def get_config_by_env(configs, current_env):
    try:
        common_configs = configs.get('common', ConfigTree())
        env_configs = configs.get(current_env)
        merge_configs = Configger.merge_configs([common_configs, env_configs])
        return merge_configs
    except Exception:
        logger.error(traceback.format_exc())
        logger.error("Fetch config by {} ENV error.".format(current_env))


def load_config():
    app_home = os.environ['APP_HOME']
    with open(os.path.join(app_home, 'var/config/config.pkl'), 'rb') as f:
        config = pickle.load(f)
    return config


def get_full_keys(conf, root=None):

    def dict_path(conf_dict, path=None, root=None):
        if path is None:
            if root is None:
                path = []
            else:
                path = [root]

        for k, v in conf_dict.iteritems():
            newpath = path + [k]
            if isinstance(v, dict):
                for u in dict_path(v, newpath):
                    yield u
            else:
                yield newpath, v

    spark_config = dict()
    if conf is None:
        logger.warn("conf is empty")
    else:
        for path, v in dict_path(conf_dict=conf, root=root):
            spark_config.setdefault('.'.join(path), v)

    return spark_config
