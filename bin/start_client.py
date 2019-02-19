from __future__ import print_function

import SimpleHTTPServer
import SocketServer
import sys
import traceback
import logging
import click

from cathay.setting.config.config_utils import merge_env_configs
from cathay.setting.client.submit_client import SubmitClient

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--conf', help='config')
def receive(conf):
    logger.info("======== Start Submit Client ========")

    # load configs
    logger.info("Load configs...")
    configs = merge_env_configs(conf)

    # kafka client
    logger.info("Start submit client...")
    try:
        submitClient = SubmitClient(config=configs)
        submitClient.start()
    except Exception:
        logger.error(traceback.format_exc())
        exit(2)

    # start a server
    logger.info("Start a server...")
    try:
        CLIENT_HOST = configs.get('client.host')
        CLIENT_PORT = configs.get('client.port')

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((CLIENT_HOST, CLIENT_PORT), Handler)
        logger.info("Serving client app at port: {}".format(CLIENT_PORT))
        httpd.serve_forever()
    except:
        logger.error(traceback.format_exc())
        exit(2)

    logger.info("======== Finish ========")


if __name__ == '__main__':
    receive()
