import os
import click

from cathay.setting.config.config_utils import merge_env_configs
from cathay.setting.jupyter.jupyter_utils import dump_configs


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--conf', help='config')
def receive(conf):
    configs = merge_env_configs(conf)
    dump_configs(configs, os.environ['APP_HOME'])


if __name__ == '__main__':
    receive()
