import os
import logging
import papermill as pm

from cathay_time_utils import TimeUtils

from cathay.job.submit_job import SubmitJob
from cathay.setting.jupyter import get_jupyter_dir, rm_jupyter_history, dump_configs

logger = logging.getLogger(__name__)


class SubmitJupyterJob(SubmitJob):

    def __init__(self, config):
        super(SubmitJupyterJob, self).__init__(config)
        self.app_home = os.environ['APP_HOME']

    def jupyter_preprocess(self):
        # rm old jupyter *.ipynb
        rm_jupyter_history(self.config, self.app_home)

        # dump config to .pkl for jupyter to use
        dump_configs(self.config, self.app_home)

    def start(self):
        try:
            # get jupyter config
            self.jupyter_preprocess()
            jupyter_path = get_jupyter_dir(self.config, self.app_home)
            jexec_file = self.config.get('jupyter.job.exec_file')
            joutput_prefix = self.config.get('jupyter.job.output_prefix')

            logger.info("Start submit jupyter job...")
            date = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y-%m-%d')
            yyyymm = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y%m')
            db_tbl = 'test'
            pm.execute_notebook(
                os.path.join(jupyter_path, jexec_file),
                os.path.join(jupyter_path, '{}_{}.ipynb'.format(joutput_prefix, date)),
                parameters=dict(yyyymm=yyyymm, db_tbl=db_tbl)
            )
        except Exception:
            raise
