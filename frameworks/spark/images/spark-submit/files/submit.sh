#!/usr/bin/env bash

set -e

cd $WS_DIR

exec /opt/spark/bin/spark-submit --master spark://${SPARK_MASTER_IP}:7077 --executor-memory=${SPARK_EXECUTOR_RAM} "$@"

