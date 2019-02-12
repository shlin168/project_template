# !/bin/bash

function build_basic_project_func() {
    cd "${APP_HOME}"
    log_info "[BUILD] mkdir $APP_HOME/var"
    mkdir -p $APP_HOME/var

    log_info "[BUILD] mkdir $APP_HOME/var/logs"
    mkdir -p $APP_HOME/var/logs
}

function build_py_project_func() {
    log_info "[BUILD] Start to build $APP_NAME "

    python_version=$1
    test_mode=$2

    build_basic_project_func

    if [[ -z $python_version ]]; then
        default_version=2
        log_warn "python_version arg is empty, default: $default_version"
        python_version=$default_version
    fi

    cd "${APP_HOME}"

    validate_python_rtn=$(validate_python_version_func $python_version)
    log_info "validate_python_rtn: $validate_python_rtn"
    if [[ $validate_python_rtn != 127 ]]; then

        install_virtualenv_func $python_version
        install_py_project_func $test_mode
    else
        log_error "validate python error!"
    fi

}

function validate_python_version_func() {
    python_version=$1

    python${python_version} -c 'import sys; print(sys.version_info[:])'
    echo $?
}

function install_virtualenv_func() {

    python_version=$1

    log_info "create python${python_version} venv : $PY_VENV"
    virtualenv -p python${python_version} --no-setuptools --no-wheel --never-download ${PY_VENV}

    # enter virtualenv
    source ${PY_VENV}/bin/activate

    log_info "upgrade pip in venv"

    ${PY_VENV}/bin/pip install --upgrade pip --disable-pip-version-check --no-cache-dir ${PIP_OPTS}

    log_info "install setuptools wheel in venv"
    ${PY_VENV}/bin/pip install setuptools wheel --disable-pip-version-check --no-cache-dir ${PIP_OPTS}

    # exit virtualenv
    deactivate

}

function install_py_project_func() {
    test_mode=$1
    # enter virtualenv
    source ${PY_VENV}/bin/activate
    cd ${APP_HOME}

    # install moudule in py_pkg
    log_info "install py_pkg by setup.py"
    py_pkg_path=${APP_HOME}/py_pkg
    python setup.py lib -p ${py_pkg_path} --pip-args="${PIP_OPTS}"

    # install moudule in main project
    log_info "install ${APP_NAME} by setup.py"
    cd ${APP_HOME}

    log_info "python setup.py install --pip-args=${PIP_OPTS}"
    python setup.py install --pip-args="${PIP_OPTS}"

    if [[ "$test_mode" == true ]]; then
        log_info "python setup.py extra --pip-args=${PIP_OPTS}"
        python setup.py extra --pip-args="${PIP_OPTS}"
    fi

    # exit virtualenv
    deactivate
}

function clean_py_deps_func() {
    # enter virtualenv
    source ${PY_VENV}/bin/activate
    # clean .egg folder or file
    log_info "run setup.py clean -e"
    cd ${APP_HOME}
    python setup.py clean -e
    # exit virtualenv
    deactivate
}

function clean_project_func() {

    if [ -d "$PY_VENV" ]; then
        log_info "[CLEAN] clean root project $APP_NAME, delete dir $PY_VENV"
        rm -rf "$PY_VENV"
    fi
}

function test_case_py_func() {
    pytest_args=$1
    skip_build=$2

    opt_test_args=""

    if [[ -n $skip_build ]]; then
        opt_test_args="--disable-check "$opt_test_args
    fi
    cd ${APP_HOME}

    printf "\E[0;33;40m ================= [pytest] Start ================== \n"
    log_info "python setup.py test --pytest-args="$pytest_args" $opt_test_args"
    python setup.py test --pytest-args="$pytest_args" $opt_test_args
    printf "\E[0;33;40m ================= [pytest] End ================== \n"

    printf "\E[0;33;40m ================= [flake8] Start ================== \n"
    flake8
    printf "\E[0;33;40m ================= [flake8] End ================== \n"
}
