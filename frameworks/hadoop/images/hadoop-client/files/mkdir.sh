#!/usr/bin/env bash

set -x

MKDIR_PATH=$1

cat /opt/core-site.xml | sed -e "s/XXX_NAMENODE_HOST/$NAMENODE_HOST/" > ${HADOOP_HOME}/etc/hadoop/core-site.xml
cp /opt/hdfs-site.xml ${HADOOP_HOME}/etc/hadoop/

if getent passwd $HDFS_USER; then
	echo "User $HDFS_USER already exists"
else
	useradd -m -s /bin/bash -N $HDFS_USER
fi

/opt/hadoop/bin/hdfs dfs -mkdir $MKDIR_PATH
/opt/hadoop/bin/hdfs dfs -chown $HDFS_USER $MKDIR_PATH
/opt/hadoop/bin/hdfs dfs -chmod 750 $MKDIR_PATH

