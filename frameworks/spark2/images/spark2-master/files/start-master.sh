#!/usr/bin/env bash
if [ -z ${SPARK_MASTER_IP} ]; then
	export SPARK_MASTER_IP=`awk 'NR==1 {print $1}' /etc/hosts`
fi

cd /opt/spark
./bin/spark-class org.apache.spark.deploy.master.Master --host $SPARK_MASTER_IP --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT $@

