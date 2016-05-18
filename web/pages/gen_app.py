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
import tornado.gen
import tornado.web

import web.base_handler

import applications.hadoop.hdfs_client
import applications.misc.notebook
import applications.misc.sleeper
import applications.spark_jupyter.eurecom_aml_lab
import applications.spark_submit.spark_submit


class GenAppHandler(web.base_handler.BaseHandler):
    @tornado.gen.coroutine
    def post(self):
        app_base = self.get_argument('app_base')
        if app_base == 'simple_notebook':
            gen_func = applications.misc.notebook.gen_app
            options = applications.misc.notebook.options
        elif app_base == 'spark_notebook':
            gen_func = applications.spark_jupyter.eurecom_aml_lab.gen_app
            options = applications.spark_jupyter.eurecom_aml_lab.options
        elif app_base == 'spark_submit':
            gen_func = applications.spark_submit.spark_submit.gen_app
            options = applications.spark_submit.spark_submit.options
        elif app_base == 'test_app':
            gen_func = applications.misc.sleeper.gen_app
            options = applications.misc.sleeper.options
        elif app_base == 'hdfs_client':
            gen_func = applications.hadoop.hdfs_client.gen_app
            options = applications.hadoop.hdfs_client.options
        else:
            self.set_status(404)
            self.finish()
            return

        args = {}
        for opt in options:
            args[opt[0]] = self.get_argument(opt[0])
        app = gen_func(**args)
        self.add_header('Content-Disposition', 'attachment; filename="app.json"')
        self.write(app)
        self.finish()
