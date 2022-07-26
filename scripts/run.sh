#!/bin/bash
shopt -s xpg_echo
##################################
# Set default variables
filenametime1=$(date +"%m%d%Y%H%M%S")
##################################
# Set variables
export PYTHON_SCRIPT_NAME=$(cat config.toml | grep 'py_script' | awk -F"=" '{print $2}' | tr -d '"')
export SCRIPTS_FOLDER=$(pwd)
export LOGDIR=$SCRIPTS_FOLDER/log
export SHELL_SCRIPT_NAME='run'
export LOG_FILE=${LOGDIR}/${SHELL_SCRIPT_NAME}_${filenametime1}.log
##################################
# Go to script folder and run
cd ${SCRIPTS_FOLDER}

##################################
# Set log rules
exec > >(tee ${LOG_FILE}) 2>&1

##################################
# Run script
source sandbox/bin/activate

echo "Start to run Python script"
python3 ${SCRIPTS_FOLDER}/${PYTHON_SCRIPT_NAME}

RC1=$?
if [ ${RC1} != 0 ]; then
    echo "PYTHON RUNNNING FAILED"
    echo "[ERROR:] RETURN CODE: ${RC1}"
    echo "[ERROR:] REFER TO THE LOG FOR THE REASON FOR THE FAILURE"
    exit 1
fi

echo "PROGRAM SUCCEEDED"

deactivate

exit 0