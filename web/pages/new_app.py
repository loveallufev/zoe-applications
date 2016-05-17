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
import json

import tornado.gen
import tornado.web
import tornado.httpclient

import web.base_handler
from web.config import get_conf

import applications.misc.notebook
import applications.spark_jupyter.eurecom_aml_lab


class NewAppHandler(web.base_handler.BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        try:
            app_base = self.get_argument('app_base')
        except tornado.web.MissingArgumentError:
            self.redirect('/')
            return

        if app_base == 'simple_notebook':
            app_name = applications.misc.notebook.APP_NAME
            options = applications.misc.notebook.options
        elif app_base == 'spark_notebook':
            app_name = applications.spark_jupyter.eurecom_aml_lab.APP_NAME
            options = applications.spark_jupyter.eurecom_aml_lab.options
        else:
            self.redirect('/')
            return

        http_client = tornado.httpclient.AsyncHTTPClient()
        image_list = yield http_client.fetch(get_conf().registry_url + "/v2/_catalog")
        image_list = json.loads(image_list.body.decode('utf-8'))['repositories']
        image_list = [get_conf().registry_url[7:] + "/" + img for img in image_list]

        template_vars = {
            'app_base': app_base,
            'app_name': app_name,
            'options': options,
            'image_list': image_list
        }

        self.render('new_app.html', **template_vars)
