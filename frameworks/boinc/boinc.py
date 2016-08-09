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


def boinc_client(image, project_url, project_key):
    """
    :rtype: dict
    """
    service = {
        'name': "boinc-client",
        'docker_image': image,
        'monitor': True,
        'required_resources': {"memory": 512 * 1024 * 1024},  # 512MB
        'ports': [],
        'environment': [
            ['PROJECT_URL', project_url],
            ['PROJECT_KEY', project_key]
        ],
        'volumes': [],
        'command': '',
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }

    return service
