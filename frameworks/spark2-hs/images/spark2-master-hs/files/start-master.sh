#!/usr/bin/env bash
if [ -z ${SPARK_MASTER_IP} ]; then
	export SPARK_MASTER_IP=`awk 'NR==1 {print $1}' /etc/hosts`
fi

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

#cd ${log_dir}
#chmod 755 ${log_dir}
#chmod +r * # grant the read permission to all users for all files

cat "${SPARK_HOME}/conf/spark-defaults.conf"


#/opt/spark/sbin/start-history-server.sh &
#sudo service spark-history-server start

/opt/spark/bin/spark-class org.apache.spark.deploy.master.Master --host $SPARK_MASTER_IP --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT $@

