#!/bin/sh

# TODO remove the slash at the end of parameters, if there is one
# TODO retrieve all logs in parallele 
# TODO clean output and add informations
# TODO maybe create a new downloadQtMonitorLog.sh to move the log from qt_monitoring

TIMEOUT=3;

SWITCH="rhoban@10.2.0.10"

if [ $# -lt 2 ]
then
    echo "./downloadAllGameLog.sh <OUTPUT_FOLDER> <QT_MONITORING_FOLDER>" 
    exit -1
else 
    OUTPUT_PARENT_DIR=$1
    QT_MONITORING_FOLDER=$2
fi

echo "logs save in :" ${OUTPUT_PARENT_DIR}

echo "Move logs from monitor"
OUTPUT_MONITOR_DIR=${OUTPUT_PARENT_DIR}/"monitor"
mkdir -p ${OUTPUT_MONITOR_DIR} 
find ${QT_MONITORING_FOLDER}/* -maxdepth 0 -type d -exec mv '{}'  ${OUTPUT_MONITOR_DIR} \;  >/dev/null

# Retrieving all robot's log
for NUMBER in 1 2 3 4 5
do
    HOST=$SWITCH$NUMBER
    
    echo "---------------------------------------------"
    echo "Try to connect to " $HOST
    ROBOT=$(ssh -q -o ConnectTimeout=$TIMEOUT $HOST hostname) 
#    ROBOT=$(ssh -q -o ConnectTimeout=$TIMEOUT $HOST hostname >/dev/null) 
  
    if [ -z $ROBOT ]
    then 
      echo "Robot " $NUMBER "not connected."  
      continue    
    else 
      echo "START !" 
    fi

    if ssh -o ConnectTimeout=$TIMEOUT $HOST [ -d $LOG_PATH ] >/dev/null
    then
 	OUTPUT_DIR_LOG=$OUTPUT_PARENT_DIR'/team9/'${ROBOT}'/output_log'
        OUTPUT_DIR_PERCEPTION=$OUTPUT_PARENT_DIR'/team9/'${ROBOT}'/perception'

        LOG_PATH="/home/rhoban/env/${ROBOT}/game_logs"
	COMPRESS_NAME="tmp_logs"

	mkdir -p ${OUTPUT_DIR_LOG}
	mkdir -p ${OUTPUT_DIR_PERCEPTION}
        mkdir -p ${OUTPUT_PARENT_DIR}/${COMPRESS_NAME}  

        # compress log folder
	echo "compressing... pls wait"
        ssh ${HOST} tar czvf ${COMPRESS_NAME}'.tar.gz' ${LOG_PATH} >/dev/null

        # copy compress log folder
        echo "retrieving archive... pls wait"
        scp -r ${HOST}:${COMPRESS_NAME}'.tar.gz' ${OUTPUT_PARENT_DIR}/${COMPRESS_NAME}

	# uncompress log copy
        echo "uncompress archive..."
        tar xzvf ${OUTPUT_PARENT_DIR}/${COMPRESS_NAME}/${COMPRESS_NAME}.tar.gz  -C ${OUTPUT_PARENT_DIR}/${COMPRESS_NAME}/ >/dev/null

        # move .log to perception folder
        echo "move .log to log folder" 
        mv $(find ${OUTPUT_PARENT_DIR}/${COMPRESS_NAME}${LOG_PATH}/ -name "*.log") ${OUTPUT_DIR_LOG}

        # move all directories that contains images to perception folder
        echo "move images folder to perception folder" $HOST
	find ${OUTPUT_PARENT_DIR}/${COMPRESS_NAME}${LOG_PATH}/* -maxdepth 0 -type d -exec mv '{}'  ${OUTPUT_DIR_PERCEPTION} \;  >/dev/null
	
	#delete files on robot
        ssh ${HOST} "rm -rf ${LOG_PATH}" 
        ssh ${HOST} rm ${COMPRESS_NAME}'.tar.gz'

	#delete tmp files 
       rm -rf ${OUTPUT_PARENT_DIR}/${COMPRESS_NAME}

	echo $ROBOT "done"
    else 
        echo "${LOG_PATH} not found on ${HOST}'('${ROBOT}')'"
        continue
    fi
done







