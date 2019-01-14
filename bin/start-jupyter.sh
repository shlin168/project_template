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

cd ${APP_HOME}

export APP_TYPE="jupyter"

export ENV=${ENV}

jupyter notebook --ip 0.0.0.0 --port 5678