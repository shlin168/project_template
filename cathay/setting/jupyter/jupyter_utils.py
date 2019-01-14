import os
import re
import pickle

import logging
logger = logging.getLogger(__name__)


def get_jupyter_dir(configs, app_home):
    jupyter_dir = configs.get('jupyter.job.dir')
    return os.path.join(app_home, jupyter_dir)


def rm_jupyter_history(configs, app_home):
    joutput_re = configs.get('jupyter.job.output_re')
    jkeep_history = configs.get('jupyter.files.keep_history')

    if jkeep_history < 1:
        raise ValueError('jupyter history files should be at least 1')

    # rm old *.ipynb
    jupyter_path = get_jupyter_dir(configs, app_home)
    regex = re.compile(joutput_re)
    match_files = filter(regex.match, os.listdir(jupyter_path))
    rm_files_amount = len(match_files) - jkeep_history
    if rm_files_amount > 0:
        for f in sorted(match_files)[:rm_files_amount]:
            logger.warning('rm old jupyter file: {}'.format(f))
            os.remove(os.path.join(jupyter_path, f))


def dump_configs(configs, app_home):
    # save config to .pkl for jupyter to use
    config_pkl_path = configs.get('jupyter.config.save_pkl')
    with open(os.path.join(app_home, config_pkl_path), 'wb') as f:
        pickle.dump(configs, f)
