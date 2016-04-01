#!/usr/bin/env bash

set -x

cat /opt/core-site.xml | sed -e "s/XXX_NAMENODE_HOST/$NAMENODE_HOST/" > ${HADOOP_HOME}/etc/hadoop/core-site.xml
cp /opt/hdfs-site.xml ${HADOOP_HOME}/etc/hadoop/
 
/opt/hadoop/bin/hdfs dfs -rm -R -skipTrash $RM_PATH

