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

options = [
    ('datanode_count', 3, 'Number of datanodes'),
    ('namenode_image', '192.168.45.252:5000/zoerepo/hadoop-namenode'),
    ('datanode_image', '192.168.45.252:5000/zoerepo/hadoop-datanode')
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(datanode_count,
            namenode_image, datanode_image):
    app = {
        'name': APP_NAME,
        'version': 2,
        'will_end': False,
        'priority': 512,
        'requires_binary': False,
        'services': [
            hadoop_framework.hadoop_namenode_service(namenode_image),
            hadoop_framework.hadoop_datanode_service(datanode_count, datanode_image),
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
