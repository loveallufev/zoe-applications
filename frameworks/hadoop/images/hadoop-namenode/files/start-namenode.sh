#!/bin/sh

cd /opt

cat core-site.xml | sed -e "s/XXX_NAMENODE_HOST/$NAMENODE_HOST/" -e "s/SPARK_EXEC_RAM/$SPARK_EXECUTOR_RAM/" > ${HADOOP_HOME}/etc/hadoop/core-site.xml
cp hdfs-site.xml ${HADOOP_HOME}/etc/hadoop/

if [ -n "$FORMAT" ]; then
	${HADOOP_HOME}/bin/hdfs namenode -format hdfscluster
fi

${HADOOP_HOME}/bin/hdfs namenode

