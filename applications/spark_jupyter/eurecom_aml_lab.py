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

APP_NAME = 'aml-lab'

options = [
    ('master_mem_limit', 512 * (1024**2), 'Spark Master memory limit (bytes)'),
    ('worker_mem_limit', 12 * (1024**3), 'Spark Worker memory limit (bytes)'),
    ('notebook_mem_limit', 12 * (1024**3), 'Notebook memory limit (bytes)'),
    ('worker_cores', 6, 'Cores used by each worker'),
    ('worker_count', 2, 'Number of workers'),
    ('master_image', '192.168.45.252:5000/zoerepo/spark-master', 'Spark Master image'),
    ('worker_image', '192.168.45.252:5000/zoerepo/spark-worker', 'Spark Worker image'),
    ('notebook_image', '192.168.45.252:5000/zoerepo/spark-jupyter-notebook', 'Jupyter notebook image'),
    ('hdfs_network_id', '07e76e17d68117653d2147827a3a309d113eedc761fceecee750ffb6efa442e1', 'Docker Swarm HDFS network ID'),
    ('hdfs_namenode', 'hdfs-namenode.zoe', 'Namenode hostname')
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(notebook_mem_limit, master_mem_limit, worker_mem_limit, worker_cores,
            worker_count,
            master_image, worker_image, notebook_image,
            hdfs_network_id, hdfs_namenode):
    sp_master = spark_framework.spark_master_service(int(master_mem_limit), master_image)
    sp_master['networks'].append(hdfs_network_id)
    sp_worker = spark_framework.spark_worker_service(int(worker_count), int(worker_mem_limit), int(worker_cores), worker_image)
    jupyter = spark_jupyter.spark_jupyter_notebook_service(int(notebook_mem_limit), int(worker_mem_limit), notebook_image)
    jupyter['networks'].append(hdfs_network_id)
    jupyter['environment'].append(['NAMENODE_HOST', hdfs_namenode])

    app = {
        'name': APP_NAME,
        'version': 2,
        'will_end': False,
        'priority': 512,
        'requires_binary': False,
        'services': [
            sp_master,
            sp_worker,
            jupyter,
        ]
    }
    return app

if __name__ == "__main__":
    args = {}
    for opt in options:
        args[opt[0]] = opt[1]
    app_dict = gen_app(**args)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')
