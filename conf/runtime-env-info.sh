#echo "this script is for runtime environment check "

# what might be interested:
# network
# memory
# build path
# dependency
# whoami
# service version, like Impala, Hive, HBase....
# language version, like Python, JDK, R, Scala


if [[ "${ENV}" == "prod" ]]; then
    # == HADOOP + SPARK ==
    export HADOOP_CONF_DIR=/source/hadoop/conf
    export SPARK_HOME=/etc/spark-2.3.1-bin-hadoop2.6
    export PATH=$SPARK_HOME/bin:$PATH
    export PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH

elif [[ "${ENV}" == "uat" ]]; then
    # == HADOOP + SPARK ==
    export HADOOP_CONF_DIR=/source/hadoop/conf
    export SPARK_HOME=/etc/spark-2.3.1-bin-hadoop2.6
    export PATH=$SPARK_HOME/bin:$PATH
    export PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH

elif [[ "${ENV}" == "ut" ]]; then
    # == HADOOP + SPARK ==
    export HADOOP_CONF_DIR=/etc/hadoop/conf
    export SPARK_HOME=/opt/spark-2.3.1-bin-hadoop2.6
    export PATH=$SPARK_HOME/bin:$PATH
    export PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH

elif [[ "${ENV}" == "dev" ]]; then
    # == HADOOP + SPARK ==
    export HADOOP_CONF_DIR=
    export SPARK_HOME=/usr/local/spark-2.3.0-bin-hadoop2.6
    export PATH=$SPARK_HOME/bin:$PATH
    export PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH

else

    log_info "ENV: '${ENV}' not found!"
    exit 2

fi
