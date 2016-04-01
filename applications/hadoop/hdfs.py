#!/usr/bin/env python

# Copyright (c) 2015, Daniele Venzano
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
import frameworks.hadoop.hadoop as hadoop_framework

#################################
# Zoe Application customization #
#################################

APP_NAME = 'hdfs'
DATANODE_COUNT = 3
NAMENODE_IMAGE = 'zoerepo/hadoop-namenode'
DATANODE_IMAGE = 'zoerepo/hadoop-datanode'
DOCKER_REGISTRY = '192.168.45.252:5000'  # Set to None to use images from the Docker Hub

#####################
# END CUSTOMIZATION #
#####################


def hdfs_app(name,
             datanode_count,
             namenode_image, datanode_image):
    app = {
        'name': name,
        'version': 1,
        'will_end': False,
        'priority': 512,
        'requires_binary': False,
        'services': [
            hadoop_framework.hadoop_namenode_service(namenode_image),
        ] + hadoop_framework.hadoop_datanode_service(datanode_count, datanode_image)
    }
    return app

if __name__ == "__main__":
    if DOCKER_REGISTRY is not None:
        NAMENODE_IMAGE = DOCKER_REGISTRY + '/' + NAMENODE_IMAGE
        DATANODE_IMAGE = DOCKER_REGISTRY + '/' + DATANODE_IMAGE

    app_dict = hdfs_app(APP_NAME, DATANODE_COUNT, NAMENODE_IMAGE, DATANODE_IMAGE)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')
