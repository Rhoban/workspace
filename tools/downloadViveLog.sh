#!/bin/sh

# No arguments : creates folder 'vision_logs' in current directory
# Argument 1 : path of directory where 'logs' are downloaded

HOST="rhoban@10.0.0.1"

OUTPUT_DIR="vive_logs"
VIVE_DIR='src/rhoban/vive_provider/logs/'

if [ $# -gt 0 ]
then
    OUTPUT_DIR=$1
fi

# Retrieving robot hostname
ROBOT=$(ssh $HOST hostname)
OUTPUT_DIR=$OUTPUT_DIR'/'${ROBOT}
LOG_PATH="/home/rhoban/env/${ROBOT}/manual_logs/"

# If the folder exist copy it
if ssh $HOST [ -d $LOG_PATH ]
then
    LAST_LOG=`ssh $HOST ls -c $LOG_PATH|head -n1`
    LAST_VIVE=`ls -c $VIVE_DIR|head -n1`

    echo "* Retrieving ${LAST_LOG} and ${LAST_VIVE}..."
    mkdir -p ${OUTPUT_DIR}
    # scp -r ${HOST}:${LOG_PATH}/${LAST_LOG} ${OUTPUT_DIR}
    cp ${VIVE_DIR}/$LAST_VIVE ${OUTPUT_DIR}/${LAST_LOG}/vive.bin
else
    echo "${LOG_PATH} not found on ${HOST}"
    exit -1
fi