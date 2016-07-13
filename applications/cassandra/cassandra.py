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
from frameworks.cassandra.cassandra import cassandra_master_service, cassandra_node_service
import applications.app_base

#################################
# Zoe Application customization #
#################################

APP_NAME = 'cassandra'
options = [
    ('node_count', 5, 'Total number of Cassandra nodes')
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(node_count):
    services = [
        cassandra_master_service(),
        cassandra_node_service(node_count - 1)
    ]
    return applications.app_base.fill_app_template(APP_NAME, False, services)

if __name__ == "__main__":
    args = {}
    for opt in options:
        args[opt[0]] = opt[1]
    app_dict = gen_app(**args)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')
