#!/usr/bin/env python

# Copyright (c) 2016, Daniele Venzano
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
sys.path.append('../..')

import frameworks.spark.spark as spark_framework
import applications.app_base

#################################
# Zoe Application customization #
#################################

APP_NAME = 'spark-submit'

NUM_WORKERS = 16
NUM_CORE_PER_WORKER = 1

GBs = 1024**3

options = [
    ('client_mem_limit', 1 * GBs, 'Spark client memory limit (bytes)'),
    ('master_mem_limit', 2 * GBs, 'Spark Master memory limit (bytes)'),
    ('worker_mem_limit', 8 * GBs, 'Spark Worker memory limit (bytes)'),
    ('worker_cores', NUM_CORE_PER_WORKER, 'Cores used by each worker'),
    ('worker_count', NUM_WORKERS, 'Number of workers'),
    ('master_image', 'docker-registry:5000/zapps/spark2-master', 'Spark Master image'),
    ('worker_image', 'docker-registry:5000/zapps/spark2-worker', 'Spark Worker image'),
    ('submit_image', 'docker-registry:5000/zapps/spark2-submit', 'Spark Submit image'),
    ('namenode_host', '10.0.0.15', 'Address of the Namenode'),
    ('commandline', 'wordcount.py hdfs://192.168.45.157/datasets/gutenberg_big_2x.txt hdfs://192.168.45.157/tmp/cntwdc1', 'Spark submit command line')
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(client_mem_limit, master_mem_limit, worker_mem_limit, worker_cores,
            worker_count,
            master_image, worker_image, submit_image,
            commandline, namenode_host, 
            expose_submit_service=False,
            monitor_submit_service=True,
            monitor_master_service=False,
            disable_autorestart=False):
    submit_service = spark_framework.spark_submit_service(int(client_mem_limit), int(worker_mem_limit), submit_image, commandline)
    submit_service['environment'].append(['NAMENODE_HOST', namenode_host])
    submit_service['ports'][0]['expose'] = expose_submit_service
    submit_service['monitor'] = monitor_submit_service

    master_service = spark_framework.spark_master_service(int(master_mem_limit), master_image)
    master_service['ports'][0]['expose'] = True
    master_service['monitor'] = monitor_master_service
    master_service['ports'].append({
        "expose": true,
        "is_main_endpoint": false,
        "name": "Spark history server",
        "path": "/",
        "port_number": 18080,
        "protocol": "http"
    })

    workers_service = spark_framework.spark_worker_service(int(worker_count), int(worker_mem_limit), int(worker_cores), worker_image)
    
    services = [
         master_service,
         workers_service,
         submit_service
             ]
    return applications.app_base.fill_app_template(APP_NAME, False, services, disable_autorestart)

if __name__ == "__main__":
    args = {}
    for opt in options:
        args[opt[0]] = opt[1]
    app_dict = gen_app(**args)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')
