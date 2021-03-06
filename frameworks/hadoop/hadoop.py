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


def hadoop_namenode_service(image):
    """
    :type image: str
    :rtype: dict
    """
    service = {
        'name': "namenode",
        'docker_image': image,
        'monitor': True,
        'required_resources': {"memory": 2 * 1024 * 1024 * 1024},  # 2 GB
        'ports': [
            {
                'name': "NameNode web interface",
                'protocol': "http",
                'port_number': 50070,
                'path': "/",
                'is_main_endpoint': True
            }
        ],
        'networks': [],
        'volumes': [],
        'environment': [
            ["NAMENODE_HOST", "{dns_name#self}:8020"]
        ],
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }
    return service


def hadoop_datanode_service(count, image):
    """
    :type count: int
    :type image: str
    :rtype: List(dict)
    """
    service = {
        'name': "datanode{}".format(i),
        'docker_image': image,
        'monitor': False,
        'required_resources': {"memory": 1 * 1024 * 1024 * 1024},  # 1 GB
        'ports': [],
        'networks': [],
        'volumes': [],
        'environment': [
            ["NAMENODE_HOST", "{dns_name@namenode0}:8020"]
        ],
        'total_count': count,
        'essential_count': count,
        'startup_order': 1
    }
    return service


def hadoop_client_service(image, namenode_address, user, command):
    """
    :type command: str
    :type namenode_address: str
    :type user: str
    :type image: str
    :rtype: List(dict)
    """
    service = {
        'name': "hadoop-client",
        'docker_image': image,
        'monitor': False,
        'required_resources': {"memory": 1 * 1024 * 1024 * 1024},  # 1 GB
        'ports': [],
        'environment': [
            ["NAMENODE_HOST", namenode_address],
            ["HDFS_USER", user]
        ],
        'networks': [],
        'volumes': [],
        'command': command,
        'total_count': 1,
        'essential_count': 1,
        'startup_order': 0
    }
    return service
