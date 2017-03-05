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

cat "${SPARK_HOME}/conf/spark-defaults.conf"

echo 'Configuration done, starting Spark...'

/opt/spark/bin/spark-submit --master spark://${SPARK_MASTER_IP}:7077 --executor-memory=${SPARK_EXECUTOR_RAM} "$@"

copy_to=${ZOE_WORKSPACE}/spark-events/
if [ ! -d ${copy_to} ]; then 
    mkdir -p ${copy_to}; 
fi; 

file_name=$(find /tmp/spark-events -type f | head -n 1)

gzip ${file_name}
cp ${file_name}.gz ${copy_to}
# current_user=$(stat -c "%U" $ZOE_WORKSPACE)
# current_group=$(stat -c "%G" $ZOE_WORKSPACE)
# chown ${current_user}:${current_group}  ${copy_to}$(basename ${file_name}.gz)
chmod 644 ${copy_to}$(basename ${file_name}.gz)

