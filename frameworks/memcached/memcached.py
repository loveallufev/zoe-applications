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


def memcached_service():
    """
    :rtype: dict
    """
    service = {
        'name': "memcached",
        'docker_image': 'memcached:alpine',
        'monitor': True,
        'required_resources': {"memory": 64 * 1024 * 1024},  # 64M
        'ports': [],
        'environment': [],
        'volumes': [],
        'command': '',
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }

    return service

