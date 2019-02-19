#!/bin/sh
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
. "${APP_HOME}/conf/default.conf"
. "${APP_HOME}/conf/env.conf"
. "${APP_HOME}/conf/runtime-env-info.sh"
. "${APP_HOME}/libexec/run-py-venv.sh"

START_PATH=${APP_HOME}/bin/start_client.py

CONF_PATH_CLIENT=${APP_HOME}/conf/client.conf
CONF_PATH_HIPPO=${APP_HOME}/conf/hippo.conf
CONF_PATH_JOB=${APP_HOME}/conf/job.conf
CONF_PATH=${CONF_PATH_CLIENT}:${CONF_PATH_HIPPO}:${CONF_PATH_JOB}

cd ${APP_HOME}

export APP_TYPE="client"

# from env.conf
export ENV=${ENV}

python ${START_PATH} -c ${CONF_PATH}