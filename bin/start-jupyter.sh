#!/bin/sh
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"

. "${APP_HOME}/conf/default.conf"
. "${APP_HOME}/conf/env.conf"
. "${APP_HOME}/conf/runtime-env-info.sh"
. "${APP_HOME}/libexec/run-py-venv.sh"
. "${APP_HOME}/libexec/hocon-parser.sh"

if [[ -d ${PY_VENV} ]]; then
    PYTHONPATH=${PY_VENV}/lib/python2.7/site-packages/:$PYTHONPATH
fi

SET_CONFIG_PATH=${APP_HOME}/bin/start_jupyter.py

CONF_PATH_JOB=${APP_HOME}/conf/job.conf
CONF_PATH_SPARK=${APP_HOME}/conf/spark.conf
CONF_PATH_JUPYTER=${APP_HOME}/conf/jupyter.conf
CONF_PATH=${CONF_PATH_JOB}:${CONF_PATH_SPARK}:${CONF_PATH_JUPYTER}

cd ${APP_HOME}

export APP_TYPE="jupyter"

export ENV=${ENV}

python ${SET_CONFIG_PATH} -c ${CONF_PATH} $@

jupyter notebook --ip 0.0.0.0 --port 5678
