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
from frameworks.jupyter.jupyter import jupyter_notebook_service

#################################
# Zoe Application customization #
#################################

APP_NAME = 'notebook'
DOCKER_IMAGE = '192.168.45.252:5000/apps/jupyter-notebook'
MEM_LIMIT = 4 * (1024 ** 3)

#####################
# END CUSTOMIZATION #
#####################


def notebook_app(app_name):
    app = {
        'name': app_name,
        'version': 1,
        'will_end': True,
        'priority': 512,
        'requires_binary': False,
        'services': [
            jupyter_notebook_service(MEM_LIMIT, DOCKER_IMAGE)
        ]
    }
    return app

if __name__ == "__main__":
    app_dict = notebook_app(APP_NAME)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')

