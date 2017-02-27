# Copyright (c) 2015, Duc-Trung NGUYEn
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


def generic_service(image, memory, command):
    """
    :type image: str
    :type memory: int
    :rtype: dict
    """
     service = {
        'name': "generic",
        'docker_image': image,
        'monitor': True,
        'required_resources': {"memory": memory},
        'ports': [],
        'environment': [],
        'volumes': [],
        'command': command,
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0,
        'network': []
    }
    return service

