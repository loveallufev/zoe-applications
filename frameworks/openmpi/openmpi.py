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


def openmpi_worker_service(count, image, worker_memory):
    """
    :type count: int
    :type image: str
    :type worker_memory: int
    :rtype: dict
    """
    service = {
        'name': "mpiworker",
        'docker_image': image,
        'monitor': False,
        'required_resources': {"memory": worker_memory},
        'ports': [],
        'environment': [],
        'volumes': [],
        'command': '',
        'total_count': count,
        'essential_count': count,
        'startup_order': 0
    }
    return service


def openmpi_mpirun_service(mpirun_commandline, image, worker_memory):
    """
    :type mpirun_commandline: str
    :type image: str
    :type worker_memory: int
    :rtype: dict
    """
    service = {
        'name': "mpirun",
        'docker_image': image,
        'monitor': True,
        'required_resources': {"memory": worker_memory},
        'ports': [],
        'environment': [],
        'volumes': [],
        'command': mpirun_commandline,
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 1
    }
    return service
