# !/bin/bash

function get_value()
{
    # call example: get_value "conf/uat/job.conf" ".adw_monitor.output.local.file"
    config_path=$1
    key=$2
    cat $config_path | pyhocon -f json | jq $key
}