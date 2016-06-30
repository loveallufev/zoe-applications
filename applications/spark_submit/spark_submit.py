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

options = [
    ('master_mem_limit', 512 * (1024**2), 'Spark Master memory limit (bytes)'),
    ('worker_mem_limit', 12 * (1024**3), 'Spark Worker memory limit (bytes)'),
    ('worker_cores', 6, 'Cores used by each worker'),
    ('worker_count', 2, 'Number of workers'),
    ('master_image', '192.168.45.252:5000/zoerepo/spark-master', 'Spark Master image'),
    ('worker_image', '192.168.45.252:5000/zoerepo/spark-worker', 'Spark Worker image'),
    ('submit_image', '192.168.45.252:5000/zoerepo/spark-submit', 'Spark Submit image'),
    ('commandline', 'wordcount.py hdfs://192.168.45.157/datasets/gutenberg_big_2x.txt hdfs://192.168.45.157/tmp/cntwdc1', 'Spark submit command line')
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(master_mem_limit, worker_mem_limit, worker_cores,
            worker_count,
            master_image, worker_image, submit_image,
            commandline):
    services = [
        spark_framework.spark_master_service(int(master_mem_limit), master_image),
        spark_framework.spark_worker_service(int(worker_count), int(worker_mem_limit), int(worker_cores), worker_image),
        spark_framework.spark_submit_service(int(master_mem_limit), int(worker_mem_limit), submit_image, commandline)
    ]
    return applications.app_base.fill_app_template(APP_NAME, False, services)

if __name__ == "__main__":
    args = {}
    for opt in options:
        args[opt[0]] = opt[1]
    app_dict = gen_app(**args)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')
