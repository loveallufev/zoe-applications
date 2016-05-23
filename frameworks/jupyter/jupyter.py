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


def jupyter_notebook_service(mem_limit, image):
    """
    :type mem_limit: int
    :type image: str
    :rtype: dict
    """
    service = {
        'name': "jupyter",
        'docker_image': image,
        'monitor': True,
        'required_resources': {"memory": mem_limit},
        'ports': [
            {
                'name': "Jupyter Notebook interface",
                'protocol': "http",
                'port_number': 8888,
                'path': "/",
                'is_main_endpoint': True,
                'expose': True
            }
        ],
        'environment': [
            ["NB_USER", "{user_name}"]
        ],
        'networks': [],
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }
    return service

