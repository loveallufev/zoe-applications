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
import frameworks.openmpi.openmpi as openmpi_framework

#################################
# Zoe Application customization #
#################################

APP_NAME = 'openmpi'

options = [
    ('commandline', 'mpirun -hostfile hostlist MPI_Hello', 'mpirun commandline'),
    ('mpirun_image', '192.168.45.252:5000/zoeapps/openmpi-ubuntu', 'Image for the mpirun process'),
    ('worker_image', '192.168.45.252:5000/zoeapps/openmpi-ubuntu', 'Image for the worker processes'),
    ('worker_count', 4, 'Number of worker processes'),
    ('cpu_per_worker', 1, 'CPU count per worker'),
    ('worker_memory', 1024 ** 3, 'Memory reservation for each worker')
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(mpirun_image, worker_image, commandline, worker_count, worker_memory):
    app = {
        'name': APP_NAME,
        'version': 1,
        'will_end': True,
        'priority': 512,
        'requires_binary': True,
        'services': []
    }
    for i in range(worker_count):
        proc = openmpi_framework.openmpi_worker_service(i, worker_image, worker_memory)
        app['services'].append(proc)
    proc = openmpi_framework.openmpi_mpirun_service(commandline, mpirun_image, worker_memory)
    app['services'].append(proc)
    return app


if __name__ == "__main__":
    args = {}
    for opt in options:
        args[opt[0]] = opt[1]
    app_dict = gen_app(**args)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')

    sys.stderr.write('### Copy and customize the following lines to the hostlist file passed to mpirun #####\n')
    for wc in range(options[3][1]):
        sys.stderr.write('mpiworker{}-##Zoe execution name##-##zoe user name##-##zoe deployment name##-zoe:{}\n'.format(wc, options[4][1]))
