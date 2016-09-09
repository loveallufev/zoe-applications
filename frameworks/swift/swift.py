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


def swift_proxy_service(proxy_image, volume_conf, constraint_host, memcached_server):
    """
    :rtype: dict
    """
    service = {
        'name': "swift-proxy",
        'docker_image': proxy_image,
        'monitor': True,
        'required_resources': {"memory": 1024 * 1024 * 1024},  # 1G
        'ports': [
            {
                'name': "Swift proxy interface",
                'protocol': "http",
                'port_number': 8080,
                'path': "/",
                'is_main_endpoint': True,
                'expose': True
            }
        ],
        'environment': [
            ('MEMCACHED_SERVER', memcached_server)
        ],
        'volumes': [
            (volume_conf, '/etc/swift', False)
        ],
        'constraints': [
            'constraint:node==' + constraint_host
        ],
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }

    return service

def swift_configurator_service(configurator_image, volume_conf, zoe_api_endpoint):
    """
    :rtype: dict
    """
    service = {
        'name': "swift-configurator",
        'docker_image': configurator_image,
        'monitor': False,
        'required_resources': {"memory": 512 * 1024 * 1024},  # 512M
        'ports': [],
        'environment': [
            ('ZOE_EXECUTION_ID', '{execution_id}'),
            ('ZOE_URL', zoe_api_endpoint)
        ],
        'volumes': [
            (volume_conf, '/etc/swift', False)
        ],
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 1
    }

    return service

def swift_storage_service(storage_image, volume_conf, volume_storage, constraint_host):
    """
    :rtype: dict
    """
    disk_no_slashes = volume_storage.replace('/', '')
    service = {
        'name': "swift-" + constraint_host + disk_no_slashes + "-storage",
        'docker_image': storage_image,
        'monitor': False,
        'required_resources': {"memory": 1024 * 1024 * 1024},  # 1G
        'ports': [],
        'environment': [],
        'volumes': [
            (volume_conf, '/etc/swift', False),
            (volume_storage, '/srv/node/storage', False)
        ],
        'constraints': [
            'constraint:node==' + constraint_host
        ],
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }

    return service

