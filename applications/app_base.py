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

ZOE_APPLICATION_DESCRIPTION_VERSION = 2


def fill_app_template(name, will_end, service_list):
    if not isinstance(name, str):
        raise TypeError('name must be a string')
    if not isinstance(will_end, bool):
        raise TypeError('will_end must be a bool')
    if not isinstance(service_list, list):
        raise TypeError('service list must be a list')
    app = {
        'name': name,
        'version': ZOE_APPLICATION_DESCRIPTION_VERSION,
        'will_end': will_end,
        'priority': 512,
        'requires_binary': True,
        'services': service_list
    }
    return app
