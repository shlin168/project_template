#!/bin/sh
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"

. "${APP_HOME}"/libexec/log.sh

. "${APP_HOME}/conf/default.conf"
. "${APP_HOME}/conf/env.conf"
. "${APP_HOME}/conf/runtime-env-info.sh"
. "${APP_HOME}/libexec/run-py-venv.sh"

START_PATH=${APP_HOME}/bin/start_job.py

CONF_PATH_JOB=${APP_HOME}/conf/job.conf
CONF_PATH_SPARK=${APP_HOME}/conf/spark.conf
CONF_PATH=${CONF_PATH_JOB}:${CONF_PATH_SPARK}

cd ${APP_HOME}

if [[ -z $APP_TYPE ]] ; then
    APP_TYPE="job"
fi
export APP_TYPE

# from env.conf
export ENV=${ENV}

python ${START_PATH} -c ${CONF_PATH} $@
