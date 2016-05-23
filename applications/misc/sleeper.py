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
from frameworks.utils.utils import sleeper_service

#################################
# Zoe Application customization #
#################################

APP_NAME = 'sleeper'
options = [
    ('sleep_duration', 5, 'Amount of time to sleep (seconds)')
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(sleep_duration):
    app = {
        'name': APP_NAME,
        'version': 2,
        'will_end': True,
        'priority': 512,
        'requires_binary': False,
        'services': [
            sleeper_service(sleep_duration)
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
