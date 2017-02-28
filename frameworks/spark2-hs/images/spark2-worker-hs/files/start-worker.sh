#!/usr/bin/env bash


cat /opt/spark-defaults.conf | sed -e "s/XXX_DRIVER_MEMORY/$SPARK_DRIVER_RAM/" > ${SPARK_HOME}/conf/spark-defaults.conf

cd /opt/spark


function escape {
    echo $1 | sed "s|\.|\\\.|g" | sed "s|/|\\\/|g"
}


function replace_or_add {
    key=$1; value=$2; file=$3
    if grep -Fq ${key} ${file}
    then
        # if found
        regex="s/\(`escape ${key}`\s*\)\(.*\)/\1`escape ${value}`/"
        sed -i.bak ${regex} ${file}
    else
        echo "${key} ${value}" >> ${file}
    fi
}

log_dir=/tmp/spark-events
full_log_dir=file://${log_dir}
replace_or_add "spark.eventLog.enabled" "true" "${SPARK_HOME}/conf/spark-defaults.conf"
replace_or_add "spark.eventLog.dir" "${full_log_dir}"  "${SPARK_HOME}/conf/spark-defaults.conf"
replace_or_add "spark.history.fs.logDirectory" "${full_log_dir}" "${SPARK_HOME}/conf/spark-defaults.conf"

mkdir -p ${log_dir}

./bin/spark-class org.apache.spark.deploy.worker.Worker \
	spark://${SPARK_MASTER_IP}:7077 --cores ${SPARK_WORKER_CORES:-4} --memory ${SPARK_WORKER_RAM:-4g} \
	-h ${SPARK_LOCAL_IP:-127.0.0.1} "$@"
