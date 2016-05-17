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
import frameworks.spark.spark_jupyter as spark_jupyter

#################################
# Zoe Application customization #
#################################

APP_NAME = 'spark-jupyter'
SPARK_MASTER_MEMORY_LIMIT = 512 * (1024**2)  # 512MB
SPARK_WORKER_MEMORY_LIMIT = 12 * (1024**3)  # 12GB
NOTEBOOK_MEMORY_LIMIT = 4 * (1024**3)  # 4GB, contains also the Spark client
SPARK_WORKER_CORES = 4
SPARK_WORKER_COUNT = 2
DOCKER_REGISTRY = '192.168.45.252:5000'  # Set to None to use images from the Docker Hub
SPARK_MASTER_IMAGE = 'zoerepo/spark-master'
SPARK_WORKER_IMAGE = 'zoerepo/spark-worker'
NOTEBOOK_IMAGE = 'zoerepo/spark-jupyter-notebook'

#####################
# END CUSTOMIZATION #
#####################


def spark_jupyter_notebook_app(name,
                               notebook_mem_limit, master_mem_limit, worker_mem_limit, worker_cores,
                               worker_count,
                               master_image, worker_image, notebook_image):
    sp_master = spark_framework.spark_master_service(master_mem_limit, master_image)
    sp_workers = spark_framework.spark_worker_service(worker_count, worker_mem_limit, worker_cores, worker_image)

    app = {
        'name': name,
        'version': 1,
        'will_end': False,
        'priority': 512,
        'requires_binary': False,
        'services': [
            sp_master,
            spark_jupyter.spark_jupyter_notebook_service(notebook_mem_limit, worker_mem_limit, notebook_image)
        ] + sp_workers
    }
    return app

if __name__ == "__main__":
    if DOCKER_REGISTRY is not None:
        SPARK_MASTER_IMAGE = DOCKER_REGISTRY + '/' + SPARK_MASTER_IMAGE
        SPARK_WORKER_IMAGE = DOCKER_REGISTRY + '/' + SPARK_WORKER_IMAGE
        NOTEBOOK_IMAGE = DOCKER_REGISTRY + '/' + NOTEBOOK_IMAGE

    app_dict = spark_jupyter_notebook_app(APP_NAME, NOTEBOOK_MEMORY_LIMIT, SPARK_MASTER_MEMORY_LIMIT, SPARK_WORKER_MEMORY_LIMIT, SPARK_WORKER_CORES, SPARK_WORKER_COUNT, SPARK_MASTER_IMAGE, SPARK_WORKER_IMAGE, NOTEBOOK_IMAGE)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')
