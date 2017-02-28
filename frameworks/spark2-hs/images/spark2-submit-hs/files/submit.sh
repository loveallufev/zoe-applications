#!/usr/bin/env bash

set -e

cat /opt/spark-defaults.conf | sed -e "s/XXX_DRIVER_MEMORY/$SPARK_DRIVER_RAM/" > ${SPARK_HOME}/conf/spark-defaults.conf
cat /opt/core-site.xml | sed -e "s/XXX_NAMENODE_HOST/$NAMENODE_HOST/" > ${HADOOP_HOME}/etc/hadoop/core-site.xml
cp /opt/hdfs-site.xml ${HADOOP_HOME}/etc/hadoop/

cd $ZOE_WORKSPACE

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
cd ${log_dir}
chmod +r * # grant the read permission to all users for all files

cat "${SPARK_HOME}/conf/spark-defaults.conf"

echo 'Configuration done, starting Spark...'

/opt/spark/bin/spark-submit --master spark://${SPARK_MASTER_IP}:7077 --executor-memory=${SPARK_EXECUTOR_RAM} "$@"

