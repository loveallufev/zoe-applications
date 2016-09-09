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
from frameworks.memcached.memcached import memcached_service
from frameworks.swift.swift import swift_configurator_service, swift_storage_service, swift_proxy_service
import applications.app_base

#################################
# Zoe Application customization #
#################################

APP_NAME = 'swift'

REGISTRY = 'docker-registry:5000'

options = [
    ('proxy_image', REGISTRY + '/experimental/swift-proxy', 'Name of the Swift proxy image'),
    ('storage_image', REGISTRY + '/experimental/swift-storage', 'Name of the Swift storage image'),
    ('configurator_image', REGISTRY + '/experimental/swift-configurator', 'Name of the Swift configurator image'),
    ('volume_conf', '/mnt/cephfs/docker-volumes/swift-conf', 'Path to a writable directory on the shared filesystem'),
    ('zoe_api_endpoint', 'http://bf5:8080/api/0.6', 'Base path of the Zoe API service'),
    ('proxy_node', 'bf13', 'Host on which to place the Swift proxy'),
    ('memcached_server', '{dns_name#memcached0}', 'Memcached server to use to cache auth tokens')
]

# Disks to use for Swift storage nodes
# Format: <hostname>, <XFS partition mountpoint>
storage_nodes = [
    ['bf12', '/mnt/sdc'],
    ['bf15', '/mnt/sdc'],
    ['bf14', '/mnt/sdc']
]

#####################
# END CUSTOMIZATION #
#####################


def gen_app(proxy_image, storage_image, configurator_image, volume_conf, zoe_api_endpoint, proxy_node, memcached_server):
    proxy = swift_proxy_service(proxy_image, volume_conf, proxy_node, memcached_server)
    services = [
        proxy,
        swift_configurator_service(configurator_image, volume_conf, zoe_api_endpoint),
        memcached_service()
    ]
    for host, path in storage_nodes:
        services.append(swift_storage_service(storage_image, volume_conf, path, host))
        
    return applications.app_base.fill_app_template(APP_NAME, False, services)

if __name__ == "__main__":
    args = {}
    for opt in options:
        args[opt[0]] = opt[1]
    app_dict = gen_app(**args)
    json.dump(app_dict, sys.stdout, sort_keys=True, indent=4)
    sys.stdout.write('\n')
