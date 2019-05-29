#!/bin/sh

# No arguments : creates folder 'vision_logs' in current directory
# Argument 1 : ip address of the robot containing the logs
# Argument 2 : dst folder for logs

HOST="10.0.0.1"

OUTPUT_DIR="vision_logs"
if [ $# -gt 0 ]
then
    HOST=$1
fi
if [ $# -gt 1 ]
then
    OUTPUT_DIR=$2
fi

HOST="rhoban@${HOST}"

# Retrieving robot hostname
ROBOT=$(ssh $HOST hostname)
    
OUTPUT_DIR=$OUTPUT_DIR'/'${ROBOT}

LOG_PATH="/home/rhoban/env/${ROBOT}/manual_logs/"

# If the folder exist copy it
if ssh $HOST [ -d $LOG_PATH ]
then
    mkdir -p ${OUTPUT_DIR}
    # copy files in dir
    scp -r ${HOST}:${LOG_PATH}/* ${OUTPUT_DIR}
    # delete files on robot
    # ssh ${HOST} "rm -rf ${LOG_PATH}"
else
    echo "${LOG_PATH} not found on ${HOST}"
    exit -1
fi


