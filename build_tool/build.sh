# !/bin/bash
export APP_HOME="$(
    cd "$(dirname "$0")"/..
    pwd
)"
export APP_NAME="$(basename $APP_HOME)"

. "${APP_HOME}/conf/default.conf"

# include log manipulation script start
. "${APP_HOME}"/libexec/log.sh
# include log manipulation script end

. "${APP_HOME}"/libexec/str-parser.sh
. "${APP_HOME}"/build_tool/build-utils.sh

LIB_PATH="${APP_HOME}"/lib

function usage() {
    echo "[Installation]
    Usage: $(basename $0) [OPTIONS] ENV (dev|ut|uat|prod)
     e.g. $(basename $0) -p dev
    OPTIONS:
       -h|--help                             Show this message
       -b|--build                            Build project
       -c|--clean                            Clean build result (venv)
       -r|--rebuild                          Rebuild Project, Clean and Build
       -p|--python                           Python version (Default:2) e.g. --python 2.7
       -d|--clean-deps                       Clean dependences from dist, build, egg_info folder
       -t|--test                             Execute test case, use \"{pytest-args}\" to pass to pytest, e.g. -t\"-s -v\" or --test=\"-s -v\"
       -s|--skip-build                       Skip build project stage when run Test command
    "
}

args=$(getopt -o hrbcdst::p: --long build,clean,rebuild,clean-deps,skip-build,test::,python:,help \
    -n 'build.sh' -- "$@")

if [ $? != 0 ]; then
    echo "terminating..." >&2
    exit 1
fi
eval set -- "$args"

while true; do
    case "$1" in
    -b | --build)
        BUILD_OPT="true"
        shift
        ;;
    -c | --clean)
        CLEAN_OPT="true"
        shift
        ;;
    -r | --rebuild)
        BUILD_OPT="true"
        CLEAN_OPT="true"
        shift
        ;;
    -p | --python)
        PYTHON_VERSION="$2"
        shift 2
        ;;
    -d | --clean-deps)
        CLEAN_DEPS_OPT="true"
        shift
        ;;
    -t | --test)
        TEST_OPT="true"
        case "$2" in
        "")
            TEST_ARGS=''
            shift 2
            ;;
        *)
            TEST_ARGS=$2
            shift 2
            ;;
        esac
        ;;
    -s | --skip-build)
        SKIP_BUILD_OPT="true"
        shift
        ;;
    -h | --help)
        usage
        exit
        ;;
    --)
        shift
        break
        ;;
    *)
        echo "internal error!"
        exit 1
        ;;
    esac
done

for arg; do
    ENV=$arg
done

# check for required args
if [[ -z ${ENV} ]] && ([[ -n ${BUILD_OPT} ]] || [[ -n ${TEST_OPT} ]]); then
    echo "$(basename $0): missing ENV : ${ENV}"
    usage
    exit 1
fi

. "${APP_HOME}/build_tool/build.conf"

function build_project() {
    test_mode=$1
    if [[ -z "$test_mode" ]]; then
        test_mode=false
    fi

    # check exists for ENV variable and config
    if [[ -z ${ENV} ]]; then
        echo "$(basename $0): missing ENV : ${ENV}"
        usage
        exit 1
    fi

    log_info "Start to build project"

    env_config="${APP_HOME}/conf/env.conf"
    log_info "write ${ENV} to ENV arg in $env_config"
    grep -q "^ENV" "$env_config" && sed_command "s/^ENV.*/ENV=\\\"${ENV}\\\"/" "$env_config"

    build_py_project_func "${PYTHON_VERSION}" "${test_mode}"
}

function clean_project() {
    clean_deps
    log_info "Start to clean project"
    clean_project_func
}

function clean_deps() {
    log_info "Start to remove dependencies"
    clean_py_deps_func
}

function test_case() {
    if [[ -z $SKIP_BUILD_OPT ]]; then
        log_info "Start to build project by execute test case"
        build_project true
    fi
    log_info "Start to execute test case"
    . "${APP_HOME}/conf/default.conf"
    . "${APP_HOME}/conf/env.conf"
    . "${APP_HOME}/conf/runtime-env-info.sh"
    . "${APP_HOME}/libexec/run-py-venv.sh"
    test_case_py_func "$TEST_ARGS" "$SKIP_BUILD_OPT"
}
# call function

if [[ -n $CLEAN_OPT ]]; then
    clean_project
fi

if [[ -n $BUILD_OPT ]]; then
    build_project
fi

if [[ -n $CLEAN_DEPS_OPT ]]; then
    clean_deps
fi

if [[ -n $TEST_OPT ]]; then
    test_case
fi
