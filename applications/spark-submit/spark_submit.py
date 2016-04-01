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

import sys
import json
sys.path.append('../..')
import frameworks.spark.spark as spark_framework

#################################
# Zoe Application customization #
#################################

APP_NAME = 'spark-submit'
SPARK_MASTER_MEMORY_LIMIT = 4 * (1024**3)  # 4GB
SPARK_WORKER_MEMORY_LIMIT = 8 * (1024**3)  # 8GB
SPARK_WORKER_CORES = 4
SPARK_WORKER_COUNT = 3
DOCKER_REGISTRY = '192.168.45.252:5000'  # Set to None to use images from the Docker Hub
SPARK_MASTER_IMAGE = 'zoerepo/spark-master'
SPARK_WORKER_IMAGE = 'zoerepo/spark-worker'
SPARK_SUBMIT_IMAGE = 'zoerepo/spark-submit'
COMMANDLINE = 'wordcount.py hdfs://192.168.45.157/datasets/gutenberg_big_2x.txt hdfs://192.168.45.157/tmp/cntwdc1'

#####################
# END CUSTOMIZATION #
#####################


def spark_submit_app(name,
                     master_mem_limit, worker_mem_limit, worker_cores,
                     worker_count,
                     master_image, worker_image, submit_image,
                     commandline):
    app = {
        'name': name,
        'version': 1,
        'will_end': False,
        'priority': 512,
        'requires_binary': True,
        'services': [
            spark_framework.spark_master_service(master_mem_limit, master_image),
            spark_framework.spark_submit_service(master_mem_limit, worker_mem_limit, submit_image, commandline)
        ] + spark_framework.spark_worker_service(worker_count, worker_mem_limit, worker_cores, worker_image)
    }
    return app

if __name__ == "__main__":
    if DOCKER_REGISTRY is not None:
        SPARK_MASTER_IMAGE = DOCKER_REGISTRY + '/' + SPARK_MASTER_IMAGE
        SPARK_WORKER_IMAGE = DOCKER_REGISTRY + '/' + SPARK_WORKER_IMAGE
        SPARK_SUBMIT_IMAGE = DOCKER_REGISTRY + '/' + SPARK_SUBMIT_IMAGE

    app_dict = spark_submit_app(APP_NAME, SPARK_MASTER_MEMORY_LIMIT, SPARK_WORKER_MEMORY_LIMIT, SPARK_WORKER_CORES, SPARK_WORKER_COUNT, SPARK_MASTER_IMAGE, SPARK_WORKER_IMAGE, SPARK_SUBMIT_IMAGE, COMMANDLINE)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')
