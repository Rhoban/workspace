#!/bin/sh

# No arguments : creates folder 'robot_logs' in current directory
# Argument 1 : path of directory where 'robot_logs' will be created

HOST="rhoban@10.0.0.1"

DIR="./robot_logs"

if [ $# -gt 0 ]
then
    DIR=$1"/robot_logs"
else
    DIR="./robot_logs"
fi

# Retrieving robot hostname
ROBOT=$(ssh $HOST hostname)

LOG_PATH="/home/rhoban/env/${ROBOT}/manual_logs/*"

DIR=$DIR'/'${ROBOT}
mkdir -p ${DIR}

# copy files in dir
scp -r ${HOST}:${LOG_PATH} ${DIR}

# delete files on robot
ssh ${HOST} "rm -rf ${LOG_PATH}"


