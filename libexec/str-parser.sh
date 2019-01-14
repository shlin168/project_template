#!/bin/bash

function sed_command(){
    # sed command is different in Linux and MacOS, so we need this function
    os=$(uname -s)
    if [ $os == "Linux" ]; then
        sed -i $1 $2
    elif [ $os == "Darwin" ]; then
        sed -i '' $1 $2
    fi
}