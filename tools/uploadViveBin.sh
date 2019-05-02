#!/bin/sh

# No arguments : creates folder 'vision_logs' in current directory
# Argument 1 : path of directory where 'logs' are downloaded

HOST="rhoban@10.0.0.1"

OUTPUT_DIR="vive_logs"
VIVE_DIR='src/rhoban/vive_provider/logs/'
VIVE_SERVER_PID=`ps aux|grep vive_server.py|grep -v grep|awk '{print $2}'`

if [ "${VIVE_SERVER_PID}" != "" ]; then
  echo "Warning: a vive server is running, if you press enter it will be killed to dump its log"
  read X
  kill -2 ${VIVE_SERVER_PID}
  sleep 0.5
fi

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

    #mkdir -p ${OUTPUT_DIR}
    #scp -r ${HOST}:${LOG_PATH}/${LAST_LOG} ${OUTPUT_DIR}
    scp ${VIVE_DIR}/$LAST_VIVE $HOST:${LOG_PATH}/${LAST_LOG}/vive.bin
    
    echo "* Uploaded vive.bin from ${LAST_VIVE} to ${LAST_LOG}"
else
    echo "${LOG_PATH} not found on ${HOST}"
    exit -1
fi
