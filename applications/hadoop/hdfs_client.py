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

APP_NAME = 'hdfs-client'

options = [
    ('image', '192.168.45.252:5000/zapps/hadoop-client', 'Image name'),
    ('namenode', 'namenode_host', 'Namenode hostname'),
    ('user', 'root', 'User to run the command as'),
    ('command', 'hdfs dfs -ls /', 'HDFS command to run'),
    ('hdfs_network_id', '<some id>', 'HDFS docker network ID')
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(image, namenode, user, command, hdfs_network_id):
    hdfs_client = hadoop_framework.hadoop_client_service(image, namenode, user, command)
    hdfs_client['networks'].append(hdfs_network_id)
    app = {
        'name': APP_NAME,
        'version': 2,
        'will_end': True,
        'priority': 512,
        'requires_binary': False,
        'services': [
            hdfs_client
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
