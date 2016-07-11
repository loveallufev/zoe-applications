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


import os.path


def copier_service(src_volume_host_path, src_path, dst_path):
    """
    :type src_volume_host_path: str
    :type src_path: str
    :type dst_path: str
    :rtype: dict
    """
    service = {
        'name': "copier",
        'docker_image': 'alpine',
        'monitor': True,
        'required_resources': {"memory": 128 * 1024 * 1024},  # 128MB
        'ports': [],
        'environment': [],
        'volumes': [],
        'command': '',
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }
    service['volumes'].append([src_volume_host_path, '/mnt/copy-src', True])
    service['command'] = 'cp -a ' + os.path.join('/mnt/copy-src', src_path) + ' ' + os.path.join('/mnt/workspace', dst_path)

    return service


def sleeper_service(sleep_duration):
    """
    :type sleep_duration: int
    :rtype: dict
    """
    service = {
        'name': "sleeper",
        'docker_image': 'alpine',
        'monitor': True,
        'required_resources': {"memory": 1 * 1024 * 1024 * 1024},  # 1 GB
        'ports': [],
        'environment': [],
        'command': 'sleep ' + str(sleep_duration),
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }
    return service
